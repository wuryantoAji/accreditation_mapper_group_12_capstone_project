from sfia import SFIA
from knowledgebase import KnowledgeBase
import pandas as pd
from jinja2 import Template

# Step 1: Extract data and store it as a DataFrame

# Skills For the Information Age database
sfia = SFIA('KnowledgeBase/sfiaskills.6.3.en.1.xlsx')

# KnowledgeBase - processes the input from the client
kb = KnowledgeBase('KnowledgeBase/CSSE-allprograms-outcome-mappings-20240821.xlsx', sfia)


data_frames = []

# Loop through course data and save DataFrame
for course, criterion in kb.criterionA.items():
    print(f"Processing course: {course}")
    
    df = criterion.criterion_df
    if df is not None and not df.empty:
        df['Course'] = course  
        data_frames.append(df)  

# combine DataFrame
if data_frames:
    combined_df = pd.concat(data_frames)

    # Step 2: use Jinja2 to generate HTML 

    # group by course and level
    grouped = combined_df.groupby(['Course', 'Level'])


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
        <div class="section-title">Program Details</div>
        <table border="1" cellpadding="10">
            <tr>
                <td class="back_color space">Code</td>
                <td>{{ course_data.code }}</td>  
            </tr>
            <tr>
                <td class="back_color">Award Title on Transcript/Testamur</td>
                <td>{{ course_data.title }}</td>  
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
                        <li>{{ course_data.outcome_1 }}</li>
                        <li>{{ course_data.outcome_2 }}</li>
                        <li>{{ course_data.outcome_3 }}</li>
                    </ol>
                </td>
            </tr>
        </table>
    </div>

    <div class="unit-sequence">
        <div class="section-title">Unit Sequence</div>
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
                <!-- Dynamically display different levels for each course -->
                {% for level, units in course_data.levels.items() %}
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
    </div>

    <!-- Justification of Program Design -->
    <div class="justification">
        <div class="section-title">Justification of Program Design</div>
        <table border="1" cellpadding="10" width="100%">
            <tr>
                <td>
                    <!-- Your Justification of Program Design text here -->
                    <p>
                        placeholder text
                    </p>
                </td>
            </tr>
        </table>
    </div>

    {% endfor %}
</body>
</html>
    """

    # render Jinja2 template with data
    courses = {}
    for (course, level), group in grouped:
        course_code = course.split()[-1] 
        course_title = " ".join(course.split()[:-1])  

        if course_code not in courses:
            courses[course_code] = {
                "code": course_code, 
                "title": course_title,
                "eft_years": "",  
                "first_year": "",  
                "program_chair": "",  
                "ict_industry_liaison": "",  
                "key_academic_staff": "",  
                "outcome_1": "", 
                "outcome_2": "",  
                "outcome_3": "", 
                "levels": {}
            }
        # store data in courses dictionary
        courses[course_code]["levels"][level] = group.to_dict(orient='records')

    # render Jinja2 template with data
    template = Template(html_template)
    html_output = template.render(courses=courses)

    # write HTML output to file
    with open("output_program_details.html", "w") as f:
        f.write(html_output)

    print("output_program_details.html")

else:
    print("input data is empty")
