from sfia import SFIA
from knowledgebase import KnowledgeBase

# Skills For the Information Age database
sfia = SFIA('KnowledgeBase\sfia_v8_custom.xlsx')

# KnowledgeBase - processes the input from the client
kb = KnowledgeBase( 'KnowledgeBase\CSSE-allprograms-outcome-mappings-20241001.xlsx', sfia)


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