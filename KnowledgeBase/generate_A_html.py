from sfia import SFIA
from knowledgebase import KnowledgeBase
from caidi import CAIDI
import pandas as pd
from jinja2 import Template

# Step 1: Extract data and store it as a DataFrame

# Skills For the Information Age database
sfia = SFIA('KnowledgeBase/sfia_v8_custom.xlsx')

# CAIDI processing
cd = CAIDI("knowledgebase/caidi-data-for-ACS-A.zip")  # Ensure the correct path to your zip file

# KnowledgeBase - processes the input from the client
kb = KnowledgeBase('KnowledgeBase/CSSE-allprograms-outcome-mappings-20241007.xlsx', sfia, cd)

data_frames = []

# Loop through course data and save DataFrame
for course, criterion in kb.criterionA.items():
    print(f"Processing course: {course}")
    
    # Extract the actual DataFrame from the criterion object
    df = criterion.criterion_df  # Assuming criterion_df is the actual DataFrame we need
    
    if df is not None and not df.empty:
        df['Course'] = course  # Add a 'Course' column
        data_frames.append(df)  # Append DataFrame to the list

# Combine DataFrames if we have data
if data_frames:
    combined_df = pd.concat(data_frames)

    # Step 2: Use Jinja2 to generate HTML 

    # Group by course
    grouped = combined_df.groupby('Course')

    # Define the HTML template
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Program Details Table</title>
        <link rel="stylesheet" href="criterion.css">
    </head>

    <body style="margin: 150px;">
        {% for course_code, course_data in courses.items() %}
        <div class="program-details">
            <div class="section-title">Program Details for {{ course_data.title }}</div>
            <table border="1" cellpadding="10">
                <tr>
                    <td class="back_color space">Code</td>
                    <td>{{ course_data.code }}</td>  
                </tr>
                <tr>
                    <td class="back_color">Award Title on Transcript/Testamur</td>
                    <td>{{ course_data.award_title }}</td>  
                </tr>
                <tr>
                    <td class="back_color">EFT Years of Study</td>
                    <td>{{ course_data.eft_years }}</td>  
                </tr>
                <tr>
                    <td class="back_color">First Year of Offer</td>
                    <td>{{ course_data.first_year }}</td>  
                </tr>
            </table>
        </div>

        <div class="personnel">
            <div class="section-title">Personnel</div>
            <table border="1" cellpadding="10">
                <tr>
                    <td class="back_color space">Program Chair</td>
                    <td>{{ course_data.program_chair }}</td>
                </tr>
                <tr>
                    <td class="back_color">ICT Industry Liaison</td>
                    <td>{{ course_data.ict_industry_liaison }}</td>  
                </tr>
                <tr>
                    <td class="back_color">Key Academic Staff</td>
                    <td>{{ course_data.key_academic_staff }}</td>  
                </tr>
            </table>
        </div>

        <div class="outcomes">
            <div class="section-title">Outcomes</div>
            <table border="1" cellpadding="10">
                <tr>
                    <td>
                        <ol>
                            <li>{{ course_data.outcomes }}</li>  
                        </ol>
                    </td>
                </tr>
            </table>
        </div>

        <div class="unit-sequence">
            <div class="section-title">Unit Sequence</div>

            <!-- Dynamically display different groups within each course -->
            {% for group_name, group_data in course_data.groups.items() %}
            <h3 style="background-color:#90bad944;">{{ group_name }}</h3>
            <table border="1" cellpadding="10">
                <thead>
                    <tr class="back_color">
                        <th></th>
                        <th>Code</th>
                        <th>Title</th>
                        <th>Unit Coordinator(s)</th>
                        <th>File #</th>
                    </tr>
                </thead>
                <tbody>
                    {% for level, units in group_data.levels.items() %}
                    <tr>
                        <td rowspan="{{ units|length + 1 }}" style="writing-mode: vertical-lr; text-align: center; background-color: #90bad944;">LEVEL {{ level }}</td>
                    </tr>
                    {% for unit in units %}
                    <tr>
                        <td>{{ unit['Unit Code'] }}</td>
                        <td>{{ unit['Unit Name'] }}</td>
                        <td>{{ unit['Coordinator'] }}</td>
                        <td>{{ unit['File'] }}</td>
                    </tr>
                    {% endfor %}
                    {% endfor %}
                </tbody>
            </table>
            {% endfor %}
        </div>

        <!-- Justification of Program Design -->
        <div class="justification">
            <div class="section-title">Justification of Program Design</div>
            <table border="1" cellpadding="10" width="100%">
                <tr>
                    <td>
                        <p>{{ course_data.justification }}</p>
                    </td>
                </tr>
            </table>
        </div>

        {% endfor %}
    </body>
    </html>
    """

    # Prepare data for each course and level
    courses = {}
    for course, group in grouped:
        course_code = course.split()[-1]
        course_title = " ".join(course.split()[:-1])

        if course_code not in courses:
            # Extract data from CAIDI, assuming it's available through criterionA
            criterion = kb.criterionA.get(course, None)
            if criterion:
                courses[course_code] = {
                    "code": course_code,
                    "title": course_title,
                    # Ensure each attribute is handled with a fallback for missing data
                    "award_title": getattr(criterion, "award_title", "N/A"),
                    "eft_years": getattr(criterion, "eft", "N/A"),
                    "first_year": getattr(criterion, "first_year_offered", "N/A"),
                    "program_chair": getattr(criterion, "program_chair", "N/A"),
                    "ict_industry_liaison": "Placeholder",  # Example placeholder
                    "key_academic_staff": "Placeholder",  # Example placeholder
                    "outcomes": getattr(criterion, "outcomes", "N/A"),
                    "justification": getattr(criterion, "justification", "N/A"),
                    "groups": {}
                }

        # Group by the new column (with the same name as the course)
        new_column_name = course  # Assuming the new column has the same name as the course
        group_by_new_column = group.groupby(new_column_name)

        # Process each group within the course
        for group_name, group_data in group_by_new_column:
            if group_name not in courses[course_code]["groups"]:
                courses[course_code]["groups"][group_name] = {"levels": {}}

            # Group by 'Level' within each subgroup
            level_grouped = group_data.groupby('Level')
            for level, level_group in level_grouped:
                courses[course_code]["groups"][group_name]["levels"][level] = level_group.to_dict(orient='records')

    # Render Jinja2 template with data
    template = Template(html_template)
    html_output = template.render(courses=courses)

    # Write HTML output to file
    with open("output_program_details.html", "w") as f:
        f.write(html_output)

    print("output_program_details.html")

else:
    print("Input data is empty.")
