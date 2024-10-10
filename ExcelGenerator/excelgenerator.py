from sfia import SFIA
from knowledgebase import KnowledgeBase
import io
import zipfile
import argparse
import pandas as pd
from caidi import CAIDI

# Create the parser
parser = argparse.ArgumentParser(description="Program to create ACS criterion Excel file from input Excel file.")

# Add arguments
parser.add_argument('-k', '--knowledge', type=str, help='The Knowledge Base input file', required=True)
parser.add_argument('-s', '--sfia', type=str, help='The SFIA input file', required=True)
parser.add_argument('-c', '--caidi', type=str, help='The CAIDI input zip file', required=True)
parser.add_argument('-o', '--output', type=str, help='The output file', default='output.zip', required=True)

# Parse the arguments
args = parser.parse_args()

# Use the arguments
print(f"Knowledge base input file: {args.knowledge}")
print(f"CAIDI input file: {args.caidi}")
print(f"SFIA input file: {args.sfia}")
print(f"Output file: {args.output}")

#input_excel_file = args.input
output_zip_file = args.output

# Skills For the Information Age database
sfia = SFIA(args.sfia)

# CAIDI dataset
cd = CAIDI( args.caidi )

# KnowledgeBase - processes the input from the client
kb = KnowledgeBase( args.knowledge, sfia, cd)


with zipfile.ZipFile(output_zip_file, 'w') as output_zip:
    for course, units_df in kb.unit_details_dict.items():
        print( course )
        # Create a BytesIO buffer to hold the Excel file
        excel_buffer = io.BytesIO()

        # Write the DataFrame to the Excel buffer
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            startrow = 0
            kb.unit_details_dict[course].to_excel(writer, sheet_name='Units', index=False)
            kb.criterionA[course].criterion_df.to_excel(writer, sheet_name='CriterionA', index=False)
            kb.criterionA[course].criterion_qa_df.to_excel(writer, sheet_name='CriterionA_QA', index=False)
            kb.criterionB[course].criterion_df.to_excel(writer, sheet_name='CriterionB', index=False)
            kb.criterionB[course].criterion_qa_df.to_excel(writer, sheet_name='CriterionB_QA', index=False)
            kb.criterionC[course].table_1_df.to_excel(writer, sheet_name='CriterionC', startrow=startrow, index=False)
            startrow += len(kb.criterionC[course].table_1_df) + 2
            kb.criterionC[course].table_2_df.to_excel(writer, sheet_name='CriterionC', startrow=startrow, index=True)
            startrow += len(kb.criterionC[course].table_2_df) + 4  
            kb.criterionC[course].table_3_df.to_excel(writer, sheet_name='CriterionC', startrow=startrow, index=False)
            kb.criterionC[course].criterion_qa_df.to_excel(writer, sheet_name='CriterionC_QA', index=False)
            kb.criterionD[course].criterion_df.to_excel(writer, sheet_name='CriterionD', index=False)
            kb.criterionD[course].criterion_qa_df.to_excel(writer, sheet_name='CriterionD_QA', index=False)
            kb.criterionE[course].criterion_df.to_excel(writer, sheet_name='CriterionE', index=False)
            kb.criterionE[course].criterion_qa_df.to_excel(writer, sheet_name='CriterionE_QA', index=False)

            # Iterate through all worksheets and set the column width automatically
            # Only applicable when using xlsxwriter as the engine
            for sheet_name, worksheet in writer.sheets.items():
                worksheet.autofit()
                
        # Seek to the beginning of the BytesIO buffer
        excel_buffer.seek(0)

        output_zip.writestr(course+'.xlsx', excel_buffer.getvalue())

    all_criterion_QA_df =pd.DataFrame(columns=['Course', 'Criterion', 'QA Item', 'Pass/Fail' ])
    # Create a BytesIO buffer to hold the Excel file
    excel_buffer = io.BytesIO()
    criterion_A_QA_df =pd.DataFrame(columns=['Course', 'Criterion', 'QA Item', 'Pass/Fail' ])
    for course, criterion in kb.criterionA.items():
        criterion_QA_df =pd.DataFrame(columns=['Course', 'Criterion', 'QA Item', 'Pass/Fail' ])
        criterion_QA_df = pd.concat([criterion_QA_df, criterion.criterion_qa_df], ignore_index=True)
        criterion_QA_df['Criterion'] = 'A'
        criterion_QA_df['Course'] = course
        criterion_A_QA_df = pd.concat([criterion_QA_df, criterion_A_QA_df], ignore_index=True)
    all_criterion_QA_df = pd.concat([all_criterion_QA_df, criterion_A_QA_df], ignore_index=True)
    
    criterion_B_QA_df =pd.DataFrame(columns=['Course', 'Criterion', 'QA Item', 'Pass/Fail' ])
    for course, criterion in kb.criterionB.items():
        criterion_QA_df =pd.DataFrame(columns=['Course', 'Criterion', 'QA Item', 'Pass/Fail' ])
        criterion_QA_df = pd.concat([criterion_QA_df, criterion.criterion_qa_df], ignore_index=True)
        criterion_QA_df['Criterion'] = 'B'
        criterion_QA_df['Course'] = course
        criterion_B_QA_df = pd.concat([criterion_QA_df, criterion_B_QA_df], ignore_index=True)
    all_criterion_QA_df = pd.concat([all_criterion_QA_df, criterion_B_QA_df], ignore_index=True)
    
    criterion_C_QA_df =pd.DataFrame(columns=['Course', 'Criterion', 'QA Item', 'Pass/Fail' ])
    for course, criterion in kb.criterionC.items():
        criterion_QA_df =pd.DataFrame(columns=['Course', 'Criterion', 'QA Item', 'Pass/Fail' ])
        criterion_QA_df = pd.concat([criterion_QA_df, criterion.criterion_qa_df], ignore_index=True)
        criterion_QA_df['Criterion'] = 'C'
        criterion_QA_df['Course'] = course
        criterion_C_QA_df = pd.concat([criterion_QA_df, criterion_C_QA_df], ignore_index=True)
    all_criterion_QA_df = pd.concat([all_criterion_QA_df, criterion_C_QA_df], ignore_index=True)

    criterion_D_QA_df =pd.DataFrame(columns=['Course', 'Criterion', 'QA Item', 'Pass/Fail' ])
    for course, criterion in kb.criterionD.items():
        criterion_QA_df =pd.DataFrame(columns=['Course', 'Criterion', 'QA Item', 'Pass/Fail' ])
        criterion_QA_df = pd.concat([criterion_QA_df, criterion.criterion_qa_df], ignore_index=True)
        criterion_QA_df['Criterion'] = 'D'
        criterion_QA_df['Course'] = course
        criterion_D_QA_df = pd.concat([criterion_QA_df, criterion_D_QA_df], ignore_index=True)
    all_criterion_QA_df = pd.concat([all_criterion_QA_df, criterion_D_QA_df], ignore_index=True)
    
    criterion_E_QA_df =pd.DataFrame(columns=['Course', 'Criterion', 'QA Item', 'Pass/Fail' ])
    for course, criterion in kb.criterionE.items():
        criterion_QA_df =pd.DataFrame(columns=['Course', 'Criterion', 'QA Item', 'Pass/Fail' ])
        criterion_QA_df = pd.concat([criterion_QA_df, criterion.criterion_qa_df], ignore_index=True)
        criterion_QA_df['Criterion'] = 'E'
        criterion_QA_df['Course'] = course
        criterion_E_QA_df = pd.concat([criterion_QA_df, criterion_E_QA_df], ignore_index=True)
    all_criterion_QA_df = pd.concat([all_criterion_QA_df, criterion_E_QA_df], ignore_index=True)

    all_criterion_QA_df = pd.concat([all_criterion_QA_df, kb.criterion_QA_df], ignore_index=True)

    # Write the DataFrame to the Excel buffer
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        all_criterion_QA_df.to_excel(writer, sheet_name='QA', index=False)

    # Seek to the beginning of the BytesIO buffer
    excel_buffer.seek(0)

    output_zip.writestr('criterion_QA.xlsx', excel_buffer.getvalue())
