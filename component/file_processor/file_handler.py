import pandas as pd
from internal_util import web_util
import os


class FileHandler:
    data_file_name = "analytics-data.csv"
    cols = ['Page',
            'Page length? (Word count)',
            'Does the page include numbered list?',
            'If yes- numbered list total?',
            'Does the page include bulletpoints?',
            'If yes- bulletpoints list total??',
            'How many hyperlinks?',
            'How many CTAs?',
            'how many images?',
            'popup on page',
            'includes entry pop up?',
            'includes exit pop up?',
            'Does the page include prices?',
            'How many buttons?',
            'Does the page include video?']

    error_cols = ['Error url', 'Exception cause']

    def __init__(self):
        self.analytics_df = self.create_csv_data_file()
        self.error_df = self.create_error_data_file()

    def file_reader(self, file_name):
        df = pd.read_csv(web_util.get_project_data_root() + file_name)
        return df

    def create_csv_data_file(self):
        df = pd.DataFrame(columns=self.cols)
        df.to_csv(web_util.get_project_analytics_path() + "analytics-data.csv", index=False)
        return df

    def apppend_csv_data_file(self, new_row):
        self.analytics_df.loc[len(self.analytics_df)] = new_row
        self.analytics_df.to_csv(web_util.get_project_analytics_path() + "analytics-data.csv", mode='a',
                                 header=False, index=False)
        self.analytics_df = pd.DataFrame(columns=self.analytics_df.columns)

    def create_error_data_file(self):
        df = pd.DataFrame(columns=self.error_cols)
        df.to_csv(web_util.get_project_analytics_path() + "error-urls.csv", index=False)
        return df

    def append_error_url(self, new_row):
        self.error_df.loc[len(self.analytics_df)] = new_row
        self.error_df.to_csv(web_util.get_project_analytics_path() + "error-urls.csv", mode='a',
                             header=False, index=False)
        self.error_df = pd.DataFrame(columns=self.error_df.columns)
