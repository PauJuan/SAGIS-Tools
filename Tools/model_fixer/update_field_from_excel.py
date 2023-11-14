import arcpy
import os
import pandas as pd

import importlib


class UpdateFieldFromExcel(object):
    def __init__(self):
        """
        A tool that takes an ID and data fields from an Excel file and uses them
        to update a table
        """
        self.label = "Update Field from Table"
        self.description = "Update field from table"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        # Param 1
        fc = arcpy.Parameter(
                displayName="feature class",
                name="fc",
                datatype="DEFeatureClass",
                parameterType="Required",
                direction="Input",
                multiValue=False)

        # Param 2
        excel = arcpy.Parameter(
                displayName="Excel file with data",
                name="excel",
                datatype="DEFile",
                parameterType="Required",
                direction="Input",
                multiValue=False)

        # Param 3
        id_field = arcpy.Parameter(
                displayName="Name of field to use as ID",
                name="id_field",
                datatype="GPString",
                parameterType="Required",
                direction="Input",
                multiValue=False)

        # Param 4
        data = arcpy.Parameter(
                displayName="Name of fields with data",
                name="data",
                datatype="GPString",
                parameterType="Required",
                direction="Input",
                multiValue=True)

        # Create the parameters list
        params = [fc, excel, data, id_field]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        excel = parameters[1].ValueAsText
        data = parameters[2]
        id_field = parameters[3]

        if os.path.exists(excel):
            data.filter.list = pd.read_excel(excel).columns.to_list()

        if data.ValueAsText:
            id_field.filter.list = data.ValueAsText.split(";")

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """
        """
        fc = parameters[0].ValueAsText
        excel = parameters[1].ValueAsText
        data = parameters[2].ValueAsText.split(";")
        id_field = parameters[3].ValueAsText

        # Read excel and index per ID field
        df = pd.read_excel(excel)
        data.insert(0, data.pop(data.index(id_field)))  # Bring id field to beginning
        df = df[data].set_index(id_field)

        # Open Update cursor and update field from dictionary
        with arcpy.da.UpdateCursor(fc, data) as uCur:
            for row in uCur:
                try:
                    values = df.loc[row[0]].values
                    row[1:] = values
                    uCur.updateRow(row)
                except KeyError:
                    continue
