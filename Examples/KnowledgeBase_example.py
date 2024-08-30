from sfia import SFIA
from knowledgebase import KnowledgeBase

# Skills For the Information Age database
sfia = SFIA('sfiaskills.6.3.en.1.xlsx')

# KnowledgeBase - processes the input from the client
kb = KnowledgeBase( 'CSSE-allprograms-outcome-mappings-20240821.xlsx', sfia)


# Example code, print Criterion B to screen.
for course, criterionB in kb.criterionB.items():
    print( course )
    print( criterionB.criterion_df )
    print( criterionB.criterion_qa_df )
