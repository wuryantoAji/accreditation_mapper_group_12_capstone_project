import pandas as pd


class SFIA:
    def __init__(self, excel_file, sheet='Sheet1', 
                columns=[ 'lang', 
                          'version', 
                          'Skill', 
                          'description', 
                          'code', 
                          'level', 
                          'description22' ]):
        self.data = {}
        self.langugage = ""
        self.version = ""

        df = pd.read_excel(excel_file, header=0, sheet_name=sheet)
        filtered_df = df[columns]

        for index, row in filtered_df.iterrows():
            self.language = row['lang']
            self.version = row['version']
            entry =   { 'Description' : row['description'], 'Description22':row['description22'] } 
            outer_key = row['code']
            inner_key = row['level']
            if outer_key not in self.data:
                self.data[outer_key] = {}
            self.data[outer_key][inner_key] = entry

    def get_language(self):
        return self.language
    
    def get_version(self):
        return self.version

    def get_data_frame(self):
        """ Flatten a triple nested dictionary into a list of dictionaries. """
        rows = []
        for outer_key, sub_dict in self.data.items():
            for inner_key, items_dict in sub_dict.items():
                beginning = {
                    'code': outer_key,
                    'level': inner_key 
                }
                end = {}
                for item_key, value in items_dict.items():
                    end[item_key] = value
                rows.append( beginning | end )
        return pd.DataFrame(rows)
    
    def __getitem__(self, key):
        if isinstance(key, tuple):
            outer_key, inner_key, item_key = key
            return self.data.get(outer_key, {}).get(inner_key, {}).get(item_key, None)
        elif isinstance(key, str):
            return self.data.get(key, {})
        else:
            raise KeyError("Key must be a string or a tuple (code, level, item)")

    def __repr__(self):
        return repr(self.data)

