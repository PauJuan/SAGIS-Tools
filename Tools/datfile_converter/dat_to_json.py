"""
Python version of SIMCAT
"""

# TODO Many of the values should be numerical but are being appended as text
# TODO Need to strip quotes from string values
# TODO Add functionality to handle gis coordinates as lat/long
# TODO Add determinands section in metadata
# TODO General review of how the values are stored

import re
import json
import yaml
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
                            section_lines, dat_file, det_units_dict)
                    section_start = section_end = None

            # Effluent
            elif config["Effluent"]["start"] in line:
                section_start = "start_effluent"
                section_lines = []
            elif config["Effluent"]["end"] in line:
                section_end = "end_effluent"
                if section_start and section_end:
                    eff_data = process_effluent_section(
                            section_lines, dat_file, det_units_dict)
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
                section_lines.append(line.strip())

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
    count = 1
    for line in lines:
        name, short_name, units = re.findall(r"'(.*?)'", line)
        det_units_dict[str(count)] = {
                "name": name,
                "short_name": short_name,
                "units": units
                }
        count += 1

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
            reach["connectivity"] = {
                    "conn1": conn1,
                    "conn2": conn2,
                    "conn3": conn3
                    }
            reach["flow_data"] = flow_code
            reach["wq_data"] = wq_code
            reach["velocity"] = {
                    "alpha": alpha,
                    "beta": beta
                    }
            # Increase count
            count += 1


def process_river_flow_section(lines, dat_file):
    """
    Parse river flow using dataset code as key
    [4] River Flow - dist type, params, linked to feature
    """
    flow_data = {}
    for line in lines:

        if ".npd" in line:
            code, dist, npd_filename, corr, _ = re.split(r"\s{2,}", line)
            flow_data[code] = {
                    "dist": dist,
                    "npd_filename": npd_filename,
                    "corr": corr
                    }
        else:
            code, dist, mean_flow, low_95th_flow, shift_flow, corr, _ = re.split(r"\s{2,}", line)
            flow_data[code] = {
                    "dist": dist,
                    "mean_flow": mean_flow,
                    "low_95th_flow": low_95th_flow,
                    "shift_flow": shift_flow,
                    "corr": corr
                    }

    # Return dictionary to use data later
    return flow_data


def process_river_quality_section(lines, dat_file, det_units_dict):
    """
    Parse river quality using dataset code as key
    [5] River Quality - per determinand, dist type and params, linked to feature
    """
    wq_data = {}
    for line in lines:

        parts = re.split(r"\s{2,}", line)
        code, det_code = parts[0], parts[1]
        det_name = det_units_dict[det_code]["short_name"]

        # Initialise for first determinand
        if det_code == '1':
            wq_data[code] = {}

        if len(parts) > 9:
            # Power function
            code, det_code, dist, mean_conc, std, power_idx, base_conc, \
            cut_off_pc, corr, sample_n, _ = parts

            wq_data_det = wq_data[code]
            wq_data_det[det_name] = {
                    "dist": dist,
                    "mean_conc": mean_conc,
                    "std": std,
                    "power_idx": power_idx,
                    "base_conc": base_conc,
                    "cut_off_pc": cut_off_pc,
                    "corr": corr,
                    "sample_n": sample_n
                    }

        else:
            code, det_code, dist, mean_conc, std, shift_conc, corr, sample_n, _ = parts

            wq_data_det = wq_data[code]
            wq_data_det[det_name] = {
                    "dist": dist,
                    "mean_conc": mean_conc,
                    "std": std,
                    "shift_conc": shift_conc,
                    "corr": corr,
                    "sample_n": sample_n
                    }

    # Return dictionary to use data later
    return wq_data


def process_effluent_section(lines, dat_file, det_units_dict):
    """
    Parse effluent flow and quality using dataset code as key
    [6] Effluent Flow and Quality - flow and per det, dist type and params,
    linked to feature
    """
    eff_data = {}
    for line in lines:

        parts = re.split(r"\s{2,}", line)
        code, det_code = parts[0], parts[1]
        if det_code == '0':
            det_name = "Flow"
        else:
            det_name = det_units_dict[det_code]["short_name"]

        # Initialise for first line (flow)
        if det_code == '0':
            eff_data[code] = {}

        # Check for NPD files
        if ".npd" in line:
            code, dist, npd_filename, shift, corr, sample_n, *_ = re.split(r"\s{2,}", line)

            eff_data_det = eff_data[code]
            eff_data_det[det_name] = {
                    "dist": dist,
                    "npd_filename": npd_filename,
                    "shift": shift_conc,
                    "corr": corr,
                    "sample_n": sample_n
                    }

        else:
            code, det_code, dist, mean_conc, std, shift_conc, corr, sample_n, _ = parts

            eff_data_det = eff_data[code]
            eff_data_det[det_name] = {
                    "dist": dist,
                    "mean_conc": mean_conc,
                    "std": std,
                    "shift_conc": shift_conc,
                    "corr": corr,
                    "sample_n": sample_n
                    }

    # Return dictionary to use data later
    return eff_data


def process_features_section(lines, dat_file, flow_data, wq_data, eff_data):
    """
    Parse features and assing flow and quality data
    [9] Features - id, name, feat type, distance (km), coordinates (BNG)
    """
    for line in lines:
        if "WBID:" in line:
            pass
            # TODO Populate reach flow and wq data

        else:
            parts = re.split(r"\s{2,}", line)
            # Handle names with spaces
            if len(parts) > 10:
                parts = [parts[0] + " " + parts[1]] + parts[2:]

            name, code, simno, dist_head, flow_code, wq_code, _, _, _, giscode = parts
            reach = dat_file["reaches"][simno]

            # TODO Need to add logic to handle data based on feature type

            # Retrieve feature flow and quality data
            try:
                feature_flow_data = flow_data[flow_code]
            except KeyError:
                feature_flow_data = None

            try:
                feature_wq_data = wq_data[wq_code]
            except KeyError:
                feature_wq_data = None

            try:
                effluent_data = eff_data[wq_code]
            except KeyError:
                effluent_data = None

            reach["features"][name] = {
                    "feat_code": code,
                    "dist_head": dist_head,
                    "flow_data": feature_flow_data,
                    "wq_data": feature_wq_data,
                    "giscode": giscode,
                    }

# Process dat file
process_dat_file_lines(file_path, config, DatFile)

# Export as json and yaml
jsonfile = "EXAMPLE.json"
yamlfile = "EXAMPLE.yaml"

with open(jsonfile, "w") as outfile:
    json.dump(DatFile, outfile, indent=4, sort_keys=False)
# with open(jsonfile) as outfile:
#     d = json.load(outfile)
with open(yamlfile, "w") as outfile:
    yaml.dump(DatFile, outfile, allow_unicode=True)
