import arcpy
import os


class NormaliseReachNames(object):
    def __init__(self):
        """
        A tool to remove commas and forbidden characters from reach names
        """
        self.label = "SimReaches names fixer"
        self.description = "SimReaches names fixer"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        # Param 1
        simReaches = arcpy.Parameter(
                displayName="simReaches feature class",
                name="simReaches",
                datatype="DEFeatureClass",
                parameterType="Required",
                direction="Input",
                multiValue=False)

        # Create the parameters list
        params = [simReaches]

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
        arcpy.AddMessage("Checking for commas in reach names")

        simReaches = parameters[0].ValueAsText
        with arcpy.da.UpdateCursor(simReaches, ["SIMNAME"]) as uCur:
            for row in uCur:
                name = row[0]
                if "," in name:
                    arcpy.AddWarning(f"Removing commas from reach name: {name}")
                    row = [name.replace(",", "")]
                    uCur.updateRow(row)

        arcpy.AddMessage("Finished revising all names in SimReaches")
