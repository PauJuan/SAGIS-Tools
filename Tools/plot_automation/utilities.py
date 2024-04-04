"""
Utilities library for the chainage plots tool
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
plt.style.use("ggplot")
from cycler import cycler

import arcpy

COLUMNS = [
    "OBJECTID",
    "ReachNo",
    "MeanConc",
    "LCLimMnCon",
    "UCLimMnCon",
    "CalcValQ90",
    "LCLimPer90",
    "UCLimPer90",
    "CalcValQ95",
    "LCLimPer95",
    "UCLimPer95",
    "CalcValQ99",
    "LCLimPer99",
    "UCLimPer99",
    "FeatName",
    "US_DS_Feat",
    "ReachName",
    "ObsConc",
    "ObsConcUCL",
    "ObsConcLCL",
    "ObsQ90Conc",
    "ObsQ90ConcUCL",
    "ObsQ90ConcLCL",
    "ObsQ95Conc",
    "ObsQ99Conc",
    "TargetMean",
    "Target90",
    "DetNo",
    "SWConc",
    "IMConc",
    "INConc",
    "MIConc",
    "LSConc",
    "ARConc",
    "HWConc",
    "URConc",
    "ATConc",
    "BGConc",
    "STConc",
    "LKConc",
    "DConc",
    "TargetHigh",
    "TargetGood",
    "TargetMod",
    "TargetPoor",
    "EA_WB_ID",
    "DiffConc",
    "PntConc",
    "CalStatus",
    "CalScore",
    "DISHeadKM",
    "DISPOINTKM",
]

# Rename sectors for a better legend
APPORTIONMENT_COLS = {
    "SWConc": "Sewage",
    "IMConc": "Intermittent",
    "INConc": "Industry",
    "MIConc": "Mines",
    "LSConc": "Livestock",
    "ARConc": "Arable",
    "HWConc": "Highways",
    "URConc": "Urban",
    "ATConc": "Atmospheric",
    "BGConc": "Background",
    "STConc": "Septic tanks",
    "LKConc": "Lakes",
}

# Prepare colorscale
APPORTIONMENT_COLORMAP = cycler(
    "color",
    [
        "0.1",
        "0.5",
        "r",
        "b",
        "yellowgreen",
        "yellow",
        "g",
        "purple",
        "olive",
        "pink",
        "gold",
        "orange",
        "lightsteelblue"
    ],
)

def spatial_selection(out_layer, reach_layer):
    """
    Carry out spatial selection on plot outputs using the river (2m)
    intersection distance
    """
    arcpy.management.SelectLayerByLocation(
        out_layer, "INTERSECT", reach_layer, "2 Meters", "NEW_SELECTION", "NOT_INVERT"
    )


def plot_chainage_chart(out1, out2, reach, params):
    """
    Takes input data and plots the chainage chart as required
    """
    global APPORTIONMENT_COLS
    global APPORTIONMENT_COLORMAP

    # Prepare parameters
    calibration_flag = params["calibration_flag"]
    target_flag = params["target_flag"]
    annotate_flag = params["annotate_flag"]
    annotate_filter = float(params["annotate_filter"])
    annotate_features = params["annotate_features"]
    if annotate_features:
        annotate_features = [s.replace("'", "") for s in
                             annotate_features.split(';')]
    custom_annotations = params["custom_annotations"]
    if custom_annotations:
        custom_annotations = {
                ' '.join(e.split(' ')[:-1]): float(e.split(' ')[-1])
                for e in custom_annotations.split(';')
                }

    headwater_flag = params["headwater_flag"]
    fig_size = float(params["figure_size"])
    aspect_ratio_modifier = float(params["aspect_ratio_modifier"])
    legend_loc = params["legend_loc"]

    # Get number of plots needed
    num_plots = 1
    if calibration_flag == 'true':
        num_plots += 1
    if out2:
        num_plots +=1

    # Carry out spatial selections for input features
    spatial_selection(out1, reach)
    # Read feature class as dataframe
    df1 = pd.DataFrame.spatial.from_featureclass(out1)
    # Filter necessary columns
    df1 = df1[COLUMNS].copy()
    # Sort per reach ascending
    df1.sort_values(["ReachNo", "OBJECTID"], inplace=True)
    # Calculate cummulative distance
    df1["DISTANCE"] = df1["DISPOINTKM"].cumsum()
    # Calculate diff in concentration
    df1["DIFF_CONC"] = df1["MeanConc"].diff().fillna(0)
    # Set distance as index for x axis
    df1.set_index("DISTANCE", inplace=True)
    # Remove first point next to headwater
    if headwater_flag == 'true':
        df1 = df1[1:].copy()

    # Repeat for second output if needed
    # NOTE This could be refactored into a function
    if out2:
        spatial_selection(out2, reach)
        df2 = pd.DataFrame.spatial.from_featureclass(out2)
        df2 = df2[COLUMNS].copy()
        df2.sort_values(["ReachNo", "OBJECTID"], inplace=True)
        df2["DISTANCE"] = df2["DISPOINTKM"].cumsum()
        df2["DIFF_CONC"] = df2["MeanConc"].diff().fillna(0)
        df2.set_index("DISTANCE", inplace=True)
        if headwater_flag == 'true':
            df2 = df2[1:].copy()

    # Get rid of 0s in Observed concentrations
    df1["ObsConc"].replace(0, np.NaN, inplace=True)
    df1["ObsConcLCL"].replace(0, np.NaN, inplace=True)
    df1["ObsConcUCL"].replace(0, np.NaN, inplace=True)
    if out2:
        df2["ObsConc"].replace(0, np.NaN, inplace=True)
        df2["ObsConcLCL"].replace(0, np.NaN, inplace=True)
        df2["ObsConcUCL"].replace(0, np.NaN, inplace=True)

    # Get metadata
    DETERMINAND = out1.split("GIS1")[1]
    SCENARIO = out1.split("GIS1")[0]
    if out2:
        SCENARIO2 = out2.split("GIS1")[0]

    # Add reach diffuse if needed
    if DETERMINAND in ["Ammonia", "BOD", "DO_9924"]:
        APPORTIONMENT_COLS = {
            "SWConc": "Sewage",
            "IMConc": "Intermittent",
            "INConc": "Industry",
            "MIConc": "Mines",
            "DiffConc": "Reach Diffuse",
        }
        APPORTIONMENT_COLORMAP = cycler(
            "color",
            [
                "0.1",
                "0.5",
                "r",
                "b",
                "lightsteelblue"
            ],
        )

    # Change column names
    df1.rename(APPORTIONMENT_COLS, inplace=True, axis=1)
    if out2:
        df2.rename(APPORTIONMENT_COLS, inplace=True, axis=1)

    # Set figure size
    plt.rcParams["figure.figsize"] = (
            fig_size,  # width
            aspect_ratio_modifier * fig_size / (1.618 * 2 / num_plots)  # height
            )

    # Set colormap
    plt.rcParams["axes.prop_cycle"] = APPORTIONMENT_COLORMAP

    # Set up initial layout
    fig, axes = plt.subplots(nrows=num_plots, ncols=1, sharex=True, sharey=True)

    # Calibration plot
    if calibration_flag == 'true':
        # Simulated data
        df1.MeanConc.plot(ax=axes[0], c="k")
        df1.UCLimMnCon.plot(ax=axes[0], c="k", ls="--", alpha=0.75)
        df1.LCLimMnCon.plot(ax=axes[0], c="k", ls="--", alpha=0.75)

        # Observed data
        df1.ObsConc.plot(ax=axes[0], c="b", marker="o")
        df1.ObsConcUCL.plot(ax=axes[0], c="b", marker=".")
        df1.ObsConcLCL.plot(ax=axes[0], c="b", marker=".")

    # Apportionment plot 1
    ax = 0
    if calibration_flag == 'true':
        ax = 1
    # Data
    df1[APPORTIONMENT_COLS.values()].replace(0, np.NaN).plot.area(ax=axes[ax], lw=0)

    # Targets
    if target_flag == 'true':
        df1.TargetPoor.plot(ax=axes[ax], c="r", ls="--", alpha=0.5)
        df1.TargetMod.plot(ax=axes[ax], c="orange", ls="--", alpha=0.5)
        df1.TargetGood.plot(ax=axes[ax], c="g", ls="--", alpha=0.5)
        df1.TargetHigh.plot(ax=axes[ax], c="b", ls="--", alpha=0.5)

    ## Apportionment plot 2
    if out2:
        ax2 = 1
        if calibration_flag == 'true':
            ax2 = 2
        # Data
        df2[APPORTIONMENT_COLS.values()].replace(0, np.NaN).plot.area(ax=axes[ax2], lw=0)

        # Targets
        if target_flag == 'true':
            df2.TargetPoor.plot(ax=axes[ax2], c="r", ls="--", alpha=0.5)
            df2.TargetMod.plot(ax=axes[ax2], c="orange", ls="--", alpha=0.5)
            df2.TargetGood.plot(ax=axes[ax2], c="g", ls="--", alpha=0.5)
            df2.TargetHigh.plot(ax=axes[ax2], c="b", ls="--", alpha=0.5)

    # Compose title
    title_text = f"{DETERMINAND} "
    if calibration_flag == 'true':
        title_text += f"calibration (top) and "
    title_text += f"source apportionment for scenario {SCENARIO} "
    if out2:
        title_text += f"(middle) and {SCENARIO2} (bottom) "
    title_text += f"\n for reaches {df1.ReachNo.min()} to {df1.ReachNo.max()}"

    # Add title
    fig.suptitle(
        title_text,
        size=12,
        ha="center",
        y=0.98,
    )
    # NOTE Subtitles can be added with:
    # axes[0].set_title("Calibration")

    # Make sure axis starts at 0
    for n in range(num_plots):
        axes[n].set_ylim(bottom=0)

    # Axis labels
    for n in range(num_plots):
        axes[n].set_ylabel("Concentration (mg/L)")
    axes[n].set_xlabel("Distance (km)")

    # Activate legend
    if calibration_flag == 'true':
        axes[0].legend(
            labels=[
                "Sim. Mean",
                "Sim. Mean UCL",
                "Sim. Mean LCL",
                "Obs. Mean",
                "Obs. Mean UCL",
                "Obs. Mean LCL",
            ]
        )
    for n in range(ax, num_plots):
        axes[n].legend(ncol=2, loc=legend_loc)  # change to 'upper right' if needed

    # Annotations
    if annotate_flag == 'true':

        # Apply filter
        mask = (df1["DIFF_CONC"] > annotate_filter) & (df1.US_DS_Feat == "d-s")

        # Bespoke features to plot if input is not empty
        if annotate_features:
            mask2 = df1["FeatName"].isin(annotate_features)
            mask = mask | mask2

        # Draw labels
        # NOTE Could refactor this into a function
        count = 0
        max_conc = axes[ax].get_ylim()[1]
        for dis, row in df1[mask].iterrows():
            axes[ax].annotate(
                row.FeatName,
                xy=(dis, row.MeanConc),
                xycoords="data",
                xytext=(dis,
                        max_conc - 0.15 * max_conc * (count)),
                textcoords="data",
                va="top",
                ha="center",
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="k"),
                bbox=dict(boxstyle="square, pad=0.3", fc="1", ec="0.5", lw=1, alpha=0.5),
            )
            count += 1

        if out2:
            # Apply filter
            mask = (df2["DIFF_CONC"] > annotate_filter) & (df2.US_DS_Feat == "d-s")

            # Bespoke features to plot if input is not empty
            if annotate_features:
                mask2 = df2["FeatName"].isin(annotate_features)
                mask = mask | mask2

            # Draw labels
            count = 0
            max_conc = axes[ax2].get_ylim()[1]
            for dis, row in df2[mask].iterrows():
                axes[ax2].annotate(
                    row.FeatName,
                    xy=(dis, row.MeanConc),
                    xycoords="data",
                    xytext=(dis,
                            max_conc - 0.15 * max_conc * (count)),
                    textcoords="data",
                    va="top",
                    ha="center",
                    arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="k"),
                    bbox=dict(boxstyle="square, pad=0.3", fc="1", ec="0.5", lw=1, alpha=0.5),
                )
                count += 1

    # Custom annotations
    if custom_annotations:
        max_conc = axes[ax].get_ylim()[1]
        for label, dis in custom_annotations.items():
            for n in range(ax, num_plots):
                axes[n].axvline(dis, ls='--', color='grey')
                axes[n].annotate(
                    label.replace("'", ""),
                    xy=(dis, max_conc),
                    xycoords="data",
                    xytext=(dis,
                            max_conc - 0.05 * max_conc),
                    textcoords="data",
                    va="top",
                    ha="right",
                    rotation="vertical",
                    color='grey'
                    )

    # Make everything tidy
    plt.tight_layout()

    # Create Figures folder in project folder if it doesn't exist
    p = arcpy.mp.ArcGISProject("CURRENT")
    fig_folder = os.path.join(p.homeFolder, "Figures")
    if not os.path.exists(fig_folder):
        os.mkdir(fig_folder)

    # Save figure and show
    scenario_name = SCENARIO
    if out2:
        scenario_name += f"_{SCENARIO2}"
    fig_name = f"{DETERMINAND}_{scenario_name}_{df1.ReachNo.min()}_{df1.ReachNo.max()}.png"
    fig_path = os.path.join(fig_folder, fig_name)
    print(f"Created {fig_name}")
    plt.savefig(fig_path)
    plt.close()
