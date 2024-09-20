from sfia import SFIA
from knowledgebase import KnowledgeBase
import pandas as pd
from jinja2 import Template

# Step 1: Extract data and store it as a DataFrame

# Skills For the Information Age database
sfia = SFIA('KnowledgeBase/sfiaskills.6.3.en.1.xlsx')

# KnowledgeBase - processes the input from the client
kb = KnowledgeBase('KnowledgeBase/CSSE-allprograms-outcome-mappings-20240821.xlsx', sfia)

# Assume your KnowledgeBase object and data processing part have been initialized
data_frames = []

# Iterate over criterionD data and extract DataFrame
for course, criterion in kb.criterionD.items():
    print(f"Processing course: {course}")
    
    df = criterion.criterion_df
    if df is not None and not df.empty:
        df['Course Title'] = course  # Add a 'Course Title' column to the DataFrame
        df['Unit Code & Title'] = df['Unit Code'] + ' ' + df['Unit Name']  # Combine 'Unit Code' and 'Unit Name'
        
        # Split 'Justification' by period into 'Complex Computing Criteria met' and 'Assessment Item'
        def split_justification(justification):
            if '.' in justification:
                parts = justification.split('.', 1)
                complex_computing = parts[0].strip()  # Part before the period
                assessment_item = parts[1].strip()  # Part after the period
                return complex_computing, assessment_item
            else:
                return "", justification  # If only one sentence, 'Complex Computing Criteria met' is empty, entire sentence is 'Assessment Item'
            
        df[['Complex Computing Criteria met', 'Assessment Item']] = df['Justification'].apply(
            lambda x: pd.Series(split_justification(x))
        )
        
        data_frames.append(df)

# Combine all DataFrames
if data_frames:
    combined_df = pd.concat(data_frames)

    # Group by 'Course Title'
    grouped = combined_df.groupby('Course Title')

    # Jinja2 HTML template
    html_template = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced ICT Units Addressing Complex Computing</title>
    <link rel="stylesheet" href="criterion.css">
</head>
<body>

    {% for course_title, units in courses.items() %}
    <h1>{{ course_title }}</h1>

    <table border="1" cellpadding="10">
        <thead>
            <tr class="title-row">
                <td colspan="3">Criterion D: Advanced ICT Units Addressing Complex Computing</td>
            </tr>
            <tr>
                <th>Unit Code & Title</th>
                <th>Assessment Item</th>
                <th>Complex Computing Criteria met</th>
            </tr>
        </thead>
        <tbody>
            {% for unit in units %}
            <tr>
                <td>{{ unit['Unit Code & Title'] }}</td>
                <td>{{ unit['Assessment Item'] }}</td>
                <td>{{ unit['Complex Computing Criteria met'] }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% endfor %}

</body>
</html>
    """

    # Data preparation: group by 'Course Title', generate data structure for rendering
    courses = {}
    for course_title, group in grouped:
        courses[course_title] = group.to_dict(orient='records')

    # Render HTML template
    template = Template(html_template)
    html_output = template.render(courses=courses)

    # Write HTML to file
    with open("output_criterion_D.html", "w") as f:
        f.write(html_output)

    print("HTML file output_criterion_D.html generated successfully.")

else:
    print("No data found in criterionD.")
