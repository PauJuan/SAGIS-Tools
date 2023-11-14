import arcpy
import os
import pandas as pd

import importlib


class InsertFieldFromExcel(object):
    def __init__(self):
        """
        A tool that takes an ID and data fields from an Excel file and uses them
        to insert fields in a table
        """
        self.label = "Insert Field from Table"
        self.description = "Insert field from table"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        # Param 1
        fc = arcpy.Parameter(
                displayName="feature class",
                name="fc",
                datatype="DETable",
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
        sheet = arcpy.Parameter(
                displayName="Sheet",
                name="sheet",
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
        params = [fc, excel, sheet, data]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        excel = parameters[1].ValueAsText
        sheet = parameters[2]
        data = parameters[3]

        if os.path.exists(excel):
            sheet.filter.list = pd.ExcelFile(excel).sheet_names

        if os.path.exists(excel):
            if sheet.ValueAsText:
                data.filter.list = pd.read_excel(
                        excel,
                        sheet_name=sheet.ValueAsText
                        ).columns.to_list()

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
        sheet = parameters[2].ValueAsText
        data = parameters[3].ValueAsText.split(";")

        # Read excel and index per ID field
        df = pd.read_excel(excel, sheet_name=sheet)
        df = df[data]

        # Open Update cursor and update field from dictionary
        with arcpy.da.InsertCursor(fc, data) as iCur:
            for row in df.iterrows():
                arcpy.AddMessage(f"{row[1].values}")
                arcpy.AddMessage(f"{data}")
                iCur.insertRow(list(row[1].values))
