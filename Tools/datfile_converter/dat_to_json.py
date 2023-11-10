"""
Python version of SIMCAT
"""

import re
import json
from datfile import DatFile, config  # Main dict to contain data and config file

file_path = "EXAMPLE.dat"


def process_dat_file_lines(file_path, config, dat_file):
    """
    Process all the sections:
    [0] Metadata at the top of the file
    [1] General - superseded
    [2] Determinands - short name and units, linked to features
    [3] Reaches - order (simno), id, name, waterbody, length, connectivity,
    velocity (alpha and beta), temperature, EQS targets (per det), decay rates (per det)
    [4] River Flow - dist type, params, linked to feature
    [5] River Quality - per determinand, dist type and params, linked to feature
    [6] Effluent Flow and Quality - flow and per det, dist type and params,
    linked to feature
    [7] River Quality Targets - superseded
    [8] Intermittent Discharges - superseded
    [9] Features - id, name, feat type, distance (km), coordinates (BNG)
    """
    # Open DAT file for reading
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Process metadata section at the top
        process_metadata(lines, dat_file)

        # Initialize variables to track section boundaries
        section_start = None
        section_end = None

        # Iterate through the lines
        for line in lines:

            # Determinands
            if config["Determinands"]["start"] in line:
                section_start = "start_determinands"
                section_lines = []
            elif config["Determinands"]["end"] in line:
                section_end = "end_determinands"
                if section_start and section_end:
                    det_units_dict = process_determinand_section(
                            section_lines, dat_file)
                    section_start = section_end = None

            # Reaches
            elif config["Reaches"]["start"] in line:
                section_start = "start_reaches"
                section_lines = []
            elif config["Reaches"]["end"] in line:
                section_end = "end_reaches"
                if section_start and section_end:
                    process_reaches_section(
                            section_lines, dat_file)
                    section_start = section_end = None

            # River flow
            elif config["RiverFlow"]["start"] in line:
                section_start = "start_river_flow"
                section_lines = []
            elif config["RiverFlow"]["end"] in line:
                section_end = "end_river_flow"
                if section_start and section_end:
                    flow_data = process_river_flow_section(
                            section_lines, dat_file)
                    section_start = section_end = None

            # River quality
            elif config["RiverQuality"]["start"] in line:
                section_start = "start_river_quality"
                section_lines = []
            elif config["RiverQuality"]["end"] in line:
                section_end = "end_river_quality"
                if section_start and section_end:
                    wq_data = process_river_quality_section(
                            section_lines, dat_file)
                    section_start = section_end = None

            # Effluent
            elif config["Effluent"]["start"] in line:
                section_start = "start_effluent"
                section_lines = []
            elif config["Effluent"]["end"] in line:
                section_end = "end_effluent"
                if section_start and section_end:
                    eff_data = process_effluent_section(
                            section_lines, dat_file)
                    section_start = section_end = None

            # Features
            elif config["Features"]["start"] in line:
                section_start = "start_features"
                section_lines = []
            elif config["Features"]["end"] in line:
                section_end = "end_features"
                if section_start and section_end:
                    process_features_section(
                            section_lines, dat_file, flow_data, wq_data, eff_data)
                    section_start = section_end = None

            # Anything else add lines to be processed
            elif section_start:
                section_lines.append(line)

    except FileNotFoundError:
        print(f"The file '{file_path}' was not found.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def process_metadata(lines, dat_file):
    """
    Parse dat file metadata at the top of the file
    """
    for line in lines[1:10]:
        name = line.split(": ")[0].strip("=").strip()
        value = line.split(": ")[1].strip()
        dat_file["metadata"][name] = value


def process_determinand_section(lines, dat_file):
    """
    Parse determinand data (to populate decay and feature
    quality sections later)
    """
    det_units_dict = {}
    for line in lines:
        name, short_name, units = re.findall(r"'(.*?)'", line)
        det_units_dict[short_name] = units

    # Return dictionary to use data later
    return det_units_dict


def process_reaches_section(lines, dat_file):
    """
    Parse reaches
    [3] Reaches - order (simno), id, name, waterbody, length, connectivity,
    velocity (alpha and beta), temperature, EQS targets (per det), decay rates (per det)
    """
    # Use count to separate reach data from decay, standards, etc
    count = 0
    for line in lines:
        # Clean spaces
        line = line.strip()
        # TODO Need to implement logic to read in Standards
        if line.startswith("'Standard'"):
            continue
        elif count == 1:
            decay_rates = re.split(r"\s{2,}", line)
            reach["decay_rates"] = decay_rates
            # Add features at the end
            reach["features"] = {}
            count = 0
        elif count == 0:
            # Retrieve data
            simno, name, length, conn1, conn2, conn3 , flow_code, wq_code, alpha, \
            beta, wbid, unique_ref = re.split(r"\s{2,}", line)
            # Create reach
            dat_file["reaches"][simno] = {}
            reach = DatFile["reaches"][simno]
            # Populate
            reach["name"] = name.strip("''")
            reach["unique_ref"] = unique_ref.strip()
            reach["wbid"] = wbid.strip("'")
            reach["length"] = length
            reach["connectivity"] = (conn1, conn2, conn3)
            reach["flow_data"] = flow_code
            reach["wq_data"] = wq_code
            reach["velocity"] = (alpha, beta)
            # Increase count
            count += 1


def process_river_flow_section(lines, dat_file):
    """
    Parse river flow using dataset code as key
    [4] River Flow - dist type, params, linked to feature
    """
    flow_data = {}
    for line in lines:
        pass
        # TODO use code as key and retrieve data in simple manner
        code, XXX = re.split(r"\s{2,}", line)
        flow_data[code] = {
            "dist": dist,
            ""
                }

    # Return dictionary to use data later
    return flow_data


def process_river_quality_section(lines, dat_file):
    """
    Parse river quality using dataset code as key
    [5] River Quality - per determinand, dist type and params, linked to feature
    """
    wq_data = {}
    for line in lines:
        # print(f"Processing river quality section: {line}")
        pass
        # TODO use code as key, det dict (need to add to func arguments) to
        # count determinands, and retrieve data in simple manner

    # Return dictionary to use data later
    return wq_data


def process_effluent_section(lines, dat_file):
    """
    Parse effluent flow and quality using dataset code as key
    [6] Effluent Flow and Quality - flow and per det, dist type and params,
    linked to feature
    """
    eff_data = {}
    for line in lines:
        # print(f"Processing effluent section: {line}")
        pass
        # TODO use code as key, det dict (need to add to func arguments) to
        # count determinands (on top of flow), and retrieve data in simple manner

    # Return dictionary to use data later
    return eff_data


def process_features_section(lines, dat_file, flow_data, wq_data, eff_data):
    """
    Parse features and assing flow and quality data
    [9] Features - id, name, feat type, distance (km), coordinates (BNG)
    """
    for line in lines:
        # print(f"Processing features section: {line}")
        pass
        # TODO Use Reach number to retrieve reach, replace flow and wq codes by
        # data, add new feature, populate with data (using effluent data when
        # necessary)


    # TODO Loop through reaches and features and substitute flow and wq codes by
    # values


# Process dat file
process_dat_file_lines(file_path, config, DatFile)

# Export as json
with open("EXAMPLE.json", "w") as outfile:
    json.dump(DatFile, outfile, indent=4, sort_keys=False)
