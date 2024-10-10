import argparse
import itertools
import re
import os
import io
import zipfile
import pandas as pd



CRITERION_B_ELEMENTS = { 'PROG': 'Programming/Software Development', 
                        'PRMG': 'Project Management', 
                        'DESN': 'System Design'}

def check_criterion_b(unit_details_dict, criterionB):
   criterionB_QA = {}
   for course, criterionB_df in criterionB.items():
        num_of_outcomes = criterionB_df['Outcome'].nunique()
        num_of_criterionB_units = criterionB_df['Unit Code & Title'].nunique()  
        num_of_units = unit_details_dict[course]['Unit Code'].nunique()  
        data = {
            'QA Item': ['Number of outcomes ' +str(num_of_outcomes)+' outcomes (2 required)',
                        'Number of units ' +str(num_of_criterionB_units)+' units out of ' + str(num_of_units) ],
            'Pass/Fail': [ str(num_of_outcomes >= 2), 'N/A']
         }
        criterionB_QA[course] = pd.DataFrame(data)

   return criterionB_QA

def create_criterionB(outcomes_mappings_df, unit_details_dict, outcomes_details_df):
    criterionB = {}
    for course, unit_df in unit_details_dict.items():
        outcomes_mappings_df_copy = outcomes_mappings_df.copy()

        #Remove N/A Level (SFIA/Bloom/UnitOutcome) and convert the rest to Ints
        outcomes_mappings_df_copy.dropna(subset=['Level (SFIA/Bloom/UnitOutcome)'], inplace=True)
        outcomes_mappings_df_copy['Level (SFIA/Bloom/UnitOutcome)'] = pd.to_numeric(outcomes_mappings_df_copy['Level (SFIA/Bloom/UnitOutcome)'], errors='coerce').fillna(0).astype(int)

        # Concatenate Unit Code and Unit Title
        outcomes_mappings_df_copy['Unit Code & Title'] = outcomes_mappings_df['Unit Code'].astype(str) + ' ' + outcomes_mappings_df['Unit Name'].astype(str)
        filtered_outcomes_mappings_df_copy = outcomes_mappings_df_copy[outcomes_mappings_df_copy['Outcome'].isin(CRITERION_B_ELEMENTS)]
       
        merged_df = pd.merge(unit_df, filtered_outcomes_mappings_df_copy, on='Unit Code', how='inner')
        merged_df.drop(columns=['Outcome Group', 'Unit Code', 'Unit Name_y', 'Unit Name_x', 'Level', 'Semester', 'Justification TODO (check 2021 submission)'], inplace=True)
        merged_df.drop(columns=unit_details_dict.keys(), inplace=True)
        sorted_df = merged_df.groupby('Outcome').apply(lambda x: x.sort_values(by='Outcome')).reset_index(drop=True)

        group_column = 'Outcome'
        value_column = 'Level (SFIA/Bloom/UnitOutcome)'

        # Group by the specified column and find the maximum value for each group
        max_values = sorted_df.groupby(group_column)[value_column].transform('max')

        # Retain rows where the value column is equal to the maximum value within its group
        result_df = sorted_df[sorted_df[value_column] == max_values]

        criterionB[course] = result_df

    return criterionB


def load_unit_details(excel):
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
        

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="Program to create ACS criterion Excel file from input Excel file.")

    # Add arguments
    parser.add_argument('-i', '--input', type=str, help='The input file', default='input.xlsx')
    parser.add_argument('-o', '--output', type=str, help='The output file', default='output.docx')
    
    # Parse the arguments
    args = parser.parse_args()

    # Use the arguments
    print(f"Input file: {args.input}")
    print(f"Output file: {args.output}")

    input_excel_file = args.input
    output_zip_file = args.output

    #Outcomes Mappings
    outcomes_mappings_df = df = pd.read_excel(input_excel_file, header=0, sheet_name='Outcomes Mappings')
    # Unit Details
    unit_details_df =  pd.read_excel(input_excel_file, header=0, sheet_name='Unit Details')
    # Outcomes Details
    outcomes_details_df = pd.read_excel(input_excel_file, header=1, sheet_name='Outcomes Details')

    outcomes_mappings_df.dropna(subset=['Unit Code'], inplace=True)
    unit_details_df.dropna(subset=['Unit Code'], inplace=True)
    outcomes_details_df.dropna(subset=['Outcome Group'], inplace=True)
    
    criterion = [ 'CriterionA', 'CriterionB', 'CriterionC', 'CriterionD', 'CriterionE' ]

    unit_details_dict = load_unit_details(input_excel_file)

    criterionB = create_criterionB(outcomes_mappings_df, unit_details_dict, outcomes_details_df)
    criterionB_QA = check_criterion_b(unit_details_dict, criterionB)

    with zipfile.ZipFile(output_zip_file, 'w') as output_zip:
        for course, units_df in unit_details_dict.items():
            print( course )
            # Create a BytesIO buffer to hold the Excel file
            excel_buffer = io.BytesIO()

            # Write the DataFrame to the Excel buffer
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                unit_details_dict[course].to_excel(writer, sheet_name='Units', index=False)
                criterionB[course].to_excel(writer, sheet_name='CriterionB', index=False)
                criterionB_QA[course].to_excel(writer, sheet_name='CriterionB_QA', index=False)

            # Seek to the beginning of the BytesIO buffer
            excel_buffer.seek(0)

            output_zip.writestr(course+'.xlsx', excel_buffer.getvalue())

        criterion_QA_df =pd.DataFrame(columns=['QA Item', 'Pass/Fail', 'Criterion', 'Course'])
        # Create a BytesIO buffer to hold the Excel file
        excel_buffer = io.BytesIO()
        for course, criterion_df in criterionB_QA.items():
            criterion_df['Criterion'] = 'B'
            criterion_df['Course'] = course
            criterion_QA_df = pd.concat([criterion_QA_df, criterion_df], ignore_index=True)

        # Write the DataFrame to the Excel buffer
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            criterion_QA_df.to_excel(writer, sheet_name='QA', index=False)

        # Seek to the beginning of the BytesIO buffer
        excel_buffer.seek(0)

        output_zip.writestr('criterion_QA.xlsx', excel_buffer.getvalue())

if __name__ == "__main__":
    main()
  
