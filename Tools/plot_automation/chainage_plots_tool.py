"""
Library containing the main functions of the chainage plots tool
"""

import utilities

import importlib
importlib.reload(utilities)


def chainage_plots(params):
    """Main function to create the chainage plots"""

    # Retrieve parameters and transform as needed
    outputs_list_1 = params["outputs_list_1"].split(';')
    outputs_list_2 = params["outputs_list_2"]
    if outputs_list_2:
        outputs_list_2 = outputs_list_2.split(';')
    reaches_list = params["reaches_list"].split(';')

    # Loop through rivers and determinands
    for reach in reaches_list:
        if outputs_list_2:
            for out1, out2 in zip(outputs_list_1, outputs_list_2):
                utilities.plot_chainage_chart(out1, out2, reach, params)
        else:
            for out1 in outputs_list_1:
                utilities.plot_chainage_chart(out1, out2=None, reach=reach, params=params)
