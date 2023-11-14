import arcpy
import os
import converters as cvs

import importlib
importlib.reload(cvs)


SIM_FEATURES_FIELD_TYPES = {
        "DETCODE_Q*": "String",
        "SAMPLES_Q*": "Integer",
        "DIST_Q*": "Integer",
        "MEAN_Q*": "Double",
        "SD_Q*": "Double",
        "SHIFT_Q*": "Double",
        "CORR_Q*": "Double",
        }


class SimFeaturesFixer(object):
    def __init__(self):
        """
        A tool to check for common field formatting errors in SimFeatures and
        fix them automatically
        """
        self.label = "SimFeatures Format Fixer"
        self.description = "SimFeatures Format Fixer"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        # Param 1
        simFeatures = arcpy.Parameter(
                displayName="SimFeatures feature class",
                name="simFeatures",
                datatype="DEFeatureClass",
                parameterType="Required",
                direction="Input",
                multiValue=False)

        # Create the parameters list
        params = [simFeatures]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """
        """
        simFeatures = parameters[0].ValueAsText
        for field_name, field_type in SIM_FEATURES_FIELD_TYPES.items():
            fields = arcpy.ListFields(simFeatures, field_name)
            for field in fields:
                arcpy.AddMessage(f"Checking field {field.name}")
                if field.type != field_type:
                    cvs.convert_field_type(simFeatures, field.name, field_type)
                    arcpy.AddMessage(f"Incorrect field format for {field.name}. Correcting...")

        arcpy.AddMessage("Finished revising all fields in SimFeatures")
