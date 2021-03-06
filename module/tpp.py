# -----------------------------------------------------------------------------
# Author:      Texas Department of Transportation (TPP)
#
# Licence:  The MIT License (MIT)
# Copyright (C) 2014 TxDOT
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# -----------------------------------------------------------------------------

def txArchive():
    """
    Create an archive of your MyModules script and push the working script
    to the main folder.
    """
    import os
    import time
    import shutil

    directory = "C:\\DATAMGT\\Scripts\\MyModules"
    workingCopy = "C:\\DATAMGT\\Scripts\\MyModules\MyModules_WorkingCopy.py"
    archiveTime = str(time.localtime()[2]) + str(time.localtime()[1]) + \
        str(time.localtime()[0]) + "_" + \
        str(time.localtime()[3]) + str(time.localtime()[4])
    archive = (directory + os.sep + "Archive" + archiveTime + ".py")
    MyModulesMain = "C:\\Python26\\ArcGIS10.0\\Lib\\site-packages\MyModules.py"
    shutil.copyfile(MyModulesMain, archive)
    shutil.copyfile(workingCopy, MyModulesMain)
    del directory
    del workingCopy
    del archiveTime
    del archive


def fileChecklist(directory, extension='All'):
    """
    Create a checklist file in "txt" format for any folder - list all files
    by name.
    """
    import os

    checkFile = directory + os.sep + 'Checklist.txt'
    file1 = open(checkFile, "w")
    dirList = os.listdir(directory)
    for fname in dirList:
        if extension == 'All':
            file1.write(str(fname) + "\n")
        else:
            if fname.endswith(extension):
                file1.write(str(fname) + "\n")
    file1.close()
    print 'Done!'


def projectMenu():
    """
    Through a defined menu, allows a user to select a project category,
    create a new folder, and optionally add a project plan document.
    """
    import os
    import shutil
    import time
    # Determine project type and location
    ansMenu = raw_input(
        "What type of project are you creating?\n\n 1 - Data Transmittal\n\
         2 - Minute Order\n 3 - Special Map\n 4 - Training Map\n\
         5 - Other Location\n\nEnter Selection: ")
    if ansMenu == '1':
        tmYR = str(time.localtime()[0])
        path = ("T:\\DATAMGT\MAPPING\\Data Transmittals" + os.sep + tmYR)
    elif ansMenu == '2':
        tmYR = str(time.localtime()[0])
        path = ("T:\\DATAMGT\\MAPPING\\Special Maps" + os.sep + tmYR +
                "\\Minute Orders")
        moType = raw_input(
            "\nWhat's the intent of the Minute Order?\n\n 1 - New Designation\n\
             2 - Re-Designation\n 3 - Proposed Highway\n\
             4 - Removal\n\nEnter Selection: ")
        if moType == '1':
            moChange = "New Designation"
        if moType == '2':
            moChange = "Re-Designation"
        if moType == '3':
            moChange = "Proposed Highway"
        if moType == '4':
            moChange = "Removal"
    elif ansMenu == '3':
        tmYR = str(time.localtime()[0])
        path = ("T:\\DATAMGT\\MAPPING\\Special Maps" + os.sep + tmYR)
    elif ansMenu == '4':
        path = "T:\\DATAMGT\\MAPPING\\Training"
    else:
        path = raw_input("\nWhat is the filepath of your working directory?\
                          \n\nPath: ")
    # Name the project
    projName = raw_input("\nWhat is the project name?: ")
    # Ask for a project plan
    ansPlan = raw_input("\nWould you like to include a project plan? \
                         \n\nY or N: ")
    # Create folder directory
    folderPDF = (path + os.sep + projName + os.sep + "PDF")
    folderGeoData = (path + os.sep + projName + os.sep + "Geographic Data")
    folderScripts = (path + os.sep + projName + os.sep + "Scripts")
    folderMaps = (path + os.sep + projName + os.sep + "Maps")
    folderDoc = (path + os.sep + projName + os.sep + "Documentation")
    # Change the location of the Project Template here:
    projTemp = "T:\\DATAMGT\\MAPPING\\Personal Folders\\David H\
                \\Scripts\\ProjectTemplate.doc"
    newProjPlan = (folderDoc + os.sep + projName + ".doc")
    folderList = [folderPDF, folderGeoData,
                  folderScripts, folderMaps, folderDoc]
    for x in folderList:
        if not os.path.exists(x):
            os.makedirs(x)
    if ansPlan is 'Y':
        shutil.copyfile(projTemp, newProjPlan)
    else:
        pass
    print " "
    projDirectory = (path + os.sep + projName)
    print projDirectory
    # Open the file directory in Windows Explorer
    os.startfile(projDirectory)
    # Modify or create (if not existing) a general log file
    # for all logged projects
    # Change the location of the general log file here:
    logFile = "T:\\DATAMGT\\MAPPING\\Personal Folders\\David H\\Scripts\
               \\ProjectLogFile.txt"
    # Collect user name information
    userName = (os.path.expanduser("~/"))[9:16]
    # Record directory creation in general log
    with open(logFile, "a") as log:
        log.write("\n" + time.ctime() + ", " + userName + ", " +
                  projName + ", " + projDirectory)
    # Create a log file specifically for minute orders
    # Change the location of the Minute Order log file here:
    moLogFile = "T:\\DATAMGT\\MAPPING\\Personal Folders\\David H\
                 \\Scripts\\MinuteOrderProjectLogFile.txt"
    # Log minute order specifics into Minute Order log file
    with open(moLogFile, "a") as log:
        log.write("\n" + time.ctime() + ", " + moChange + ", "
                  + userName + ", " + projName + ", " + projDirectory)


def archiveComanche(output_path, db_connection):
    """
    Argument is local output path
    Args:
        output_path (str): Full path to the output folder
        db_connection
    """
    from arcpy import env
    import arcpy
    import os
    import time

    exportTime = time.ctime()
    exportTimeElements = exportTime.split(" ")
    formatTime = ""

    for element in exportTimeElements:
        if ":" in element:
            element = element.replace(":", "_")
        formatTime = formatTime + "_" + element

    env.workspace = db_connection

    outputWorkspace = output_path

    print "Creating New File Geodatabase..."
    arcpy.CreateFileGDB_management(outputWorkspace, "Archive" + formatTime,
                                   "10.0")
    outputPath = outputWorkspace + "Archive" + formatTime + ".gdb"

    copyFiles = ["TPP_GIS.APP_TPP_GIS_ADMIN.Roadways\\TPP_GIS.APP_TPP_GIS_ADMIN.TXDOT_Roadways",
                 "TPP_GIS.APP_TPP_GIS_ADMIN.RTE_CONCURRENT",
                 "TPP_GIS.APP_TPP_GIS_ADMIN.RTE_CONTROL_SECTION",
                 "TPP_GIS.APP_TPP_GIS_ADMIN.SUBFILES"]

    for file in copyFiles:
        if file == "TPP_GIS.APP_TPP_GIS_ADMIN.Roadways\\TPP_GIS.APP_TPP_GIS_ADMIN.TXDOT_Roadways":
            fileName = file.split(".")[4]
            print "Exporting " + fileName
            outFC = outputPath + os.sep + fileName
            arcpy.CopyFeatures_management(file, outFC)
        else:
            fileName = file.split(".")[2]
            print "Exporting " + fileName
            outFC = outputPath + os.sep + fileName
            arcpy.CopyRows_management(file, outFC)

    print "Archive Complete..."


def rte_concatenate(table, group_field="RTE_ID", from_field="FROM_DFO",
                    to_field="TO_DFO", concatenate_field_name="CONCAT",
                    mark_overlap=True, overlap_field_name="OVERLAPS"):
    """
    Adds a field for route concatenate and populates a concatenation index.
    This value marks records that belong to the same linear segment.
    Optionally, checks for overlapping measures.

    Example 1:
    rte_concatenate("C:\\Test.gdb\\test")

    Example 2:
    rte_concatenate("C:\\Test.gdb\\test", "Route_ID", "FRM_Mea",
        "TO_Mea", "Concat", True, "Overlap")

    Args:
        table_name (str): Full path to the route table

        group_field (str, optional): Field name containing field for
        concatenation ("RTE_ID","C_SEC"); default: "RTE_ID"

        from_field (str, optional): Field name containing from measure;
        default: "FROM_DFO"

        to_field (str, optional): Field name containing to measure;
        default: "TO_DFO"

        concatenate_field_name (str, optional): Specify custom name for
        concatenate field; default: "CONCAT"

        mark_overlap (boolean, optional): Mark if the measures are overlapping;
        default: True

        overlap_field_name (str, optional): Specify custom name for concatenate
        field; default: "RTE_OVERLAP"
    """

    # Import arcpy module
    import arcpy
    import time
    import os

    # Establish start time
    start_time = time.time()

    # Create table in memory
    output_dir_path = os.path.dirname(table)
    output_table_name = os.path.basename(table) + "_RTE_CONCATENATE"
    output_table = os.path.join(output_dir_path, output_table_name)

    # Create temp table
    temp_table = "in_memory//" + output_table_name
    arcpy.TableSelect_analysis(table, temp_table)

    # Create field list to check that valid field exists
    field_list = arcpy.ListFields(temp_table)
    add_field_list = [concatenate_field_name, "RC_UNIQUE"]

    # Add field for marking overlap if specified by user
    if mark_overlap is True:
        add_field_list.append(overlap_field_name)

    # Iterate through table, checking if the add field already exist
    for field in field_list:
        if field.name == concatenate_field_name:
            add_field_list.remove(concatenate_field_name)
        elif field.name == overlap_field_name and mark_overlap is True:
            add_field_list.remove(overlap_field_name)
    del field_list

    # If valid field does not exist, add the field
    if len(add_field_list) == 0:
        pass
    else:
        for field in add_field_list:
            print "Adding Field: {0}".format(field)
            arcpy.AddField_management(temp_table, field, "LONG")

    # Create update cursor to populate the concatenation value
    sort_string = str("{0} A; {1} A".format(group_field, from_field))
    fields_subset = "[group_field, from_field, to_field, concatenate_field_name,\
                      overlap_field_name]"
    rows = arcpy.UpdateCursor(temp_table, "", "", fields_subset, sort_string)
    row = rows.next()

    # Create baseline variables
    previous = ""
    previous_to = ""
    previous_unique_id = ""
    counter = 0
    concatenate_index = 1

    # Create Empty List to hold overlaps
    overlap_list = []

    # begin cursor
    while row:
        current = row.getValue(group_field)
        current_from = row.getValue(from_field)
        current_to = row.getValue(to_field)

        # Populate Unique ID field
        unique_id = counter + 1
        row.RC_UNIQUE = unique_id

        # Sets initial values for the first record in the table
        if counter == 0:
            row.setValue(concatenate_field_name, concatenate_index)
            row.setValue(overlap_field_name, 0)

        # Marks a records as belonging to the same segment as previous
        elif previous == current and previous_to >= current_from:
            row.setValue(concatenate_field_name, concatenate_index)
            if mark_overlap is True:
                if previous_to > current_from:
                    row.setValue(overlap_field_name, previous_unique_id)
                    overlap_list.append((previous_unique_id, unique_id))
                else:
                    row.setValue(overlap_field_name, 0)

        # Marks the first record of a new segment in the same route
        elif previous == current and previous_to < current_from:
            concatenate_index += 1
            row.setValue(concatenate_field_name, concatenate_index)
            row.setValue(overlap_field_name, 0)

        # Marks the first record of a new route
        else:
            concatenate_index = 1
            row.setValue(concatenate_field_name, concatenate_index)
            row.setValue(overlap_field_name, 0)

        # Sets the current records as previous for the next row
        previous = current
        previous_to = current_to
        previous_unique_id = unique_id

        # Saves changes to the current row and get the next row object
        rows.updateRow(row)
        row = rows.next()

        # Increment's counter value and print progress feedback
        counter += 1
        print counter

    del row, rows

    if mark_overlap is True:
        print "Completing Overlap Processing..."
        rows = arcpy.UpdateCursor(temp_table)

        for row in rows:
            unique_id = row.RC_UNIQUE
            for item in overlap_list:
                if item[0] == unique_id:
                    row.setValue(overlap_field_name, item[1])
                    rows.updateRow(row)

    # Write out temp_table
    arcpy.CopyRows_management(temp_table, output_table)

    # Delete out from memory
    arcpy.Delete_management(temp_table)
    del temp_table, table, overlap_list, overlap_field_name, row, rows

    end_time = time.time()
    print "Elapsed time: {0}".format(time.strftime('%H:%M:%S',
                                     time.gmtime(end_time - start_time)))


def rte_order(rteTable, rteIDField, frmMeasField, orderField='RTE_ORDER'):
    """
    Adds segment order index by a common id and measure.

    :param rteTable:
    :param rteIDField:
    :param frmMeasField:
    :param orderField:
    :return:
    """
    import arcpy

    sql_clause = (None, "ORDER BY {0}, {1} ASC".format(rteIDField,
                  frmMeasField))

    current = ""
    previous = ""
    counter = 0
    NEW_ORDER = 1

    if orderField not in [f.name for f in arcpy.ListFields(rteTable)]:
        print "Adding order field..."
        arcpy.AddField_management(rteTable, orderField, "SHORT")

    with arcpy.da.UpdateCursor(in_table=rteTable,
                               field_names=[rteIDField, frmMeasField,
                                            orderField],
                               sql_clause=sql_clause) as rows:
        for row in rows:
            current = row[0]
            if counter == 0:
                previous = current
                row[2] = NEW_ORDER
            elif previous == current and counter > 0:
                NEW_ORDER += 1
                row[2] = NEW_ORDER
            else:
                NEW_ORDER = 1
                row[2] = NEW_ORDER
            previous = current
            counter += 1
            print counter
            rows.updateRow(row)


def unique_values_arcpy(table, field, query=None):
    """
    Return all unique values in a field as a list of strings

    :param table: Input table (any format accepted by ArcPy
    :param field: The field to return unique values for
    :param query: Optional query
    :return: Returns a list of unique values as strings
    """
    import arcpy
    import numpy as np

    desc = arcpy.Describe(table)

    field_type = None

    for f in desc.fields:
        if f.name == field:
            field_type = f.type
            break
        else:
            pass

    if not query:
        rows = arcpy.SearchCursor(table)
    else:
        rows = arcpy.SearchCursor(table, query)

    field_values = []

    for row in rows:

        if row.getValue(field) is not None:
            field_value = row.getValue(field)

            if field_type == "SmallInteger" or field_type == "Integer":
                field_values.append(field_value)

            else:
                field_values.append(str(field_value))

        else:
            field_values.append("NoneType")

    data = np.array(field_values)
    unique_data = np.unique(data)

    return unique_data.tolist()


def unique_values_report_arcpy(input_table, output_table, max_values=25):
    """
    Given an ArcGIS table or feature class, creates a CSV of all unique values

    :param input_table: Input table with values
    :param output_table: Output CSV file
    :param max_values: Total number of unique values to report (default=25)
    :return: None
    """
    from os import path
    import csv

    import arcpy
    from arcpy import env

    env.workspace = path.dirname(input_table)
    in_table = path.basename(input_table)

    with open(output_table, 'wb') as out_csv:
        spamwriter = csv.DictWriter(out_csv, ["Field", "Unique Values"])
        for field in [f.name for f in arcpy.ListFields(in_table)]:
            uniq_val = unique_values_arcpy(input_table, field)
            if len(uniq_val) <= max_values:
                print "Field: {0} Values: {1}".format(field, uniq_val)
                spamwriter.writerow({'Field': field,
                                     'Unique Values': uniq_val})
            else:
                print "OBSCURED - Field: {0} has more than {1} unique " \
                      "values".format(field, max_values)


def unique_values_report_csv(input_table, output_table, max_values=25):
    """
    Given a table in CSV format creates a new CSV of all unique values

    :param input_table: Input table with values
    :param output_table: Output CSV file
    :param max_values: Total number of unique values to report (default=25)
    :return: None
    """
    from os import path
    import csv

    import arcpy
    from arcpy import env

    env.workspace = path.dirname(input_table)
    in_table = path.basename(input_table)

    with open(output_table, 'wb') as out_csv:
        spamwriter = csv.DictWriter(out_csv, ["Field", "Unique Values"])
        for field in [f.name for f in arcpy.ListFields(in_table)]:
            uniq_val = unique_values_arcpy(input_table, field)
            if len(uniq_val) <= max_values:
                print "Field: {0} Values: {1}".format(field, uniq_val)
                spamwriter.writerow({'Field': field,
                                     'Unique Values': uniq_val})
            else:
                print "OBSCURED - Field: {0} has more than {1} unique " \
                      "values".format(field, max_values)
