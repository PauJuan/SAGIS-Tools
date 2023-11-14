import arcpy


def convert_field_type(table, field, field_type):
    """
    A simple function to change a field type
    """
    placeholder = field + '_2'
    arcpy.AddField_management(table, placeholder, field_type)
    arcpy.CalculateField_management(table, placeholder,
                                    '!{}!'.format(field), 'PYTHON3')
    arcpy.DeleteField_management(table, field)
    arcpy.AlterField_management(table, placeholder,
                                new_field_name=field, new_field_alias=field)
