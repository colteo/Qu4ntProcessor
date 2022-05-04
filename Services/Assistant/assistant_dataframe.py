import re
import unicodedata
from pathlib import Path
import os
import shutil
import pandas as pd


class AssistantDataframe:

    @staticmethod
    def columns_data_main_by_date():
        return ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']

    @staticmethod
    def columns_data_main_by_count():
        return ['Time', 'Volume', 'Open', 'High', 'Low', 'Close', 'Complete']

    @staticmethod
    def add_row_to_dataframe(main_df, row_to_append, columns):
        to_append = pd.Series(row_to_append, index=columns)
        to_append = pd.DataFrame(to_append).transpose()
        to_append.set_index(["Time"], inplace=True)

        main_df = pd.concat([main_df, to_append])
        return main_df
