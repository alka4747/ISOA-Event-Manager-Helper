from flask import Blueprint, request, abort, send_file
from werkzeug.utils import secure_filename
from operator import itemgetter
from zipfile import ZipFile
import pandas as pd
import xml.etree.ElementTree as ET
import os
import io
import csv
import tempfile
import xlsxwriter
import datetime

competition = Blueprint('competition', __name__)

ALLOWED_STARTLIST_FILE_EXTENSIONS = [".csv", ".xlsx"]
ALLOWED_MULKA_RESULTS_FILE_EXTENSIONS = [".csv"]
ALLOWED_SI_DROID_RESULTS_FILE_EXTENSIONS = [".xml"]

def validate_startlist_files_user_input(startlist_files_list):
    # User has to input 2 files exactly
    if len(startlist_files_list) != 2:
        abort(400)
    for startlist_file in startlist_files_list:
        filename = secure_filename(startlist_file.filename)
        # filename has to be valid, and with the right file extension
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in ALLOWED_STARTLIST_FILE_EXTENSIONS:
                abort(400)
            if file_ext == ".csv":
                csv_startlist_file = startlist_file
            else:
                excel_startlist_file = startlist_file
        else:
            abort(400)
    return csv_startlist_file, excel_startlist_file

def validate_si_rent_data_user_input(si_boxes_range_starts, si_boxes_range_endings, missing_si_card_numbers_in_boxes):
    missing_si_card_numbers = []
    si_boxes_ranges = []
    all_si_card_numbers = []
    for i in range(len(si_boxes_range_starts)):
        if not si_boxes_range_starts[i].isdigit() or not si_boxes_range_endings[i].isdigit():
            abort(400)
        # range start has to be smaller or equal to range end (one SI card is legal)
        if int(si_boxes_range_starts[i]) > int(si_boxes_range_endings[i]):
            abort(400)
        si_boxes_ranges.append(range(int(si_boxes_range_starts[i]), int(si_boxes_range_endings[i])+1))
        # missing si card numbers has to be within SI box card number range
        if missing_si_card_numbers_in_boxes[i] != "":
            for si_card_number in missing_si_card_numbers_in_boxes[i].replace(" ", "").split(","):
                if not si_card_number.isdigit():
                    abort(400)
                if int(si_card_number) not in [*range(int(si_boxes_range_starts[i]), (int(si_boxes_range_endings[i])+1))]:
                    abort(400)
                missing_si_card_numbers.append(int(si_card_number))
    for si_range in si_boxes_ranges:
        all_si_card_numbers.extend([*si_range])
    available_si_card_numbers_for_rent = list(filter(lambda el: el not in missing_si_card_numbers, all_si_card_numbers))
    return si_boxes_ranges, missing_si_card_numbers, available_si_card_numbers_for_rent

def read_startlist_files_to_list(csv_file, excel_file, directory):
    with open(os.path.join(directory, "isoa_startlist.csv"), encoding="utf8") as csv_file:
        # Read files
        csv_reader = csv.reader(csv_file)
        df = pd.read_excel(excel_file, dtype=str)
        excel_startlist_list = df.values.tolist()
        return sorted(list(csv_reader)[1:], key=itemgetter(1)), sorted(excel_startlist_list, key=itemgetter(1))

def get_exceptional_list(csv_statlist_list, excel_startlist_list):
    exceptional_list = []
    for index in range(len(csv_statlist_list)):
        if excel_startlist_list[index][10] == "True":
            if csv_statlist_list[index][3] == "עממי":
                exceptional_competitor = csv_statlist_list[index]
                exceptional_competitor.append("שכר כרטיס אלקטרוני אבל נרשם לעממי")
                exceptional_list.append(exceptional_competitor)
        else:
            if csv_statlist_list[index][3] != "עממי" and (csv_statlist_list[index][5] == "" or csv_statlist_list[index][5] == "0"):
                exceptional_competitor = csv_statlist_list[index]
                exceptional_competitor.append("נרשם לתחרותי אבל ללא כרטיס אלקטרוני")
                exceptional_list.append(exceptional_competitor)
    return exceptional_list

def allocate_si_cards(csv_statlist_list, excel_startlist_list, available_si_card_numbers_for_rent):
    si_number_index = 0
    si_renders_list = []
    for index in range(len(csv_statlist_list)):
        if excel_startlist_list[index][10] == "True":
            # Allocate SI number
            csv_statlist_list[index][5] = str(available_si_card_numbers_for_rent[si_number_index])
            si_renders_list.append(csv_statlist_list[index])
            si_number_index += 1
            if si_number_index > len(available_si_card_numbers_for_rent):
                raise Exception("No more SI numbers to allocate")
    return si_renders_list

def populate_si_rental_worksheets(excel_workbook, number_ranges_list, missing_numbers, renders_list):
    worksheets_list = []
    index = 1
    for number_range in number_ranges_list:
        worksheet = excel_workbook.add_worksheet("מזוודה " + str(index))
        # Create a format to use in the merged range.
        merge_format = excel_workbook.add_format({
            'bold': 1,
            'underline': 1,
            'font_name': 'Arial',
            'font_size': 14,
            'align': 'center',
            'valign': 'vcenter',
            'reading_order': 2})
        # Create format to usr in headers line
        headers_format = excel_workbook.add_format({
            'bold': 1,
            'border': 1,
            'font_name': 'Arial',
            'font_size': 12,
            'align': 'center',
            'valign': 'vcenter',
            'reading_order': 2
        })
        text_format = excel_workbook.add_format({
            'border': 1,
            'font_name': 'Arial',
            'font_size': 12,
            'align': 'center',
            'valign': 'vcenter',
            'reading_order': 2
        })
        missing_format = excel_workbook.add_format({
            'border': 1,
            'font_name': 'Arial',
            'font_size': 12,
            'fg_color': 'red'
        })
        # Change direction to right to left
        worksheet.right_to_left()

        # Set columns width
        worksheet.set_column('A:A', 11)
        worksheet.set_column('B:B', 14)
        worksheet.set_column('C:C', 25)
        worksheet.set_column('D:D', 14)
        worksheet.set_column('E:E', 12)
        worksheet.set_column('F:F', 12)
        worksheet.set_column('G:G', 14)

        # Headers row
        worksheet.merge_range('A1:G1', 'השאלת כרטיסי SI', merge_format)
        worksheet.write('A3', "מס' כרטיס", headers_format)
        worksheet.write('B3', "מס' חבר/ת.ז.", headers_format)
        worksheet.write('C3', "שם", headers_format)
        worksheet.write('D3', "טלפון", headers_format)
        worksheet.write('E3', "תעודת זהות", headers_format)
        worksheet.write('F3', "רישיון נהיגה", headers_format)
        worksheet.write('G3', "החזרת כרטיס", headers_format)

        # Separating row
        worksheet.write('A4', "", headers_format)
        worksheet.write('B4', "", headers_format)
        worksheet.write('C4', "", headers_format)
        worksheet.write('D4', "", headers_format)
        worksheet.write('E4', "", headers_format)
        worksheet.write('F4', "", headers_format)
        worksheet.write('G4', "", headers_format)

        # Populate SI numbers
        si_numbers_row_index = 5
        for si_number in [*number_range]:
            worksheet.write('A' + str(si_numbers_row_index), str(si_number), text_format)
            if si_number in missing_numbers:
                worksheet.write('B' + str(si_numbers_row_index), "", missing_format)
                worksheet.write('C' + str(si_numbers_row_index), "", missing_format)
                worksheet.write('D' + str(si_numbers_row_index), "", missing_format)
                worksheet.write('E' + str(si_numbers_row_index), "", missing_format)
                worksheet.write('F' + str(si_numbers_row_index), "", missing_format)
                worksheet.write('G' + str(si_numbers_row_index), "", missing_format)
            else:
                worksheet.write('B' + str(si_numbers_row_index), "", text_format)
                worksheet.write('C' + str(si_numbers_row_index), "", text_format)
                worksheet.write('D' + str(si_numbers_row_index), "", text_format)
                worksheet.write('E' + str(si_numbers_row_index), "", text_format)
                worksheet.write('F' + str(si_numbers_row_index), "", text_format)
                worksheet.write('G' + str(si_numbers_row_index), "", text_format)
                for render in renders_list:
                    if render[5] == str(si_number):
                        worksheet.write('B' + str(si_numbers_row_index), str(render[0]), text_format)
                        worksheet.write('C' + str(si_numbers_row_index), str(render[1]), text_format)
                        worksheet.write('D' + str(si_numbers_row_index), str(render[10]), text_format)
                        worksheet.write('E' + str(si_numbers_row_index), "", text_format)
                        worksheet.write('F' + str(si_numbers_row_index), "", text_format)
                        worksheet.write('G' + str(si_numbers_row_index), "", text_format)
            si_numbers_row_index += 1
        worksheets_list.append(worksheet)
        index += 1
    return worksheets_list

def populate_start_list_worksheets(excel_workbook, registration_csv_list):
    headers_format = excel_workbook.add_format({
        'border': 1,
        'font_name': 'Liberation Sans',
        'font_size': 10,
        'align': 'center',
        'valign': 'vcenter',
        'reading_order': 2
    })
    text_format = excel_workbook.add_format({
        'border': 1,
        'font_name': 'Liberation Sans',
        'font_size': 10,
        'align': 'right',
        'valign': 'vcenter',
        'reading_order': 2
    })
    # Write all pre-registered competitors list
    all_competitors_worksheet = excel_workbook.add_worksheet("נרשמים מראש")
    all_competitors_worksheet.right_to_left()
    all_competitors_worksheet.set_column('A:A', 11)
    all_competitors_worksheet.set_column('B:B', 20)
    all_competitors_worksheet.set_column('C:C', 13)
    all_competitors_worksheet.set_column('D:D', 7)
    all_competitors_worksheet.set_column('E:E', 11)
    all_competitors_worksheet.set_column('F:F', 13)
    all_competitors_worksheet.set_column('G:G', 11)

    # Headers row
    all_competitors_worksheet.write('A1', "מס' חבר", headers_format)
    all_competitors_worksheet.write('B1', "שם", headers_format)
    all_competitors_worksheet.write('C1', "מועדון", headers_format)
    all_competitors_worksheet.write('D1', "מסלול", headers_format)
    all_competitors_worksheet.write('E1', "מס' כרטיס", headers_format)
    all_competitors_worksheet.write('F1', "טלפון", headers_format)
    all_competitors_worksheet.write('G1', "שעת זינוק", headers_format)

    # Separating row
    all_competitors_worksheet.write('A2', "", text_format)
    all_competitors_worksheet.write('B2', "", text_format)
    all_competitors_worksheet.write('C2', "", text_format)
    all_competitors_worksheet.write('D2', "", text_format)
    all_competitors_worksheet.write('E2', "", text_format)
    all_competitors_worksheet.write('F2', "", text_format)
    all_competitors_worksheet.write('G2', "", text_format)

    competitor_index = 3
    for competitor in registration_csv_list:
        all_competitors_worksheet.write('A' + str(competitor_index), competitor[0], text_format)
        all_competitors_worksheet.write('B' + str(competitor_index), competitor[1], text_format)
        all_competitors_worksheet.write('C' + str(competitor_index), competitor[2], text_format)
        all_competitors_worksheet.write('D' + str(competitor_index), competitor[3], text_format)
        all_competitors_worksheet.write('E' + str(competitor_index), competitor[5], text_format)
        all_competitors_worksheet.write('F' + str(competitor_index), competitor[10], text_format)
        all_competitors_worksheet.write('G' + str(competitor_index), "", text_format)
        competitor_index += 1

    sorted_competitor_list_by_classes = get_sorted_competitor_list_by_classes(registration_csv_list)
    for course in sorted_competitor_list_by_classes:
        if course != "עממי":
            worksheet = excel_workbook.add_worksheet(course)
            worksheet.right_to_left()
            worksheet.set_column('A:A', 9)
            worksheet.set_column('B:B', 11)
            worksheet.set_column('C:C', 20)
            worksheet.set_column('D:D', 13)
            worksheet.set_column('E:E', 7)
            worksheet.set_column('F:F', 11)
            worksheet.set_column('G:G', 13)
            worksheet.set_column('H:H', 11)

            # Headers row
            worksheet.write('A1', "מס' סידורי", headers_format)
            worksheet.write('B1', "מס' חבר", headers_format)
            worksheet.write('C1', "שם", headers_format)
            worksheet.write('D1', "מועדון", headers_format)
            worksheet.write('E1', "מסלול", headers_format)
            worksheet.write('F1', "מס' כרטיס", headers_format)
            worksheet.write('G1', "טלפון", headers_format)
            worksheet.write('H1', "שעת זינוק", headers_format)

            # Separating row
            worksheet.write('A2', "", text_format)
            worksheet.write('B2', "", text_format)
            worksheet.write('C2', "", text_format)
            worksheet.write('D2', "", text_format)
            worksheet.write('E2', "", text_format)
            worksheet.write('F2', "", text_format)
            worksheet.write('G2', "", text_format)
            worksheet.write('H2', "", text_format)
            competitor_index = 3
            for competitor in sorted_competitor_list_by_classes[course]:
                worksheet.write('A' + str(competitor_index), str(competitor_index-2), text_format)
                worksheet.write('B' + str(competitor_index), competitor[0], text_format)
                worksheet.write('C' + str(competitor_index), competitor[1], text_format)
                worksheet.write('D' + str(competitor_index), competitor[2], text_format)
                worksheet.write('E' + str(competitor_index), competitor[3], text_format)
                worksheet.write('F' + str(competitor_index), competitor[5], text_format)
                worksheet.write('G' + str(competitor_index), competitor[10], text_format)
                worksheet.write('H' + str(competitor_index), "", text_format)
                competitor_index += 1

            # Continue lines up to 150
            while competitor_index - 2 <= 150:
                worksheet.write('A' + str(competitor_index), str(competitor_index - 2), text_format)
                worksheet.write('B' + str(competitor_index), "", text_format)
                worksheet.write('C' + str(competitor_index), "", text_format)
                worksheet.write('D' + str(competitor_index), "", text_format)
                worksheet.write('E' + str(competitor_index), "", text_format)
                worksheet.write('F' + str(competitor_index), "", text_format)
                worksheet.write('G' + str(competitor_index), "", text_format)
                worksheet.write('H' + str(competitor_index), "", text_format)
                competitor_index += 1
        else:
            worksheet = excel_workbook.add_worksheet(course)
            worksheet.right_to_left()
            worksheet.set_column('A:A', 9)
            worksheet.set_column('B:B', 20)
            worksheet.set_column('C:C', 13)
            worksheet.set_column('D:D', 13)
            worksheet.set_column('E:E', 12)
            worksheet.set_column('F:F', 11)

            # Headers row
            worksheet.write('A1', "מס' סידורי", headers_format)
            worksheet.write('B1', "שם", headers_format)
            worksheet.write('C1', "מועדון", headers_format)
            worksheet.write('D1', "מספר משתתפים", headers_format)
            worksheet.write('E1', "טלפון", headers_format)
            worksheet.write('F1', "שעת יציאה", headers_format)

            # Separating row
            worksheet.write('A2', "", text_format)
            worksheet.write('B2', "", text_format)
            worksheet.write('C2', "", text_format)
            worksheet.write('D2', "", text_format)
            worksheet.write('E2', "", text_format)
            worksheet.write('F2', "", text_format)
            competitor_index = 3
            for competitor in sorted_competitor_list_by_classes[course]:
                worksheet.write('A' + str(competitor_index), str(competitor_index - 2), text_format)
                worksheet.write('B' + str(competitor_index), competitor[1], text_format)
                worksheet.write('C' + str(competitor_index), competitor[2], text_format)
                worksheet.write('D' + str(competitor_index), "", text_format)
                worksheet.write('E' + str(competitor_index), competitor[10], text_format)
                worksheet.write('F' + str(competitor_index), "", text_format)
                competitor_index += 1

            # Continue lines up to 150
            while competitor_index - 2 <= 150:
                worksheet.write('A' + str(competitor_index), str(competitor_index - 2), text_format)
                worksheet.write('B' + str(competitor_index), "", text_format)
                worksheet.write('C' + str(competitor_index), "", text_format)
                worksheet.write('D' + str(competitor_index), "", text_format)
                worksheet.write('E' + str(competitor_index), "", text_format)
                worksheet.write('F' + str(competitor_index), "", text_format)
                competitor_index += 1

# Returns a Dictionary with course names as keys, and sorted competitor lists as values 
def get_sorted_competitor_list_by_classes(registration_csv_list):
    registration_by_classes_dict = {}
    class_names = get_class_names(registration_csv_list)
    for class_name in class_names:
        # Add class name as index
        registration_by_classes_dict[class_name] = []
    sorted_list = sorted(registration_csv_list, key=itemgetter(3, 1))
    for competitor in sorted_list:
        # Append competitor to class list
        registration_by_classes_dict[competitor[3]].append(competitor)
    return registration_by_classes_dict

# Returns all course names in a competition as a set
def get_class_names(registration_csv_list):
    class_names = set()
    for competitor in registration_csv_list:
        class_names.add(competitor[3])
    return class_names

def validate_mulka_results_user_input(uploaded_mulka_results_file):
    filename = secure_filename(uploaded_mulka_results_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in ALLOWED_MULKA_RESULTS_FILE_EXTENSIONS:
            abort(400)
    else:
        abort(400)

def generate_isoa_results_file_from_mulka_results(uploaded_mulka_results_file, directory):
    uploaded_mulka_results_file.save(os.path.join(directory, "mulka_results.csv"))
    with open(os.path.join(directory, "mulka_results.csv"), 'r', encoding="cp1255") as mulka_results_file:
        # Skip headers
        mulka_results_file.readline()
        # Read competitor list CSV
        reader = csv.reader(mulka_results_file, delimiter=',')
        csv_lines = []
        for r in reader:
            if len(r) == 18 and r[17] != '' and r[17] != 'DNS':
                name = r[4].split()
                name.insert(0, name.pop())
                first_name, *last_name = name
                last_name = " ".join(last_name)
                csv_lines.append([r[0], r[1], r[2], last_name, first_name, r[17]])
        # Sort results CSV content
        sorted_list = sorted(csv_lines, key=itemgetter(1, 5))
    with open(os.path.join(directory, "official_results.csv"), 'w', newline='', encoding="cp1255") as offical_results:
        writer = csv.writer(offical_results)
        # Write headers row
        headers_row = ["runnerid", "category", "position", "famname", "usrname", "time"]
        writer.writerow(headers_row)
        # Write results to CSV
        for row in sorted_list:
            writer.writerow(row)

def validate_si_droid_results_user_input(uploaded_si_droid_results_file):
    filename = secure_filename(uploaded_si_droid_results_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in ALLOWED_SI_DROID_RESULTS_FILE_EXTENSIONS:
            abort(400)
    else:
        abort(400)

def parse_si_droid_results_xml(xml_file):
    # create element tree object
    tree = ET.parse(xml_file)
    # get root element
    root = tree.getroot()

    # create empty list for competitors data
    competitors_data = []

    # iterate competitors
    for class_result in root.findall('{http://www.orienteering.org/datastandard/3.0}ClassResult'):
        position_index = 1
        for competitor in class_result.findall('{http://www.orienteering.org/datastandard/3.0}PersonResult'):
            if competitor.find('{http://www.orienteering.org/datastandard/3.0}Result').find('{http://www.orienteering.org/datastandard/3.0}Status').text == "OK":
                competitor_time = str(datetime.timedelta(seconds = int(competitor.find('{http://www.orienteering.org/datastandard/3.0}Result').find('{http://www.orienteering.org/datastandard/3.0}Time').text)))
                competitor_position = position_index
            else:
                competitor_time = "DISQ"
                competitor_position = ""
            competitor_id = competitor.find('{http://www.orienteering.org/datastandard/3.0}Person').find('{http://www.orienteering.org/datastandard/3.0}Id')
            if competitor_id is not None:
                competitor_id = competitor_id.text
            competitor_data = {'runnerId': competitor_id,
                               'category': class_result.find('{http://www.orienteering.org/datastandard/3.0}Class').find('{http://www.orienteering.org/datastandard/3.0}Name').text,
                               'position': competitor_position,
                               'famname': competitor.find('{http://www.orienteering.org/datastandard/3.0}Person').find('{http://www.orienteering.org/datastandard/3.0}Name').find('{http://www.orienteering.org/datastandard/3.0}Family').text,
                               'usrname': competitor.find('{http://www.orienteering.org/datastandard/3.0}Person').find('{http://www.orienteering.org/datastandard/3.0}Name').find('{http://www.orienteering.org/datastandard/3.0}Given').text,
                               'time': competitor_time}
            competitors_data.append(competitor_data)
            position_index += 1
    headers = ['runnerId', 'category', 'position', 'famname', 'usrname', 'time']
    return {"headers": headers,
            "competitors_data": competitors_data}

def save_si_droid_official_results_to_csv(xml_data, file_name):
    # writing to csv file
    with open(file_name, 'w', encoding="cp1255", newline='') as csvfile:
        # creating a csv dict writer object
        writer = csv.writer(csvfile)

        # writing headers (field names)
        writer.writerow(xml_data["headers"])
        # write punch data
        for competitor_data in xml_data["competitors_data"]:
            writer.writerow(competitor_data.values())
    return csvfile

def generate_isoa_results_file_from_si_droid_results(uploaded_si_droid_results_file, directory):
        uploaded_si_droid_results_file.save(os.path.join(directory, "si_droid_results.xml"))
        # parse xml file
        xml_data = parse_si_droid_results_xml(os.path.join(directory, "si_droid_results.xml"))
        # store results in a csv file
        return save_si_droid_official_results_to_csv(xml_data, os.path.join(directory,'official_results.csv'))
        

@competition.route('/generate-preperation-files', methods=['POST'])
def generate_preperation_files():
    if request.method == 'POST':
        platform = request.form['platform']
        uploaded_startlist_files = request.files.getlist("startlists")
        si_boxes_range_starts = request.form.getlist("rangeStart[]")
        si_boxes_range_endings = request.form.getlist("rangeEnd[]")
        missing_si_card_numbers_in_boxes = request.form.getlist("missingCards[]")
        # Validate user input
        if platform not in ['mulka', 'si-droid']:
            abort(400)
        csv_startlist_file, excel_startlist_file = validate_startlist_files_user_input(uploaded_startlist_files)
        si_boxes_ranges, missing_si_card_numbers, available_si_card_numbers_for_rent = validate_si_rent_data_user_input(si_boxes_range_starts, si_boxes_range_endings, missing_si_card_numbers_in_boxes)
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_startlist_file.save(os.path.join(tmpdir, "isoa_startlist.csv"))
            csv_startlist_list, excel_startlist_list = read_startlist_files_to_list(csv_startlist_file, excel_startlist_file, tmpdir)
            if len(available_si_card_numbers_for_rent) > 0:
                # Allocate SI cards and output renders list, exceptionals list
                si_renders_list = allocate_si_cards(csv_startlist_list, excel_startlist_list, available_si_card_numbers_for_rent)

                # Write SI rental list
                si_rental_workbook = xlsxwriter.Workbook(os.path.join(tmpdir,'השאלת_כרטיסי_SI.xlsx'))
                populate_si_rental_worksheets(si_rental_workbook, si_boxes_ranges, missing_si_card_numbers, si_renders_list)
                si_rental_workbook.close()

            # Write exceptional list
            exceptional_list = get_exceptional_list(csv_startlist_list, excel_startlist_list)
           
            with open(os.path.join(tmpdir,"חריגים.csv"), 'w', newline='', encoding="cp1255") as exceptionals_file:
                exceptionals_writer = csv.writer(exceptionals_file)
                headers_row = ["מס' חבר/ת.ז.", "שם", "מועדון", "מסלול", "טלפון", "חריגה"]
                exceptionals_writer.writerow(headers_row)
                # Write new start list to CSV
                for row in exceptional_list:
                    exceptional_competitor_row = [row[0], row[1], row[2], row[3], row[10], row[11]]
                    exceptionals_writer.writerow(exceptional_competitor_row)

            # Write Start list sheets
            start_list_workbook = xlsxwriter.Workbook(os.path.join(tmpdir,'רשימות_זינוק_למזניקים.xlsx'))
            populate_start_list_worksheets(start_list_workbook, csv_startlist_list)
            start_list_workbook.close()

            # Allocate strangers start number
            STRANGERS_START_NUMBER = 20000

            for index in range(len(csv_startlist_list)):
                if int(csv_startlist_list[index][0]) > 20000:
                    csv_startlist_list[index][0] = str(STRANGERS_START_NUMBER)
                    STRANGERS_START_NUMBER += 1
            
            # Write start list for platform
            if platform == "mulka":
                # Write start list for Mulka
                with open(os.path.join(tmpdir,"start_list.csv"), 'w', newline='', encoding="cp1255") as official_start_list:
                    start_list_writer = csv.writer(official_start_list)
                    headers_row = ["STNO", "NAME", "CLUB", "CLASS NAME", "CARD NUMBER"]
                    start_list_writer.writerow(headers_row)
                    # Write new start list to CSV
                    for row in csv_startlist_list:
                        official_start_list_row = [row[0], row[1], row[2], row[3], row[5]]
                        start_list_writer.writerow(official_start_list_row)
            elif platform == "si-droid":
                # Write start list for si-droid
                with open(os.path.join(tmpdir,"start_list.csv"), 'w', newline='', encoding="utf8") as official_start_list:
                    start_list_writer = csv.writer(official_start_list)
                    headers_row = ["SI Number", "Name", "Club", "Id", "Course"]
                    start_list_writer.writerow(headers_row)
                    # Write new start list to CSV
                    for row in csv_startlist_list:
                        official_start_list_row = [row[5], row[1], row[2], row[0], row[3]]
                        if str(row[5]) != "" and str(row[5]) != "0":
                            start_list_writer.writerow(official_start_list_row)
            
             # writing files to a zipfile
            with ZipFile(os.path.join(tmpdir,'competition_files.zip'),'w') as zip:
                # writing each file one by one
                if len(available_si_card_numbers_for_rent) > 0:
                    file_paths = [os.path.join(tmpdir,"start_list.csv"), os.path.join(tmpdir,'רשימות_זינוק_למזניקים.xlsx'), os.path.join(tmpdir,'השאלת_כרטיסי_SI.xlsx'), os.path.join(tmpdir,"חריגים.csv")]
                else:
                    file_paths = [os.path.join(tmpdir,"start_list.csv"), os.path.join(tmpdir,'רשימות_זינוק_למזניקים.xlsx'), os.path.join(tmpdir,"חריגים.csv")]
                for file in file_paths:
                    zip.write(file, os.path.basename(file))

            # Send zip to client
            with open(os.path.join(tmpdir, "competition_files.zip"), "rb") as f:
                content = io.BytesIO(f.read())
            return send_file(content,
                             as_attachment=True,
                             attachment_filename='competition_files.zip')

@competition.route('/generate-isoa-results-file', methods=['POST'])
def generate_isoa_results_file():
    if request.method == 'POST':
        platform = request.form['platform']
        if platform not in ['mulka', 'si-droid']:
            abort(400)
        with tempfile.TemporaryDirectory() as tmpdir:
            if platform == "mulka":
                uploaded_mulka_results_file = request.files["resultsFile"]
                validate_mulka_results_user_input(uploaded_mulka_results_file)
                generate_isoa_results_file_from_mulka_results(uploaded_mulka_results_file, tmpdir)
            elif platform == "si-droid":
                uploaded_si_droid_results_file = request.files["resultsFile"]
                validate_si_droid_results_user_input(uploaded_si_droid_results_file)
                generate_isoa_results_file_from_si_droid_results(uploaded_si_droid_results_file, tmpdir)
            # send official results to client
            with open(os.path.join(tmpdir, "official_results.csv"), "rb") as f:
                content = io.BytesIO(f.read())
            return send_file(content,
                             as_attachment=True,
                             attachment_filename="official_results.csv")