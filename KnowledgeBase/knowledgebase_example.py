from sfia import SFIA
from knowledgebase import KnowledgeBase

# Skills For the Information Age database
sfia = SFIA('sfiaskills.6.3.en.1.xlsx')

# KnowledgeBase - processes the input from the client
kb = KnowledgeBase( 'CSSE-allprograms-outcome-mappings-20240913.xlsx', sfia)

# for course, criterion in kb.criterionA.items():
#     print( course )
#     print( criterion.criterion_df )
#     print( "QA" )
#     print( criterion.criterion_qa_df )
    
for course, criterion in kb.criterionC.items():
        print(course)
        print(criterion.table_1_df)
        print(criterion.table_2_df)
