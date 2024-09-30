from sfia import SFIA
from knowledgebase import KnowledgeBase
import pandas as pd

# Skills For the Information Age database
sfia = SFIA('KnowledgeBase\sfiaskills.6.3.en.1.xlsx')

# KnowledgeBase - processes the input from the client
kb = KnowledgeBase( 'KnowledgeBase\CSSE-allprograms-outcome-mappings-20240913.xlsx', sfia)


# for course, criterion in kb.criterionA.items():
#         print( course )
#         print( criterion.criterion_df )
#         print( "QA" )
#         print( criterion.criterion_qa_df )

for course, criterion in kb.criterionC.items():
        print(course)
        print(criterion.table_1_df)
        print(criterion.table_2_df)
        print(criterion.table_3_df)
        print(criterion.criterion_qa_df)
        
# A test to write all courses for criterion C into a single excel sheet
# with pd.ExcelWriter('output_criterionC_combined_fixed.xlsx', engine='xlsxwriter') as writer:
#     startrow = 0  
    
#     for course, criterion in kb.criterionC.items():
        
#         course_title = pd.DataFrame([[f"Course: {course}"]])
#         course_title.to_excel(writer, sheet_name='Combined_CriterionC', startrow=startrow, header=False, index=False)
#         startrow += 1  
        
#         # write table 1
#         criterion.table_1_df.to_excel(writer, sheet_name='Combined_CriterionC', startrow=startrow, index=False)
#         startrow += len(criterion.table_1_df) + 2  

#         # write table 2
#         criterion.table_2_df.to_excel(writer, sheet_name='Combined_CriterionC', startrow=startrow)
#         startrow += len(criterion.table_2_df) + 3  
        
#         # write table 3
#         criterion.table_3_df.to_excel(writer, sheet_name='Combined_CriterionC', startrow=startrow, index=False)
#         startrow += len(criterion.table_3_df) + 3

# print('Finished writing all courses into a single sheet.')