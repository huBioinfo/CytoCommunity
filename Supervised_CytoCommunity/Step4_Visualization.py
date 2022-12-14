import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import glob
import os
import datetime


# Hyperparameter
InputFolderName = "./CODEX_ColonCancer_KNNgraph_Input/"

# Create output folders
OutputFolderName_1 = "./TCN_Plot/"
os.mkdir(OutputFolderName_1)
OutputFolderName_2 = "./CellType_Plot/"
os.mkdir(OutputFolderName_2)
OutputFolderName_3 = "./TargetGraphDF_File/"
os.mkdir(OutputFolderName_3)

#Time_FolderName = glob.glob("*Time*")
# Import region name list.
Region_filename = InputFolderName + "ImageNameList.txt"
region_name_list = pd.read_csv(
        Region_filename,
        sep="\t",  # tab-separated
        header=None,  # no heading row
        names=["Image"],  # set our own names for the columns
    )

print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
Image_FolderName = glob.glob("ImageCollection/*")
for kk in range(0, len(Image_FolderName)):
    
    print(f"This is Image{kk+1}/{len(Image_FolderName)}")

    # Import graph index.
    GraphIndex_filename = Image_FolderName[kk] + "/GraphIdx_Time1_Fold1.csv"
    graph_index = np.loadtxt(GraphIndex_filename, dtype='int', delimiter=",")

    # Import target graph x/y coordinates.
    region_name = region_name_list.Image[graph_index]
    GraphCoord_filename = InputFolderName + region_name + "_Coordinates.txt"
    x_y_coordinates = pd.read_csv(
            GraphCoord_filename,
            sep="\t",  # tab-separated
            header=None,  # no heading row
            names=["x_coordinate", "y_coordinate"],  # set our own names for the columns
        )
    target_graph_map = x_y_coordinates
    target_graph_map["y_coordinate"] = 0 - target_graph_map["y_coordinate"]  # for consistent with original paper. Don't do this is also ok.

    # Import cell type label.
    CellType_filename = InputFolderName + region_name + "_CellTypeLabel.txt"
    cell_type_label = pd.read_csv(
            CellType_filename,
            sep="\t",  # tab-separated
            header=None,  # no heading row
            names=["cell_type"],  # set our own names for the columns
        )
    # Add cell type labels to target graph x/y coordinates.
    target_graph_map["CellType"] = cell_type_label.cell_type

    #!!! Add consensus cluster labels to target graph x/y coordinates.
    MajorityVoting_FileName = Image_FolderName[kk] + "/ConsensusLabel_MajorityVoting.csv"
    target_graph_map["TCN_MajorityVoting"] = np.loadtxt(MajorityVoting_FileName, dtype='int', delimiter=",")
    # Converting integer list to string list for making color scheme discrete.
    target_graph_map.TCN_MajorityVoting = target_graph_map.TCN_MajorityVoting.astype(str)


    #-----------------------------------------Generate plots-------------------------------------------------#
    # Plot x/y map with "TCN" coloring. Note that consensus clustering result is generated by R with 1-indexing.
    dict_color_TCN = {"1": "Green", "2": "Black", "3": "Red", "4": "Blue", \
        "5": "DarkMagenta", "6": "Aqua", "7": "Orange", "8": "LightSeaGreen", "9": "Grey", "10": "FireBrick"}
    TCN_MajorityVoting_fig = sns.lmplot(x="x_coordinate", y="y_coordinate", data=target_graph_map, fit_reg=False, hue='TCN_MajorityVoting', legend=False, palette=dict_color_TCN, scatter_kws={"s": 10.0})
    TCN_MajorityVoting_fig.add_legend(label_order = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
    for lh in TCN_MajorityVoting_fig._legend.legendHandles: 
        #lh.set_alpha(1)
        lh._sizes = [15]   # You can also use lh.set_sizes([15])
    #plt.show()
    # Save the figure.
    TCN_fig_filename = OutputFolderName_1 + "TCN_" + region_name + ".pdf"
    TCN_MajorityVoting_fig.savefig(TCN_fig_filename)

   
   # Plot x/y map with "CellType" coloring.
    dict_color_CellType = {"CD11b+ monocytes": "Navy", "CD11b+CD68+ macrophages": "MediumBlue", "CD163+ macrophages": "Green", "CD68+ macrophages": "DarkCyan", "CD68+ macrophages GzmB+": "DarkTurquoise", \
        "CD68+CD163+ macrophages": "Lime", "CD11c+ DCs": "Aqua", "granulocytes": "MidnightBlue", "NK cells": "LightSeaGreen", "B cells": "Black", "CD3+ T cells": "RoyalBlue", \
            "CD4+ T cells": "Indigo", "CD4+ T cells CD45RO+": "SlateGray", "CD4+ T cells GATA3+": "LawnGreen", "CD8+ T cells": "Yellow", "Tregs": "BlueViolet", "immune cells": "DarkOliveGreen", \
                "lymphatics": "DarkMagenta", "adipocytes": "MediumPurple", "nerves": "YellowGreen", "plasma cells": "FireBrick", "smooth muscle": "DarkKhaki", "stroma": "SkyBlue", "vasculature": "Red", \
                    "tumor cells": "Orange", "tumor cells / immune cells": "Pink", "immune cells / vasculature": "Tan", "undefined": "Gold"}
    CellType_fig = sns.lmplot(x="x_coordinate", y="y_coordinate", data=target_graph_map, fit_reg=False, hue='CellType', legend=False, palette=dict_color_CellType, scatter_kws={"s": 10.0})
    CellType_fig.add_legend(label_order = ["CD11b+ monocytes", "CD11b+CD68+ macrophages", "CD163+ macrophages", "CD68+ macrophages", "CD68+ macrophages GzmB+", \
        "CD68+CD163+ macrophages", "CD11c+ DCs", "granulocytes", "NK cells", "B cells", "CD3+ T cells", \
            "CD4+ T cells", "CD4+ T cells CD45RO+", "CD4+ T cells GATA3+", "CD8+ T cells", "Tregs", "immune cells", \
                "lymphatics", "adipocytes", "nerves", "plasma cells", "smooth muscle", "stroma", "vasculature", \
                    "tumor cells", "tumor cells / immune cells", "immune cells / vasculature", "undefined"])
    for lh in CellType_fig._legend.legendHandles: 
        #lh.set_alpha(1)
        lh._sizes = [15]   # You can also use lh.set_sizes([15])
    # Save the figure.
    CellType_fig_filename = OutputFolderName_2 + "CellType_" + region_name + ".pdf"
    CellType_fig.savefig(CellType_fig_filename)


    # Export dataframe: "target_graph_map".
    TargetGraph_dataframe_filename = OutputFolderName_3 + "TargetGraphDF_" + region_name + ".csv"
    target_graph_map.to_csv(TargetGraph_dataframe_filename, na_rep="NULL", index=False) #remove row index.

print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


