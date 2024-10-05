import pandas as pd

from sfia import SFIA

class Criterion:
    def __init__(self, course, unit_details_dict, outcomes_mappings_df):
        self.course = course
        self.criterion_df = None
        self.criterion_qa_df = None
        self.unit_details_dict = unit_details_dict.copy()
        self.outcomes_mappings_df = outcomes_mappings_df.copy()
        return
    
# Missing:
# - self.code
# - self.award_title
# - self.eft
# - self.first_year_offered
# - self.program_chair
# - self.industry_liasion
# - self.key_academic_staff
# - self.outcomes
# - self.justification
class CriterionA(Criterion):
    def __init__(self, course, unit_details_dict, outcomes_mappings_df):
        Criterion.__init__(self, course, unit_details_dict, outcomes_mappings_df)
        self.code = None
        self.award_title = None
        self.eft = None
        self.first_year_offered = None
        self.program_chair = [ 'UNKNOWN' ]
        self.industry_liasion = [ 'UNKNOWN' ]
        self.key_academic_staff = [ 'UNKNOWN' ]
        self.outcomes = None
        self.justification = None
        
        self.__create_criterion_a()
        self.__check_criterion_a()

    def __check_criterion_a(self):
        return None
      
    def __create_criterion_a(self):
        self.criterion_df = self.unit_details_dict

# Missing: Role input
class CriterionB(Criterion):
    def __init__(self, course, unit_details_dict, outcomes_mappings_df):
        Criterion.__init__(self, course, unit_details_dict, outcomes_mappings_df)
        self.roles = []
        self.__create_criterion_b()
        self.__check_criterion_b()
        self.outcomes = self.criterion_df['Outcome'].unique().tolist()


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
        outcomes_mappings_df_copy = self.outcomes_mappings_df.copy()
        outcomes_mappings_df_copy = outcomes_mappings_df_copy[outcomes_mappings_df_copy['Outcome Group'] == 'ICT Skills SFIA']

        #Remove N/A Level (SFIA/Bloom) and convert the rest to Ints
        outcomes_mappings_df_copy.dropna(subset=['Level (SFIA/Bloom)'], inplace=True)
        outcomes_mappings_df_copy['Level (SFIA/Bloom)'] = pd.to_numeric(outcomes_mappings_df_copy['Level (SFIA/Bloom)'], errors='coerce').fillna(0).astype(int)
        
        
        # Load the SFIA Justifications sheet (for rows that have tags instead of direct justifications)
        sfia_justifications = pd.read_excel('CSSE-allprograms-outcome-mappings-20240927.xlsx', sheet_name='SFIA justifications')

        # Adjust 'Tag' to the correct column name found from the print statement
        justification_map = sfia_justifications.set_index('Tag (used in Outcomes Mappings)')['Justification Text (used in Report Tables)'].to_dict()
        # Function to map justification or keep existing justification if already present
        def get_justification(justification):
            if justification in justification_map:
                return justification_map[justification]  # Map the tag to its detailed justification
            else:
                return justification  # Keep the existing justification if it's already there

        # Apply the function to map specific justifications or leave them as is
        outcomes_mappings_df_copy['Justification'] = outcomes_mappings_df_copy['Justification'].apply(get_justification)

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

    
class CriterionD(Criterion):
    def __init__(self, course, unit_details_dict, outcomes_mappings_df):
        Criterion.__init__(self, course, unit_details_dict, outcomes_mappings_df)
        self.__create_criterion_d()
        self.__check_criterion_d()

    def __check_criterion_d(self):
        return None

    def __create_criterion_d(self):
        outcomes_mappings_df_copy = self.outcomes_mappings_df.copy()
        outcomes_mappings_df_copy = outcomes_mappings_df_copy[outcomes_mappings_df_copy['Outcome Group'] == 'Advanced']

        # Merge with unit_details_dict to get the Unit Name
        merged_df = pd.merge(outcomes_mappings_df_copy, self.unit_details_dict, on='Unit Code', how='inner')
        
        # Ensure we have the Unit Name and Justification columns
        if 'Unit Name' not in merged_df.columns:
            merged_df['Unit Name'] = merged_df['Unit Code'].map(self.unit_details_dict.set_index('Unit Code')['Unit Name'])
        if 'Justification' not in merged_df.columns:
            merged_df['Justification'] = ''
        
        self.criterion_df = merged_df[['Unit Code', 'Unit Name', 'Justification']]

    
class CriterionE(Criterion):
    def __init__(self, course, unit_details_dict, outcomes_mappings_df):
        Criterion.__init__(self, course, unit_details_dict, outcomes_mappings_df)
        self.__create_criterion_e()
        self.__check_criterion_e()

    def __check_criterion_e(self):
        if self.criterion_df is not None and not self.criterion_df.empty:
            num_of_criterion_units = self.criterion_df['Unit Code'].nunique()  
            num_of_units = self.unit_details_dict['Unit Code'].nunique()  
            data = {
                'QA Item': ['Number of units ' + str(num_of_criterion_units) + ' in criterion, expecting 1.' ],
                'Pass/Fail': [ str(num_of_criterion_units == 1), ]
            }
            self.criterion_qa_df = pd.DataFrame(data)
        else:
            self.criterion_qa_df = pd.DataFrame({
                'QA Item': ['No units found for Criterion E'],
                'Pass/Fail': ['Fail']
            })

    def __create_criterion_e(self):
        outcomes_mappings_df_copy = self.outcomes_mappings_df.copy()
        outcomes_mappings_df_copy = outcomes_mappings_df_copy[outcomes_mappings_df_copy['Outcome Group'] == 'Integrated Skills']

        merged_df = pd.merge(self.unit_details_dict, outcomes_mappings_df_copy, on='Unit Code', how='inner')
        
        if not merged_df.empty:
            if 'Unit Name' not in merged_df.columns:
                # Add 'Unit Name' from unit_details_dict
                unit_name_dict = self.unit_details_dict.set_index('Unit Code')['Unit Name'].to_dict()
                merged_df['Unit Name'] = merged_df['Unit Code'].map(unit_name_dict)
            
            self.criterion_df = merged_df[['Unit Code', 'Unit Name', 'Justification']]
        else:
            self.criterion_df = pd.DataFrame(columns=['Unit Code', 'Unit Name', 'Justification'])

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
            self.criterionA[course] = CriterionA( course, self.unit_details_dict[course], outcomes_mappings_df )
            self.criterionB[course] = CriterionB( course, self.unit_details_dict[course], outcomes_mappings_df )
            self.criterionC[course] = None
            self.criterionD[course] = CriterionD( course, self.unit_details_dict[course], outcomes_mappings_df )
            self.criterionE[course] = CriterionE( course, self.unit_details_dict[course], outcomes_mappings_df )

    def __load_unit_details(self, excel):
        # Load the Excel file into a Pandas DataFrame
        df = pd.read_excel(excel, header=0, sheet_name='Programs Details')

        # Drop columns where the name starts with 'Unnamed'
        df = df.loc[:, ~df.columns.str.startswith('Unnamed')]

        # Get the list of columns
        all_columns = df.columns.tolist()

        # Find indices of start and end columns
        try:
            start_idx = 4
            end_idx = len(df.columns)
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
                filtered_df.loc[:, column] = filtered_df[column].astype(str).str.strip()
                filtered_df = filtered_df[filtered_df[column]!= '']
                filtered_df = filtered_df.drop(columns=columns_to_check)

                # Store the filtered DataFrame in the dictionary with the column name as the key
                dataframes_dict[column] = filtered_df

        return dataframes_dict

    