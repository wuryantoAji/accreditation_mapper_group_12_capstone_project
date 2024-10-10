from sfia import SFIA
from knowledgebase import KnowledgeBase
from caidi import CAIDI

# Skills For the Information Age database
sfia = SFIA('KnowledgeBase/sfia_v8_custom.xlsx')

cd = CAIDI("caidi-data-for-ACS-A.zip")
# KnowledgeBase - processes the input from the client
kb = KnowledgeBase( 'KnowledgeBase/CSSE-allprograms-outcome-mappings-20241001.xlsx', sfia, cd)


# for course, criterion in kb.criterionC.items():
#         print( course )
#         print( criterion.criterion_df )
#         print( "QA" )
#         print( criterion.criterion_qa_df )

for course, criterion in kb.criterionC.items():
        print(course)
       
        print(criterion.table_2_df)

