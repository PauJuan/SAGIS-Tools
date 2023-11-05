"""
Python version of SIMCAT
"""

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
        # TODO process_metadata

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
                    process_determinand_section(
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
            # Anything else
            elif section_start:
                section_lines.append(line)

        # Ensure that any remaining lines are processed
        if section_start:
            if section_start == "start_determinands":
                process_determinand_section(
                        section_lines, dat_file)
            elif section_start == "start_reaches":
                process_reaches_section(
                        section_lines, dat_file)


    except FileNotFoundError:
        print(f"The file '{file_path}' was not found.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def process_metadata(lines, dat_file):
    """
    Parse dat file metadata at the top of the file
    """
    for line in lines:
        print(f"Processing metadata section: {line}")


def process_determinand_section(lines, dat_file):
    """
    Parse determinand data (to populate decay and feature
    quality sections later)
    """
    for line in lines:
        print(f"Processing determinand section: {line}")


def process_reaches_section(lines, dat_file):
    """
    Parse reaches
    """
    for line in lines:
        print(f"Processing reaches section: {line}")


def process_river_flow_section(lines, dat_file):
    """
    Parse river flow using dataset code as key
    """
    for line in lines:
        print(f"Processing river flow section: {line}")


def process_river_quality_section(lines, dat_file):
    """
    Parse river quality using dataset code as key
    """
    for line in lines:
        print(f"Processing river quality section: {line}")


def process_effluent_section(lines, dat_file):
    """
    Parse effluent flow and quality using dataset code as key
    """
    for line in lines:
        print(f"Processing effluent section: {line}")


def process_features_section(lines, dat_file):
    """
    Parse features and assing flow and quality data
    """
    for line in lines:
        print(f"Processing features section: {line}")


# Process dat file
process_dat_file_lines(file_path, config, DatFile)

