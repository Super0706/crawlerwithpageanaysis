from pathlib import Path
import os


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def get_project_data_root():
    data_path = str(get_project_root()) + str(os.sep) + "data" + str(os.sep)
    return data_path


def get_project_analytics_path():
    data_path = str(get_project_root()) + str(os.sep) + "data" + str(os.sep) + "analytics" + str(os.sep)
    return data_path


def get_temp_img_data_path():
    data_path = str(get_project_root()) + str(os.sep) + "data" + str(os.sep) + "temp-files" + str(os.sep)
    return data_path

