from sfia import SFIA
from knowledgebase import KnowledgeBase
from caidi import CAIDI

# Skills For the Information Age database
sfia = SFIA('sfia_v8_custom.xlsx')

# CAIDI processing
cd = CAIDI("caidi-data-for-ACS-A.zip")

# KnowledgeBase - processes the input from the client
kb = KnowledgeBase('CSSE-allprograms-outcome-mappings-20241011.xlsx', sfia, cd)

# Example code to iterate through Criterion A and process its data

for course, criterion in kb.criterionA.items():
    print(f"Processing course: {course}")
    
    # Get the DataFrame for Criterion A
    df = criterion.criterion_df
    
    # Ensure we are not working on a slice by using .loc
    df = df.copy()  # Make sure we're working on a copy of the DataFrame
    
    # Strip whitespace from strings in the columns (fixing the SettingWithCopyWarning issue)
    for column in df.columns:
        if df[column].dtype == 'object':  # Only strip strings
            df.loc[:, column] = df[column].astype(str).str.strip()
    
    # Example modification to add 'Complete Outcome' column
    if 'Outcome' in df.columns and 'Outcome Description' in df.columns:
        df.loc[:, 'Complete Outcome'] = df['Outcome'] + "\n" + df['Outcome Description']
    
    # Print to confirm changes
    print(df.head())

    print("QA DataFrame:")
    print(criterion.criterion_qa_df)

    try:
        # Accessing the metadata
        code = criterion.code
        award_title = criterion.award_title
        eft = criterion.eft
        first_year_offered = criterion.first_year_offered
        program_chair = criterion.program_chair
        industry_liasion = criterion.industry_liasion
        key_academic_staff = criterion.key_academic_staff
        outcomes = criterion.outcomes
        justification = criterion.justification
        
        # Print the metadata for debugging
        print(f"Code: {code}")
        print(f"Award Title: {award_title}")
        print(f"EFT Years: {eft}")
        print(f"First Year Offered: {first_year_offered}")
        print(f"Program Chair: {program_chair}")
        print(f"Industry Liaison: {industry_liasion}")
        print(f"Key Academic Staff: {key_academic_staff}")
        print(f"Outcomes: {outcomes}")
        print(f"Justification: {justification}")

    except AttributeError as e:
        # If any attributes are missing, handle it gracefully
        print(f"Missing attribute in course {course}: {e}")
