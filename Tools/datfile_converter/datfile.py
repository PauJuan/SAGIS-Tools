"""
The main object to hold the dat file data
"""

    # [3] Reaches - order (simno), id, name, waterbody, length, connectivity,
    # velocity (alpha and beta), temperature, EQS targets (per det), decay rates (per det)
    # [4] River Flow - dist type, params, linked to feature
    # [5] River Quality - per determinand, dist type and params, linked to feature
    # [6] Effluent Flow and Quality - flow and per det, dist type and params, linked to feature
    # [7] River Quality Targets - superseded
    # [8] Intermittent Discharges - superseded
    # [9] Features - id, name, feat type, distance (km), coordinates (BNG)

# Create data structures to hold the dat file info
DatFile = {
        "metadata" : {
            "Flow Calibration Table": "",
            "WQ Calibration Table": "",
            "Regional Database Location": "",
            "Common Database Location":  "",
            "SAGIS Project Location": "",
            "SAGIS Build No": "",
            "Created by": "",
            "DAT File Creation Date": "",
            },
        "reaches": {
            # "reach_id": Reach
            }
        }

# Reach = {
#         "metadata": {},
#         "flow_params": {},
#         "wq_params" {},
#         "features": {
#             # "feature_id": Feature
#             }
#         }

# Feature = {
#         "metadata": {},
#         "flow_params": {},
#         "wq_params": {},
#         }

config = {
        # "File": {
        #     "start": "=======================================================================",
        #     "end": "======================================================================="
        #     },
        "Determinands": {
            "start": "========b===========c======d====e====f=====g====h=====i===j====k==l===m=",
            "end": "*************** indicator of end of the determinand data ***********"
            },
        "Reaches": {
            "start": "=========b===================c====d====e====f====g====h===i===j=====",
            "end": "***************** indicator of end of Reach data *******************"
            },
        "RiverFlow": {
            "start": "===========c========d========e=========f============g===============",
            "end": "***************** indicator of end of river flow data **************"
            },
        "RiverQuality": {
            "start": "=======b=c====d======e=====f========g====h=======i==================",
            "end": "***************** indicator of end of river quality data *********"
            },
        "Effluent": {
            "start": "======b=c=========d========e=====f========g===h=====i==================",
            "end": "************ indicator of end of effluent flow and quality data ******"
            },
        "Features": {
            "start": "===========a=================================b====c====d=====e====f====g===h=i==j===",
            "end": "***************** indicator of end of data *********"
            }
        }
