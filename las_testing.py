# importing las_converter
import las_converter
## from las_converter import WellLog

# # init'd well log instance
# ## based on file input
# log1 = las_converter.WellLog("/home/dimaswehhh/Downloads/well log data/WA1.LAS")

# # get LAS data description
# ## it will describe well data section
# ## for null arguments
# log1.get_description()

# ## display specific description for well information
# log1.get_description("well")

# let's try with another well instance ...
## from URL source
# log2 = las_converter.WellLog("https://certmapper.cr.usgs.gov/data/PubArchives/of00-200/wells/WALAKPA2/LAS/WA2.LAS")
log2 = las_converter.WellLog("samples/TU1.LAS")

# ... and also display well 2 information
# log2.get_description()
# log2.get_description("well")

# log2.get_data("well")

# let's test for saving well 2
## in JSON
# log2.save_file("json")

i = int(input("""\ntype action: 
1. view description of well data
2. save file data
any number for quit
> \33[33m\33[1m"""))


while (i <= 2):
    if (i == 1):
        log2.get_description()
        desc_input = str(
            input(
                "\n\33[0mtype the description: \33[33m\33[1m"
        ))

        log2.get_description(desc_input)

    elif (i == 2):
        save_input = str(
            input(
                ("\n\33[0mselect file type to save (JSON or CSV supported): \33[33m\33[1m")
        ))

        log2.save_file(save_input)

    i = int(input("""\n\33[0mtype action: 
1. view description of well data
2. save file data
any number for quit
> \33[33m\33[1m"""))

print("\nquiting...")
