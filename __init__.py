import os
import sys

script_dir = os.path.dirname(__file__)
sys.path.append(script_dir)

import excel

__version__ = "0.1.0"


def process_excel_file(input_file_location, output_file_location):
    excel.process_excel_doc(input_file_location, output_file_location)
