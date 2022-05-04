import inspect
import re
import unicodedata
from pprint import pprint


class Assistant:

    @staticmethod
    def normalize_string(val):
        val = unicodedata.normalize('NFKD', val).encode('ascii', 'ignore').decode('ascii')
        val = re.sub(r'[^\w\s-]', '', val.upper())
        val = re.sub(r'[-\s]+', '-', val).strip('-_')
        val = val.replace("_", "-")
        return val

    @staticmethod
    def objects_list_to_matrix(objects_list):
        columns_name = list(objects_list[0].__dict__.keys())
        w = len(objects_list)
        h = len(columns_name)
        matrix = [[0 for x in range(w)] for y in range(h)]
        for idx_obj, object in enumerate(objects_list):
            for idx_column, column_name in enumerate(columns_name):
                property_value = getattr(object, column_name)
                if isinstance(property_value, Enum):
                    matrix[idx_column][idx_obj] = property_value.name
                else:
                    matrix[idx_column][idx_obj] = property_value
        return matrix

    @staticmethod
    def print_object(obj):
        if obj is not None:
            pprint(vars(obj))
            print()

