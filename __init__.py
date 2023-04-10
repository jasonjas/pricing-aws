import os
import sys

script_dir = os.path.dirname(__file__)
sys.path.append(script_dir)

import excel
import manage_offers

__version__ = "0.1.0"


def process_excel_file(input_file_location, output_file_location):
    excel.process_excel_doc(input_file_location, output_file_location)


def update_offer_databases():
    manage_offers.create_update_databases()