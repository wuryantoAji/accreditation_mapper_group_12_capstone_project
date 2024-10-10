import pandas as pd

from sfia import SFIA
from caidi import CAIDI

class Criterion:
    def __init__(self, course, unit_details_dict, outcomes_mappings_df):
        self.course = course
        self.criterion_df = pd.DataFrame()
        self.criterion_qa_df = pd.DataFrame()
        self.unit_details_dict = unit_details_dict.copy()
        self.outcomes_mappings_df = outcomes_mappings_df.copy()
        return
    
# Missing:
# - self.industry_liasion
# - self.key_academic_staff
class CriterionA(Criterion):
    def __init__(self, course, unit_details_dict, outcomes_mappings_df, outcomes_details_df, cd):
        Criterion.__init__(self, course, unit_details_dict, outcomes_mappings_df)
        
        self.__create_criterion_a()
        self.__check_criterion_a()

        identifiers = __extract_identifiers__(course)
        if identifiers[0] not in cd.course:
            return

        filtered_df = outcomes_details_df[(outcomes_details_df['Outcome Group'] == 'Program Outcomes') & (outcomes_details_df['Outcome Subgroup or Level'] == identifiers[0])]
        filtered_df[ 'Complete Outcome' ] = filtered_df[ 'Outcome' ] + "\n" + filtered_df[ 'Outcome Description' ]
        merged_outcomes = '\n'.join(filtered_df['Complete Outcome'])

        filtered_df = outcomes_details_df[(outcomes_details_df['Outcome Group'] == 'Program Justification') & (outcomes_details_df['Outcome Subgroup or Level'] == identifiers[0])]
        filtered_df[ 'Complete Justification' ] = filtered_df[ 'Outcome' ] + "\n" + filtered_df[ 'Outcome Description' ]
        merged_justification = '\n'.join(filtered_df['Complete Justification'])

        self.code = identifiers[0]
        self.award_title = cd.course[identifiers[0]]['Title']
        if identifiers[0].startswith('MJD'):
            self.eft = '3 years'
        else:
            self.eft = '2 years'
        self.first_year_offered = cd.course[identifiers[0]]['First year of offer']
        self.program_chair = cd.course[identifiers[0]]['Coordinator']
        self.industry_liasion = [ 'UNKNOWN' ]
        self.key_academic_staff = [ 'UNKNOWN' ]
        self.outcomes = merged_outcomes
        self.justification = merged_justification

    def __check_criterion_a(self):
        return None
      
    def __create_criterion_a(self):
        self.criterion_df = self.unit_details_dict


class CriterionB(Criterion):
    def __init__(self, course, unit_details_dict, outcomes_mappings_df, outcomes_details_df, sfia_justifications):
        Criterion.__init__(self, course, unit_details_dict, outcomes_mappings_df)
        self.roles = []
        self.__create_criterion_b(outcomes_details_df, sfia_justifications)
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

    def __create_criterion_b(self, outcomes_details_df, sfia_justifications):
        outcomes_mappings_df_copy = self.outcomes_mappings_df.copy()
        outcomes_mappings_df_copy = outcomes_mappings_df_copy[outcomes_mappings_df_copy['Outcome Group'] == 'ICT Skills SFIA']

        #Remove N/A Level (SFIA/Bloom) and convert the rest to Ints
        # Changed 07/10
        #outcomes_mappings_df_copy.dropna(subset=['Level (SFIA/Bloom)'], inplace=True)
        outcomes_mappings_df_copy.dropna(subset=['Level (SFIA/Bloom/UnitOutcome)'], inplace=True)
        # Changed 07/10
        #outcomes_mappings_df_copy['Level (SFIA/Bloom)'] = pd.to_numeric(outcomes_mappings_df_copy['Level (SFIA/Bloom)'], errors='coerce').fillna(0).astype(int)
        outcomes_mappings_df_copy['Level (SFIA/Bloom/UnitOutcome)'] = pd.to_numeric(outcomes_mappings_df_copy['Level (SFIA/Bloom/UnitOutcome)'], errors='coerce').fillna(0).astype(int)
        
        # Adjust 'Tag' to the correct column name found from the print statement
        justification_map = sfia_justifications.set_index('Tag (used in Outcomes Mappings)')['Justification Text (used in Report Tables)'].to_dict()
        # Function to map justification or keep existing justification if already present
        def get_justification(justification):
            if justification in justification_map:
                return justification_map[justification]  # Map the tag to its detailed justification
            else:
                return justification  # Keep the existing justification if it's already there

        # Move the justification to a column called justificationCode
        outcomes_mappings_df_copy['JustificationCode'] = outcomes_mappings_df_copy['Justification']

        # Apply the function to map specific justifications or leave them as is
        outcomes_mappings_df_copy['Justification'] = outcomes_mappings_df_copy['Justification'].apply(get_justification)

        merged_df = pd.merge(self.unit_details_dict, outcomes_mappings_df_copy, on='Unit Code', how='inner')
        # Changed 07/10
        #merged_df = merged_df[['Unit Code', 'Outcome', 'Level (SFIA/Bloom)', 'Justification']]
        merged_df = merged_df[['Unit Code', 'Outcome', 'Level (SFIA/Bloom/UnitOutcome)', 'Justification', 'JustificationCode']]
        sorted_df = merged_df.groupby('Outcome').apply(lambda x: x.sort_values(by='Outcome')).reset_index(drop=True)

        group_column = 'Outcome'
        # Changed 07/10
        #value_column = 'Level (SFIA/Bloom)'
        value_column = 'Level (SFIA/Bloom/UnitOutcome)'

        # Group by the specified column and find the maximum value for each group
        max_values = sorted_df.groupby(group_column)[value_column].transform('max')

        # Retain rows where the value column is equal to the maximum value within its group
        result_df = sorted_df[sorted_df[value_column] == max_values]

        self.criterion_df = result_df

        # Get professional role
        role_df = pd.merge(result_df, outcomes_details_df, on='Outcome', how='left')
        self.roles = list(set(role_df['Professional Role'].tolist()))


class CriterionC(Criterion):
    def __init__(self, course, unit_details_dict, outcomes_mappings_df):
        Criterion.__init__(self, course, unit_details_dict, outcomes_mappings_df)
        
        # Call the functions to create and check Criterion C
        self.__create_criterion_c()
        self.__check_criterion_c()

    def __check_criterion_c(self):
        table_2_df = self.table_2_df

        qa_items = []
        pass_fail = []

        # QA 1: No column may be empty in Table 2
        empty_columns = []
        for col in table_2_df.columns:
            if table_2_df[col].isnull().all():
                empty_columns.append(col)

        if empty_columns:
            qa_items.append(f"QA 1: The following columns have empty values: {empty_columns}")
            pass_fail.append("Fail")
        else:
            qa_items.append("QA 1: No columns are empty.")
            pass_fail.append("Pass")

        # QA 2: Professional - ICT Ethics, Working Individually & Teamwork should be at least level 3
        professional_issues = []
        for outcome in [('Professional', 'ICT Ethics'), ('Professional', 'Working Individually & Teamwork')]:
            if table_2_df[outcome].dropna().astype(float).lt(3).any() or table_2_df[outcome].isnull:
                professional_issues.append(outcome[1])

        if professional_issues:
            qa_items.append(f"QA 2: The following Professional outcomes have a Bloom level less than 3: {professional_issues}")
            pass_fail.append("Fail")
        else:
            qa_items.append("QA 2: All specified Professional outcomes have a Bloom level of at least 3.")
            pass_fail.append("Pass")

        # QA 3: Core - ICT Project Management, Cyber Security should be at least level 3
        core_issues = []
        for outcome in [('Core', 'ICT Project Management'), ('Core', 'Cyber Security')]:
            if table_2_df[outcome].dropna().astype(float).lt(3).any() or table_2_df[outcome].isnull:
                core_issues.append(outcome[1])

        if core_issues:
            qa_items.append(f"QA 3: The following Core outcomes have a Bloom level less than 3: {core_issues}")
            pass_fail.append("Fail")
        else:
            qa_items.append("QA 3: All specified Core outcomes have a Bloom level of at least 3.")
            pass_fail.append("Pass")

        data = {
            'QA Item': qa_items,
            'Pass/Fail': pass_fail
        }
        self.criterion_qa_df = pd.DataFrame(data)
        
    def __create_criterion_c(self):
        outcomes_mappings_df_copy = self.outcomes_mappings_df.copy()
        outcomes_mappings_df_copy = outcomes_mappings_df_copy[outcomes_mappings_df_copy['Outcome Group'].isin(['CBoK-Core', 'CBoK-Professional', 'CBoK-Depth'])]
        
        merged_df = pd.merge(self.unit_details_dict, outcomes_mappings_df_copy, on='Unit Code', how='inner')
        merged_df.rename(columns={'Unit Name_x': 'Unit Name'}, inplace=True)
        
        # Create Table 1
        # The outcome names here might be inconsistent with the 'Outcome' column from 'Outcomes Mappings'. Adjust the names if necessary. Same for Outcome Groups.
        knowledge_types_outcomes = [
            ('Professional', 'ICT Ethics'),
            ('Professional', 'Impacts of ICT'),
            ('Professional', 'Working Individually & Teamwork'),
            ('Professional', 'Professional Communication'),
            ('Professional', 'Professional Practitioner'),
            ('Core', 'ICT Fundamentals'),
            ('Core', 'ICT Infrastructure'),
            ('Core', 'Information & Data Science & Engineering'),
            ('Core', 'Computational Science & Engineering'),
            ('Core', 'Application Systems'),
            ('Core', 'Cyber Security'),
            ('Core', 'ICT Project Management'),
            ('Core', 'ICT management & governance'),
            ('Depth', 'In-depth ICT Knowledge')
        ]
        
        # Create a list to append the data for Table 1
        table_1_data = []
        
        # Iterate over the ICT Knowledge Types and Outcome and filter the DataFrame to get the rows that match the Outcome and Outcome Group
        for knowledge_type, outcome in knowledge_types_outcomes:
            matching_rows = merged_df[
                (merged_df['Outcome'] == outcome) & 
                (merged_df['Outcome Group'].str.contains(knowledge_type, case=False))
            ]
            
            # Check if there are any matching rows. If so, create a string of Unit Code + Unit Name
            if not matching_rows.empty:
                unit_code_name_list = matching_rows.apply(lambda row: f"{row['Unit Code']} {row['Unit Name']}", axis=1).tolist()
                unit_code_name = ', '.join(unit_code_name_list)
            else:
                unit_code_name = ""
            
            table_1_data.append([knowledge_type, outcome, unit_code_name])

        self.table_1_df = pd.DataFrame(table_1_data, columns=['ICT Knowledge Types', 'Outcome', 'Unit Code + Unit Name'])
        
        # Create Table 2
        # The outcome names here might be inconsistent with the 'Outcome' column from 'Outcomes Mappings'. Adjust the names if necessary. Same for Outcome Groups.
        columns_table_2 = pd.MultiIndex.from_tuples([
            ('Professional', 'ICT Ethics'),
            ('Professional', 'Impacts of ICT'),
            ('Professional', 'Working Individually & Teamwork'),
            ('Professional', 'Professional Communication'),
            ('Professional', 'Professional Practitioner'),
            ('Core', 'ICT Fundamentals'),
            ('Core', 'ICT Infrastructure'),
            ('Core', 'Information & Data Science & Engineering'),
            ('Core', 'Computational Science & Engineering'),
            ('Core', 'Application Systems'),
            ('Core', 'Cyber Security'),
            ('Core', 'ICT Project Management'),
            ('Core', 'ICT management & governance'),
            ('Depth', 'In-depth ICT Knowledge')
        ])
        
        # Create rows for the pivot table
        merged_df['Unit Code + Unit Name'] = merged_df.apply(lambda row: f"{row['Unit Code']}: {row['Unit Name']}", axis=1)

        index_table_2 = merged_df[['Unit Code', 'Unit Name']].drop_duplicates()
        index_table_2 = index_table_2.apply(lambda row: f"{row['Unit Code']}: {row['Unit Name']}", axis=1)
        
        # Fill the pivot table with the Level (SFIA/Bloom) values
        table_2_data = pd.DataFrame(index=index_table_2, columns=columns_table_2)
        
        # Iterate over the columns in the table and fill the cell with the Level (SFIA/Bloom) value
        for idx, row in merged_df.iterrows():
            subject_name = f"{row['Unit Code']}: {row['Unit Name']}"
            for (knowledge_type, outcome_type) in columns_table_2:
                if outcome_type == row['Outcome'] and knowledge_type in row['Outcome Group']:
                    # Changed 07/10
                    #table_2_data.loc[subject_name, (knowledge_type, outcome_type)] = row['Level (SFIA/Bloom)']
                    table_2_data.loc[subject_name, (knowledge_type, outcome_type)] = row['Level (SFIA/Bloom/UnitOutcome)']
        
        # Create a DataFrame from the list
        self.table_2_df = table_2_data
        
        # Create Table 3
        table_3_data = []
        
        for idx, row in merged_df.iterrows():
            table_3_data.append([f"{row['Unit Code']} {row['Unit Name']}", row['Outcome Group'], row['Outcome'], row['Justification']])
        
        self.table_3_df = pd.DataFrame(table_3_data, columns=['Unit Code + Unit Name', 'Outcome Group', 'Outcome', 'Justification'])
        
    
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

def __extract_identifiers__( title):
    words = title.strip().split()
    # Is this postgraduate with specialisation or postgraduate or a major
    if words[-2].isdigit():
        return [ words[-2], words[-1] ]
    # Postraduate with no specialisation
    elif words[-1].isdigit():
        return [ words[-1], 'None' ]
    # Major
    elif '-' in words[-1]:
        return [ words[-1] ]
    # No valid identifiers
    else:
        return []

    
class KnowledgeBase:
    def __init__(self, kb_excel_file, sfia, cd):
        self.__sfia = sfia
        self.__cd = cd

        #Outcomes Mappings
        outcomes_mappings_df = df = pd.read_excel(kb_excel_file, header=0, sheet_name='Outcomes Mappings')
        # Outcomes Details
        outcomes_details_df = pd.read_excel(kb_excel_file, header=0, sheet_name='Outcomes Details')
        # Unit details
        self.unit_details_dict = self.__load_unit_details(kb_excel_file)

        # Some necessary data cleaning
        outcomes_mappings_df.dropna(subset=['Unit Code'], inplace=True)
        outcomes_details_df.dropna(subset=['Outcome Group'], inplace=True)

        # Load the SFIA Justifications sheet (for rows that have tags instead of direct justifications)
        sfia_justifications = pd.read_excel(kb_excel_file, sheet_name='SFIA justifications')

        self.criterionA = {}
        self.criterionB = {} 
        self.criterionC = {}
        self.criterionD = {}
        self.criterionE = {}

        for course in self.unit_details_dict.keys():
            self.criterionA[course] = CriterionA( course, self.unit_details_dict[course], outcomes_mappings_df, outcomes_details_df, self.__cd )
            self.criterionB[course] = CriterionB( course, self.unit_details_dict[course], outcomes_mappings_df, outcomes_details_df, sfia_justifications )
            self.criterionC[course] = CriterionC( course, self.unit_details_dict[course], outcomes_mappings_df )
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

####
#        data = {
#            'QA Item': ['Number of outcomes ' +str(num_of_outcomes)+' outcomes (2 required)',
#                        'Number of units ' +str(num_of_criterionB_units)+' units out of ' + str(num_of_units) ],
#            'Pass/Fail': [ str(num_of_outcomes >= 2), 'N/A']
#        }
####
        self.criterion_QA_df = pd.DataFrame( { 'Course': [], 'Criterion' : [],'QA Item': [], 'Pass/Fail': [] })
        self.course_identifiers = {}

        # Define the columns to iterate over
        columns_to_check = all_columns[start_idx:end_idx + 1]

        # Initialize a dictionary to store DataFrames
        dataframes_dict = {}

        # Iterate through the specified columns
        for column in columns_to_check:
            # Check if the header is not NA
            if pd.notna(df[column].name) and not df[column].name.startswith('Unnamed'):
                identifiers = __extract_identifiers__(column)

                # Continue if there are no valid identifiers
                if identifiers == []:
                    print( "Ignoring " + column + " due to lack of correct identifiers")
                    new_row = {'Course': column, 'Criterion' : 'KnowledgeBase','QA Item': 'Identifier for ' + column + ' invalid', 'Pass/Fail': 'Fail'}
                    self.criterion_QA_df.loc[len(self.criterion_QA_df)] = new_row
                    continue

                self.course_identifiers[column] = identifiers

                # Filter rows where the column value is not NA
                filtered_df = df[df[column].notna()]
                filtered_df[column] = filtered_df[column].astype(str).str.strip()
                filtered_df = filtered_df[filtered_df[column]!= '']
                filtered_df = filtered_df.drop([c for c in columns_to_check if c != column], axis=1)

                # Store the filtered DataFrame in the dictionary with the column name as the key
                dataframes_dict[column] = filtered_df

        return dataframes_dict

    