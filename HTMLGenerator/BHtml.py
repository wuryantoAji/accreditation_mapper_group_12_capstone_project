import pandas as pd
from sfia import SFIA
from knowledgebase import KnowledgeBase

# Load Skills For the Information Age (SFIA) database from Excel
sfia_data = pd.read_excel('sfiaskills.6.3.en.1.xlsx', usecols=['Skill', 'description', 'description22', 'code', 'level'])

# Drop duplicates based on the 'code' and 'level' columns (keep the first occurrence)
sfia_data_unique = sfia_data.drop_duplicates(subset=['code', 'level'], keep='first')

# Load KnowledgeBase - this processes the input from the client
kb = KnowledgeBase('CSSE-allprograms-outcome-mappings-20240821.xlsx', SFIA('sfiaskills.6.3.en.1.xlsx'))

# Create a dictionary to map SFIA skills to their descriptions (Skill, Description, and Description2)
sfia_skill_data = sfia_data_unique.set_index(['code', 'level']).to_dict(orient='index')

# Prepare HTML content to display course titles, outcomes, levels, and justifications in table format
html_content = """
<html>
<head>
    <title>Course Outcomes, Levels, and Justifications</title>
    <style>
        table {
            width: 80%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
        }
        th {
            background-color: #f2f2f2;
            text-align: left;
        }
    </style>
</head>
<body>
    <h1>Course Information</h1>
"""

# Loop through the courses and add the titles, outcomes, levels, and justifications to the HTML content
for course, criterionB in kb.criterionB.items():
    course_title = f"<h2>{course}</h2>"
    
    # Add the course title to the HTML content
    html_content += course_title

    # Drop duplicates from the criterion DataFrame (based on Outcome, Level, and Justification)
    unique_df = criterionB.criterion_df.drop_duplicates(subset=['Outcome', 'Level (SFIA/Bloom)', 'Justification'])

    # Start a table for outcomes, levels, and justifications with renamed headers
    html_content += """
    <table>
        <tr>
            <th>Code</th>
            <th>Level</th>
            <th>Units Supporting SFIA Skill</th>
            <th>Skill</th>
            <th>Description</th>
            <th>Description2</th>
        </tr>
    """

    # Loop through each unique row in the criterion DataFrame to get outcomes, levels, and justifications
    for _, row in unique_df.iterrows():
        outcome = row['Outcome']  # Renamed as "Code" in the table
        level = row['Level (SFIA/Bloom)']
        justification = row['Justification']  # Renamed as "Units Supporting SFIA Skill"

        # Get the corresponding SFIA skill data based on the Outcome (code) and Level
        sfia_info = sfia_skill_data.get((outcome, level), {'Skill': 'N/A', 'description': 'N/A', 'description22': 'N/A'})

        skill = sfia_info.get('Skill', 'N/A')
        description = sfia_info.get('description', 'N/A')
        description2 = sfia_info.get('description22', 'N/A')

        # Add a row to the table with outcome, level, justification, and SFIA skill information
        html_content += f"""
        <tr>
            <td>{outcome}</td>
            <td>{level}</td>
            <td>{justification}</td>
            <td>{skill}</td>
            <td>{description}</td>
            <td>{description2}</td>
        </tr>
        """
    
    # Close the table for this course
    html_content += "</table>"

# Close the HTML content
html_content += """
</body>
</html>
"""

# Write the HTML content to a new file
output_html_path = 'course_outcomes_filtered_by_sfia.html'
with open(output_html_path, 'w') as f:
    f.write(html_content)

print(f"Filtered course outcomes, levels, and justifications (matched by code and level) have been written to {output_html_path}")
