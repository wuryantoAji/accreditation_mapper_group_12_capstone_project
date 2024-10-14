import pandas as pd
from sfia import SFIA
from knowledgebase import KnowledgeBase
from jinja2 import Template
from caidi import CAIDI

cd = CAIDI( 'caidi-data-for-ACS-A.zip')

# Load Skills For the Information Age (SFIA) database from Excel
sfia_data = pd.read_excel('sfia_v8_custom.xlsx', usecols=['Skill', 'description', 'description22', 'code', 'level'])
sfia_data['description22'] = sfia_data['description22'].str.replace('_x000D_', ' ', regex=False)

# Drop duplicates based on the 'code' and 'level' columns (keep the first occurrence)
sfia_data_unique = sfia_data.drop_duplicates(subset=['code', 'level'], keep='first')

# Load KnowledgeBase - this processes the input from the client
kb = KnowledgeBase('CSSE-allprograms-outcome-mappings-20241011.xlsx', SFIA('sfia_v8_custom.xlsx'), cd)

# Create a dictionary to map SFIA skills to their descriptions (Skill, Description, and Description2)
sfia_skill_data = sfia_data_unique.set_index(['code', 'level']).to_dict(orient='index')

# Main function that generates HTML for a given course
def generate_course_html(course):
    html_content = f"<h2>{course} - Criteria A-E Outcomes</h2>"

    # Criterion A
    html_content += generate_criterion_a_html(course)

    # Criterion B
    html_content += generate_criterion_b_html(kb.criterionB[course].criterion_df)
   
    # Criterion C
    html_content += generate_criterion_c_html(course)

    # Criterion D
    html_content += generate_criterion_d_html(course)

    # Criterion E
    html_content += generate_criterion_e_html(kb.criterionE[course].criterion_df)
    html_content += """
    <style>
    
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }

        th, td {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }

        th {

            font-weight: bold;
            text-align: center;
        }

        td {
            vertical-align: top;
        }

        .quick-nav-container h4 {
            position:absolute;
            color: #FFFFFF;
            font-size: 14px;
            font-weight: bold;
            width: 112px;
            top: 0px;
            left: 0px;
            text-align: center;
            padding: 8px;
        }

        .quick-nav-container a.close {
            position: absolute;
            top: 4px;
            right: -12px;
            width: 16px;
            height: 16px;
            text-decoration: none;
            -moz-border-radius: 8px;
            -webkit-border-radius: 8px;
            border-radius: 8px;
            display: block;
            text-align: center;
            font-weight: bold;
            font-size: 14px;
        }

        .quick-nav {
            position: relative;
            font-size: 10px;
            padding: 20px 90px 20px 20px;
            -moz-border-radius: 4px;
            -webkit-border-radius: 4px;
            border-radius: 4px;
        }

        .quick-nav a {
            text-decoration: none;
            font-size: 14px;
        }

        .quick-nav table th.skew {
            height: 60px;
            width: 40px;
            position: relative;
            vertical-align: bottom;
        }

        .quick-nav table th.skew > div {
            position: relative;
            top: 0px;
            left: 40px;
            height: 140%;
            transform:skew(-45deg,0deg);
            -ms-transform:skew(-45deg,0deg);
            -moz-transform:skew(-45deg,0deg);
            -webkit-transform:skew(-45deg,0deg);
            -o-transform:skew(-45deg,0deg);   
            overflow: hidden;
            border-top: 1px solid #CCCCCC;
            border-left: 1px solid #CCCCCC;
            border-right: 1px solid #CCCCCC;
        }

        .quick-nav table th.skew span {
            transform:skew(45deg,0deg) rotate(315deg);
            -ms-transform:skew(45deg,0deg) rotate(315deg);
            -moz-transform:skew(45deg,0deg) rotate(315deg);
            -webkit-transform:skew(45deg,0deg) rotate(315deg);
            -o-transform:skew(45deg,0deg) rotate(315deg);       
            position: absolute;
            bottom: 15px;
            left: 1px;
            display: inline-block;
            width: 100%;
            text-align: left;
            font-size: 6px;
        }

        .quick-nav table td {
            width: 40px;
            height: 35px;
            text-align: center;
            vertical-align: middle;
            border: 1px solid #CCCCCC;
        }

        .quick-nav table td.project-name {
            width: auto;
            text-align: right;
            font-weight: bold;
            border: none;
            padding-right: 8px;
        }

        .odd {
            background-color: #ecc1b9;
        }

        .colorrgange {
            background-color: #e7cfb6;
        }

        .colorgrenn {
            background-color: #d6e7d3;
        }
        .colorpurple {
            background-color: #eee4f2;
        }

        .colorblue {
            background-color: #d2dbea;
        }
        
    </style>
    """
    return html_content



# Generate HTML for Criterion A with grouping by course_title + course_code
def generate_criterion_a_html(course):
    try:
        # Get the criterionA data for the selected course only
        criterion = kb.criterionA.get(course, None)

        if criterion is None or criterion.criterion_df is None or criterion.criterion_df.empty:
            return "<p>No data available for Criterion A.</p>"

        df = criterion.criterion_df  # Get the DataFrame for the selected course

        # Prepare data for the selected course
        course_code = course
        course_title = " ".join(course.split()[:-1])  # Assuming course format might be like 'Major Code'

        # Create a combined key for course title and course code
        combined_course_key = f"{course_title} {course_code}"

        # Extract other necessary data from the criterion object
        award_title = getattr(criterion, "award_title", "")
        eft_years = getattr(criterion, "eft_years", "")
        first_year = getattr(criterion, "first_year_offered", "")
        program_chair = getattr(criterion, "program_chair", "")
        ict_industry_liaison = "Placeholder"  # Example placeholder
        key_academic_staff = "Placeholder"  # Example placeholder
        outcomes = getattr(criterion, "outcomes", "")
        justification = getattr(criterion, "justification", "")

        # Group the DataFrame by level to organize units
        groups = {}
        if 'Level' in df.columns:
            level_grouped = df.groupby('Level')
            for level, level_group in level_grouped:
                groups[level] = level_group.to_dict(orient='records')
        else:
            groups['N/A'] = df.to_dict(orient='records')  # If no level info is available

        # Define the courses dictionary with the combined course key
        courses = {
            combined_course_key: {
                "code": course_code,
                "title": course_title,
                "award_title": award_title,
                "eft_years": eft_years,
                "first_year": first_year,
                "program_chair": program_chair,
                "ict_industry_liaison": ict_industry_liaison,
                "key_academic_staff": key_academic_staff,
                "outcomes": outcomes,
                "justification": justification,
                "groups": {"Unit Sequence": {"levels": groups}}
            }
        }

        # Define the HTML template (this stays unchanged)
        html_template = """
        <h3>Criteria A</h3>
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Program Details Table</title>
            <style>
            table {
                width: 100%;
                border-collapse: collapse;
            }
            table, th, td {
                border: 1px solid black;
            }
            th, td {
                padding: 10px;
                text-align: left;
            }
            .section-title {
                background-color: #a2bde6;
                font-weight: bold;
                padding: 10px;
                text-transform: uppercase;
            }
             
            .space {
                width: 10%;
            }
            
            body {
                margin: 60px;
            }
            
            /* rotate text */
            .rotate-text {
                transform: rotate(-90deg);
                writing-mode: vertical-lr;
                text-align: center;
            }
            
            
            /* level cells */
            .level-cell {
                background-color: #d3d3d3;
                padding: 10px;
            }
            
            .program-details {
                margin-top: 60px;  
            }
            
            
        
            .title-row td {
                text-align: center;
                font-weight: bold;
                background-color: #a2bde6
            }
            </style>
        </head>
        <body style="margin: 30px;">
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
                            <td>{{ unit.get('Coordinator', '') }}</td>
                            <td>{{ unit.get('File', '') }}</td>
                        </tr>
                        {% endfor %}
                        {% endfor %}
                    </tbody>
                </table>
                {% endfor %}
            </div>
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

        # Render the HTML using Jinja2 template
        template = Template(html_template)
        html_output = template.render(courses=courses)
        print("HTML content rendered successfully for", combined_course_key)
        return html_output

    except Exception as e:
        error_msg = f"An error occurred while generating HTML for Criterion A: {e}"
        print(error_msg)
        return f"<p>{error_msg}</p>"


# Criterion B HTML generation
def generate_criterion_b_html(criterion_b_df):
    if criterion_b_df is not None and not criterion_b_df.empty:
        unique_df = criterion_b_df.drop_duplicates(subset=['Outcome', 'Level (SFIA/Bloom/UnitOutcome)', 'Justification'])
        criterion_html = """
        <h3>Criterion B</h3>
        <table>
            <thead>
                <tr>
                    <th>SFIA Skill</th>
                    <th>Skill Description</th>
                    <th>Level Description</th>
                    <th>Code</th>
                    <th>Level</th>
                    <th>Units Supporting SFIA Skill</th>
                </tr>
            </thead>
            <tbody>
        """
        for _, row in unique_df.iterrows():
            outcome = row['Outcome']
            level = row['Level (SFIA/Bloom/UnitOutcome)']
            justification = row['Justification']
            sfia_info = sfia_skill_data.get((outcome, level), {'Skill': 'N/A', 'description': 'N/A', 'description22': 'N/A'})
            skill = sfia_info.get('Skill', 'N/A')
            description = sfia_info.get('description', 'N/A')
            description2 = sfia_info.get('description22', 'N/A')
            criterion_html += f"""
            <tr>
                <td>{skill}</td>
                <td>{description}</td>
                <td>{description2}</td>
                <td>{outcome}</td>
                <td>{level}</td>
                <td>{justification}</td>
            </tr>
            """
        criterion_html += "</tbody></table>"
        return criterion_html
    return "<p>No data for Criterion B.</p>"
# Criterion C HTML generation
def generate_criterion_c_html(course):
    criterion = kb.criterionC[course]
    if hasattr(criterion, 'table_2_df'):
        df = criterion.table_2_df.copy()

        # Adjust column names based on the number of columns
        if len(df.columns) == 14:
            df.columns = ['ICT Ethics', 'Impacts of ICT', 
                          'Working Individually & Teamwork', 'Professional Communication', 
                          'Professional Practitioner', 'ICT Fundamentals', 'ICT Infrastructure', 
                          'Information & Data Science & Engineering', 'Computational Science & Engineering', 
                          'Application Systems', 'Cyber Security', 'ICT Project Management', 
                          'ICT management & governance', 'In-depth']
            df['Unit Code + Unit Name'] = df.index
        elif len(df.columns) == 15:
            df.columns = ['Unit Code + Unit Name', 'ICT Ethics', 'Impacts of ICT', 
                          'Working Individually & Teamwork', 'Professional Communication', 
                          'Professional Practitioner', 'ICT Fundamentals', 'ICT Infrastructure', 
                          'Information & Data Science & Engineering', 'Computational Science & Engineering', 
                          'Application Systems', 'Cyber Security', 'ICT Project Management', 
                          'ICT management & governance', 'In-depth']
        else:
            print(f"Unexpected number of columns: {len(df.columns)}")
            return "<p>Unexpected data format for Criterion C.</p>"

        # Replace NaN values with empty strings
        df.fillna('', inplace=True)

        # Now, use Jinja2 template to render the HTML
        html_template = """
        <h3>Criterion C</h3>
        <div class="quick-nav-container">
            <div class="quick-nav">
                <table>
                    <thead>
                        <tr>
                            <th>{{ course }}</th>
                            <th class="skew"><div class="odd"><span>ICT Ethics</span></div></th>
                            <th class="skew"><div class="colorrgange"><span>Impacts of ICT</span></div></th>
                            <th class="skew"><div class="colorrgange"><span>Working Individually & Teamwork</span></div></th>
                            <th class="skew"><div class="colorrgange"><span>Professional Communication</span></div></th>
                            <th class="skew"><div class="colorrgange"><span>Professional Practitioner</span></div></th>
                            <th class="skew"><div class="colorgrenn"><span>ICT Fundamentals</span></div></th>
                            <th class="skew"><div class="colorgrenn"><span>ICT Infrastructure</span></div></th>
                            <th class="skew"><div class="colorgrenn"><span>Information & Data Science & Engineering</span></div></th>
                            <th class="skew"><div class="colorgrenn"><span>Computational Science & Engineering</span></div></th>
                            <th class="skew"><div class=""><span>Application Systems</span></div></th>
                            <th class="skew"><div class=""><span>Cyber Security</span></div></th>
                            <th class="skew"><div class="colorgrenn"><span>ICT Project Management</span></div></th>
                            <th class="skew"><div class=""><span>ICT management & governance</span></div></th>
                        </tr>
                    </thead>
                    <tr>
                        <td class="project-name">Mandatory Subjects V  ICT knowledge type ></td>
                        <td colspan="5" class="colorrgange">Professional</td>
                        <td colspan="8" class="colorgrenn">Core</td>
                        <td class="colorblue">In-depth</td>
                    </tr>
                    <tbody>
                        {% for _, row in df.iterrows() %}
                        <tr>
                            <td class="project-name">{{ row['Unit Code + Unit Name'] }}</td>
                            <td class="colorpurple">{{ row['ICT Ethics'] }}</td>
                            <td>{{ row['Impacts of ICT'] }}</td>
                            <td>{{ row['Working Individually & Teamwork'] }}</td>
                            <td>{{ row['Professional Communication'] }}</td>
                            <td>{{ row['Professional Practitioner'] }}</td>
                            <td>{{ row['ICT Fundamentals'] }}</td>
                            <td>{{ row['ICT Infrastructure'] }}</td>
                            <td>{{ row['Information & Data Science & Engineering'] }}</td>
                            <td>{{ row['Computational Science & Engineering'] }}</td>
                            <td>{{ row['Application Systems'] }}</td>
                            <td class="colorpurple">{{ row['Cyber Security'] }}</td>
                            <td class="colorpurple">{{ row['ICT Project Management'] }}</td>
                            <td>{{ row['ICT management & governance'] }}</td>
                            <td>{{ row['In-depth'] }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
        """
        # Render the HTML using Jinja2
        template = Template(html_template)
        criterion_html = template.render(course=course, df=df)

        return criterion_html
    else:
        return "<p>No data for Criterion C.</p>"

# Criterion D HTML generation
def generate_criterion_d_html(course):
    data_frames = []
    criterion = kb.criterionD[course]

    df = criterion.criterion_df
    if df is not None and not df.empty and isinstance(df, pd.DataFrame):
        required_columns = ['Unit Code', 'Unit Name', 'Justification']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return f"<p>Warning: Missing columns {missing_columns} for course {course}.</p>"
        
        df['Unit Code & Title'] = df['Unit Code'] + ' ' + df['Unit Name']
        
       # Make sure column names exist and match
        if 'Assessment Item (for D: Advanced Algorithms and C: CBoK mapping)' in df.columns:
            df['Assessment Item'] = df['Assessment Item (for D: Advanced Algorithms and C: CBoK mapping)']
            df.drop(columns=['Assessment Item (for D: Advanced Algorithms and C: CBoK mapping)'], inplace=True)
        
        
        if 'Justification' in df.columns:
            df['Complex Computing Criteria met'] = df['Justification'].fillna('N/A')
        else:
            df['Complex Computing Criteria met'] = 'N/A'
        

        criterion_html = """
        <h3>Criterion D</h3>
        <table border="1" cellpadding="10">
            <thead>
                <tr>
                    <th>Unit Code & Title</th>
                    <th>Assessment Item</th>
                    <th>Complex Computing Criteria met</th>
                </tr>
            </thead>
            <tbody>
        """
        for _, row in df.iterrows():
            criterion_html += f"""
            <tr>
                <td>{row['Unit Code & Title']}</td>
                <td>{row['Assessment Item']}</td>
                <td>{row['Complex Computing Criteria met']}</td>
            </tr>
            """
        criterion_html += "</tbody></table>"
        return criterion_html
    return "<p>No data for Criterion D.</p>"

# Criterion E HTML generation
def generate_criterion_e_html(criterion_e_df):
    if criterion_e_df is not None and not criterion_e_df.empty:
        unique_df = criterion_e_df.drop_duplicates(subset=['Unit Code', 'Unit Name', 'Justification'])
        criterion_html = """
        <h3>Criterion E</h3>
        <table>
            <thead>
                <tr>
                    <th>Unit Code</th>
                    <th>Unit Name</th>
                    <th>Justification</th>
                </tr>
            </thead>
            <tbody>
        """
        for _, row in unique_df.iterrows():
            unit_code = row['Unit Code']
            unit_name = row['Unit Name']
            justification = row['Justification']
            criterion_html += f"""
            <tr>
                <td>{unit_code}</td>
                <td>{unit_name}</td>
                <td>{justification}</td>
            </tr>
            """
        criterion_html += "</tbody></table>"
        return criterion_html
    return "<p>No data for Criterion E.</p>"