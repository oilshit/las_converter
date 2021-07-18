import requests

import json

import pandas as pd
import numpy as np

from datetime import datetime

class WellLog():
    """
    Defines well log database with LAS file input.
     
      parameter input(s):
        - file (str)
          Specifies LAS file inputted for process well log data.
    """
    def __init__(self, file):
        """
        Initiate well log instance
        """

        # validate file source
        ## between local file and URL requests
        if ("https" in file):
            print("Getting LAS file from URL source...")
            self.file = requests.get(file, stream=True).text.split("\n")[:-1]

        else:
            print("Getiing LAS file from local drive...")
            self.file = open(file).readlines()

        # init'd empty information
        self.info = {
            "description": {}
        }

        print("Loading well data. It will takes time for a while...")
        self.load_data()

        return
        
    def load_data(self):
        """
        Load data from LAS file.

          additional notes:
            The function will be executed by default
            when WellLog class is initiated.
        """

        # init'd what information contained in LAS file
        ex_init = datetime.now()
        section_title = ["version", "well", "curve", "parameter", "other"]
        order = 0

        # read each rows of LAS data
        for i in self.file:
            # validate rows of data
            # if contains title section
            if (i[0] == "~"):
                # print(section_title[order] in i.lower())
                las_section = (section_title[order]
                                if "~a" not in i.lower()
                                else "data_table")
                order += 1

                self.info["description"][las_section] = {}
                
                self.info[las_section] = {} 

            # for aniything else
            # it will fill the section init'd before
            else:
                section = list(self.info)
                # print(section)

                if (i[0] != "#"):
                    if (section[-1] != "data_table"):
                        line = " ".join(i.split())
                        line = line.split(":")
                        line[1] = line[1].strip()

                        # define informations properties
                        ## as key-value pair
                        prop_pattern = [j.strip()
                                            for j in line[0]
                                            .split(" ", 1)]

                        prop_pattern[1] = (float(prop_pattern[1])
                                            if prop_pattern[1].isnumeric() == True
                                            else prop_pattern[1])

                        self.info[section[-1]][prop_pattern[0].lower()] = prop_pattern[1]

                        self.info["description"][section[-1]][prop_pattern[0].lower()] = line[1]

                    else:
                        # fill the data table
                        # print(section)

                        # init'd the data table column
                        ## from curve information properties
                        if (self.info["data_table"] == {}):
                            well_specs =  list(self.info["curve"])

                            self.info[["curve"][0]] = well_specs

                            # init'd empty space for each curve property
                            for j in well_specs:
                                self.info["data_table"][j] = np.array([])


                        # init'd null values
                        ## based on well information
                        null_values = [k for k in self.info["well"] if "null" in k][0]

                        data_ranges = np.array([j for j in " ".join(i.split()).split(" ")]).astype("float64")
                        
                        for j in range(len(well_specs)):
                            data_filled = data_ranges[j] if (data_ranges[j] != float(self.info["well"][null_values])) else None

                            self.info["data_table"][
                                    well_specs[j]
                                ] = np.append(self.info["data_table"][well_specs[j]],
                                              data_filled)

        print("Well log data loaded for {} s".format((datetime.now() - ex_init).total_seconds()))

        return
                        
    def get_description(self, section=None):
        """
        Get the loaded well log data description
        
          parameter input(s):
            - section (str)
              Get the well log information based on section input
              Return list of sections input provided if section is not given
              Default value = None
        
          output(s)
            - list of sections input provided (if section == None)
            - list of section properties based on section input given     
        """

        if (section == None):
            print("There are some well properties with description provided.")

            for i, j in self.info["description"].items():
                print("-", i)

        else:
            if (self.info["description"][section]) != {}:
                print("Describing well log information about '%s'" % (section))

                for i, j in self.info["description"][section].items():
                    print("-", i, ":", j)
            
            else:
                print("There are no description in section: '%s'" % (section))

        return

    def get_data(self, section):
        """
        Get the loaded well log data information
        
          parameter input(s):
            - section (str)
              Get the well log information based on section input
        
          output(s)
            - list of information based on input provided.   
        """

        if (section != None):
            print("Getting information:", section)
            # manual print for getting well log description
            if ("curve" in section):
                for i in self.info[section]:
                    print(i)
            else:
                for i, j in self.info[section].items():
                    print("-", i, ":", j)
                
        return

    def save_file(self, file_as):
        """
        Save the LAS file into other file
        JSON and CSV file are supported
        
          parameter input(s):
            - file_as (str)
              File extension will be used to save the file
        
          output(s)
            - File based on extension     
        """

        if (file_as == "JSON" or
          file_as == "JSON".lower()):
            well_temp = self.info["data_table"]

            for i, j in self.info["data_table"].items():
                self.info["data_table"][i] = list(j)

            with open('results/well.json', 'w') as json_file:
                json.dump(self.info, json_file)

            self.info["data_table"] = well_temp
            
            print("Well log data saved as JSON.")

        elif (file_as == "CSV" or
          file_as == "CSV".lower()):
            well_temp = self.info["data_table"]

            df = pd.DataFrame(well_temp)
            df.to_csv("results/well.csv", index=False)

            complete_desc = {}

            for i, j in self.info["description"].items():
                complete_desc.update(j)

            df = pd.DataFrame(complete_desc, index=[0])
            df = df.T.reset_index()
            df.rename(columns={"index": "name", 0: "description"}, inplace=True)

            df.to_csv("results/description.csv", index=False)

            print("Well log data saved as CSV (well.csv and description.csv).")

        else:
            print("File extension is not supported")

        return