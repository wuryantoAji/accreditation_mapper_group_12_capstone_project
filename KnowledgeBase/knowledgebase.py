import pandas as pd

from sfia import SFIA

class Criterion:
    def __init__(self, course, unit_details_dict, outcomes_mappings_df):
        self.course = course
        self.criterion_df = None
        self.criterion_qa_df = None
        self.unit_details_dict = unit_details_dict
        self.outcomes_mappings_df = outcomes_mappings_df
        return
    


class CriterionB(Criterion):
    def __init__(self, course, sfia, unit_details_dict, outcomes_mappings_df):
        Criterion.__init__(self, course, unit_details_dict, outcomes_mappings_df)
        self.roles = []
        self.sfia = sfia
        self.__create_criterion_b()
        self.__check_criterion_b()
        Criterion.columns = [ 'SFIA Skill', 
                              'Skill Description', 
                              'Level Description', 
                              'Code Level', 
                              'Units supporting SFIA skill' ]


    def __check_criterion_b(self):
        criterion_df = self.criterion_df
        num_of_outcomes = criterion_df['Outcome'].nunique()
        num_of_criterionB_units = criterion_df['Unit Code'].nunique()  
        num_of_units = self.unit_details_dict['Unit Code'].nunique()  
        data = {
            'QA Item': ['Number of outcomes ' +str(num_of_outcomes)+' outcomes (2 required)',
                        'Number of units ' +str(num_of_criterionB_units)+' units out of ' + str(num_of_units) ],
            'Pass/Fail': [ str(num_of_outcomes >= 2), 'N/A']
        }
        self.criterion_qa_df = pd.DataFrame(data)

    def __create_criterion_b(self):
        CRITERION_B_ELEMENTS = { 'PROG': 'Programming/Software Development', 
                            'PRMG': 'Project Management', 
                            'DESN': 'System Design'}

        outcomes_mappings_df_copy = self.outcomes_mappings_df.copy()

        #Remove N/A Level (SFIA/Bloom) and convert the rest to Ints
        outcomes_mappings_df_copy.dropna(subset=['Level (SFIA/Bloom)'], inplace=True)
        outcomes_mappings_df_copy['Level (SFIA/Bloom)'] = pd.to_numeric(outcomes_mappings_df_copy['Level (SFIA/Bloom)'], errors='coerce').fillna(0).astype(int)
   
        merged_df = pd.merge(self.unit_details_dict, outcomes_mappings_df_copy, on='Unit Code', how='inner')
        merged_df = merged_df[['Unit Code', 'Outcome', 'Level (SFIA/Bloom)', 'Justification']]
        sorted_df = merged_df.groupby('Outcome').apply(lambda x: x.sort_values(by='Outcome')).reset_index(drop=True)

        group_column = 'Outcome'
        value_column = 'Level (SFIA/Bloom)'

        # Group by the specified column and find the maximum value for each group
        max_values = sorted_df.groupby(group_column)[value_column].transform('max')

        # Retain rows where the value column is equal to the maximum value within its group
        result_df = sorted_df[sorted_df[value_column] == max_values]

        self.criterion_df = result_df

    



class KnowledgeBase:
    def __init__(self, kb_excel_file, sfia):
        self.__sfia = sfia

        #Outcomes Mappings
        outcomes_mappings_df = df = pd.read_excel(kb_excel_file, header=0, sheet_name='Outcomes Mappings')
        # Outcomes Details
        outcomes_details_df = pd.read_excel(kb_excel_file, header=1, sheet_name='Outcomes Details')
        # Unit details
        self.unit_details_dict = self.__load_unit_details(kb_excel_file)

        # Some necessary data cleaning
        outcomes_mappings_df.dropna(subset=['Unit Code'], inplace=True)
        outcomes_details_df.dropna(subset=['Outcome Group'], inplace=True)
        
        self.criterionA = {}
        self.criterionB = {} 
        self.criterionC = {}
        self.criterionD = {}
        self.criterionE = {}

        for course in self.unit_details_dict.keys():
            self.criterionA[course] = None
            self.criterionB[course] = CriterionB( course, sfia, self.unit_details_dict[course], outcomes_mappings_df )
            self.criterionC[course] = None
            self.criterionD[course] = None
            self.criterionE[course] = None

    def __load_unit_details(self, excel):
        # Load the Excel file into a Pandas DataFrame
        df = pd.read_excel(excel, header=0, sheet_name='Unit Details')

        # Drop columns where the name starts with 'Unnamed'
        df = df.loc[:, ~df.columns.str.startswith('Unnamed')]

        # Get the list of columns
        all_columns = df.columns.tolist()

        # Find indices of start and end columns
        try:
            start_idx = 4
            end_idx = 13
        except ValueError as e:
            print(f"Column not found: {e}")
            raise

        # Define the columns to iterate over
        columns_to_check = all_columns[start_idx:end_idx + 1]

        # Initialize a dictionary to store DataFrames
        dataframes_dict = {}

        # Iterate through the specified columns
        for column in columns_to_check:
            # Check if the header is not NA
            if pd.notna(df[column].name) and not df[column].name.startswith('Unnamed'):
                # Filter rows where the column value is not NA
                filtered_df = df[df[column].notna()]
                filtered_df[column] = filtered_df[column].astype(str).str.strip()
                filtered_df = filtered_df[filtered_df[column]!= '']

                # Store the filtered DataFrame in the dictionary with the column name as the key
                dataframes_dict[column] = filtered_df

        return dataframes_dict

    