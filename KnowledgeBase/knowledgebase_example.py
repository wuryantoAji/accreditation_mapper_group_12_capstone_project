from sfia import SFIA
from knowledgebase import KnowledgeBase

# Skills For the Information Age database
sfia = SFIA('sfiaskills.6.3.en.1.xlsx')

# KnowledgeBase - processes the input from the client
kb = KnowledgeBase( 'CSSE-allprograms-outcome-mappings-20240821.xlsx', sfia)


# Example code, print Criterion A to screen.
for course, criterion in kb.criterionA.items():
    print( course )
    print( criterion.criterion_df )
    print( "QA" )
    print( criterion.criterion_qa_df )