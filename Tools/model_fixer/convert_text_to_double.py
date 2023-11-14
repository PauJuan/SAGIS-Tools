import arcpy
import os
import converters as cvs


class ConvertTextToDouble(object):
    def __init__(self):
        """
        A tool to convert fields from text to double
        """
        self.label = "Text field to double field tool"
        self.description = "Text field to double field tool"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        # Param 1
        table = arcpy.Parameter(
                displayName="table with fields to be modified",
                name="table",
                datatype="DETable",
                parameterType="Required",
                direction="Input",
                multiValue=False)

        # Param 2
        fields = arcpy.Parameter(
                displayName="Fields to be modified",
                name="fields",
                datatype="Field",
                parameterType="Required",
                direction="Input",
                multiValue=True)

        # Create the parameters list
        params = [table, fields]

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
        fields = parameters[1].ValueAsText.split(";")
        for field in fields:
            cvs.convert_field_type(table, field, "Double")
