import arcpy
import os
import pandas as pd

import importlib


class CheckUnique(object):
    def __init__(self):
        """
        A tool to check if a field in a Table is unique
        """
        self.label = "Check field is unique"
        self.description = "Check field is unique"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        # Param 1
        table = arcpy.Parameter(
                displayName="table to check field",
                name="table",
                datatype="DETable",
                parameterType="Required",
                direction="Input",
                multiValue=False)

        # Param 2
        field = arcpy.Parameter(
                displayName="field to be checked",
                name="field",
                datatype="GPString",
                parameterType="Required",
                direction="Input",
                multiValue=False)

        # Create the parameters list
        params = [table, field]

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
        table = parameters[0].ValueAsText
        field = parameters[1].ValueAsText

        with arcpy.da.SearchCursor(table, field) as sCur:
            values = [val[0] for val in sCur]
            s = pd.Series(values)
            unique = s.is_unique
        if unique:
            arcpy.AddMessage(f"Field is unique")
        else:
            arcpy.AddWarning(f"Field is NOT unique")
            arcpy.AddMessage(f"There are a total of {s.duplicated().sum()} duplicated records")
            arcpy.AddMessage(f"The following records are duplicated:")
            arcpy.AddMessage(f"{s[s.duplicated()].unique()}")


