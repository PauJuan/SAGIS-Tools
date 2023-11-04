"""
Python version of SIMCAT
"""

# TODO Read DATFILE as text file, line by line

# TODO Process all the sections:
# [0] Metadata at the top of the file
# [1] General - superseded
# [2] Determinands - short name and units, linked to features
# [3] Reaches - order (simno), id, name, waterbody, length, connectivity, velocity (alpha
# and beta), temperature, EQS targets (per det), decay rates (per det)
# [4] River Flow - dist type, params, linked to feature
# [5] River Quality - per determinand, dist type and params, linked to feature
# [6] Effluent Flow and Quality - flow and per det, dist type and
# params, linked to feature
# [7] River Quality Targets - superseded
# [8] Intermittent Discharges - superseded
# [9] Features - id, name, feat type, distance (km), coordinates (BNG)

# TODO Parse data from each section into Reaches and Features (as a dict)
dat_file = {
        "metadata" : {},
        "reaches": {
            "reach_id" : {
                "metadata" : {},
                "features" : {
                    "feature_id": {
                        "metadata": {},
                        "flow_params": {},
                        "wq_params": {},
                        }
                    }
                }
            }
        }

# TODO

# TODO

# TODO

# TODO

# TODO

# TODO

# TODO

# TODO

# TODO

# TODO

# TODO
