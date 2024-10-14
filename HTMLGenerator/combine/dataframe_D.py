from sfia import SFIA
from knowledgebase import KnowledgeBase
import pandas as pd
from caidi import CAIDI


 
# CAIDI dataset
cd = CAIDI( 'caidi-data-for-ACS-A.zip')

# Skills For the Information Age database
sfia = SFIA('sfia_v8_custom.xlsx')

# KnowledgeBase - processes the input from the client
kb = KnowledgeBase('CSSE-allprograms-outcome-mappings-20241011.xlsx', sfia, cd)

# Step 1: store all the dataframes in a list
data_frames = []

# loop through course data and save DataFrame
for course, criterion in kb.criterionD.items():
    print(f"Processing course: {course}")
    
    df = criterion.criterion_df
    if df is not None and not df.empty:
        # extract course code and title from course name
        course_code = course.split()[-1]  
        course_title = " ".join(course.split()[:-1])  
        df['Course Code'] = course_code
        df['Course Title'] = course_title
        data_frames.append(df)  

# Step 2: combine DataFrame
if data_frames:
    combined_df = pd.concat(data_frames)

    # # Step 3: use Jinja2 to generate HTML
    html_output = combined_df.to_html(index=False, classes='table', border=1, justify='center')

else:
    print("input data is empty")
