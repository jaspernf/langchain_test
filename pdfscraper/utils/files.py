""" utils.files v_0_1 - functions to manipulate files"""
import os
import glob
from pathlib import Path
import pandas as pd


def create_directory(dir_name):
    """ Create a directory """
    Path(dir_name).mkdir(parents=True, exist_ok=True)

def get_input_file(input_path, header='', sheet_number=0, to_dict_val='', **kwargs):
    """
    :param input_path: path of input file
    :param header: the name of the header to scrape
    :param has_sheet: check if csv or excel file input
    :param to_dict_val: if this has value this will serve as the dictionary value and
    header is the dictionary key
    :return: list or dictionary if to_dict_val is not ''
    """
    if 'xlsx' in input_path:
        to_find_data = pd.read_excel(os.path.abspath(input_path), sheet_name=sheet_number, **kwargs)
    else:
        to_find_data = pd.read_csv(os.path.abspath(input_path), **kwargs)

    if to_dict_val == '':
        return to_find_data[header].drop_duplicates().to_list()

    return to_find_data.set_index(header).to_dict()[to_dict_val]

def get_file_list(file_dir='.', file_extension='txt', is_latest_only=False):
    """
    get list of all file in the directory
    :param file_dir: file directory string
    :param file_extension: file extension ('txt') is the default
    :param is_latest_only: if this is True, then return only the latest file in the directory
    :return: list of directory , or a single directory
    """
    try:
        list_of_files = glob.glob(
            f'{file_dir}/*.{file_extension}')  # * means all if need specific format then *.csv
        if is_latest_only:
            return max(list_of_files, key=os.path.getctime)
    except ValueError:
        return []
    return list_of_files
