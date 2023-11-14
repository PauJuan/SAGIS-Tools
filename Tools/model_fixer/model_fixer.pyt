import arcpy

#DA Additional library to import
import importlib

#DA as keyword allows shorter names to be used
import convert_text_to_double, sim_features_fixer, check_unique, update_field_from_excel, normalise_reach_names, insert_field_from_excel

#DA .reload ensures any sub modules get reloaded when the current module is reloaded - ie refreshed in ArcGIS Pro
#DA no need to restart ArcGIS Pro
importlib.reload(convert_text_to_double)
importlib.reload(sim_features_fixer)
importlib.reload(check_unique)
importlib.reload(update_field_from_excel)
importlib.reload(normalise_reach_names)
importlib.reload(insert_field_from_excel)

#DA Need to set tool classes to new variables as for some reason if the line self.tools = [] contains '.' 
#DA the tool doesn't get imported into the toolbox
text_to_double = convert_text_to_double.ConvertTextToDouble
sim_features = sim_features_fixer.SimFeaturesFixer
check_unique_tool = check_unique.CheckUnique
update_field_tool = update_field_from_excel.UpdateFieldFromExcel
reach_names_tool = normalise_reach_names.NormaliseReachNames
insert_field_tool = insert_field_from_excel.InsertFieldFromExcel


class Toolbox(object):
    """Template for a toolbox and a tool"""
    def __init__(self):
        """Model Build toolbox"""
        self.label = "A toolbox with common editing features"

        #Alias name needs no spaces or special characters
        self.alias = "model_fixer"
        
        # List of tool classes associated with this toolbox
        self.tools = [text_to_double, check_unique_tool, update_field_tool, insert_field_tool]
