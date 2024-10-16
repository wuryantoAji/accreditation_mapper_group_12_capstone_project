import pandas as pd
from jinja2 import Template
from sfia import SFIA
from knowledgebase import KnowledgeBase
from caidi import CAIDI

def generate_html_content():
    try:
        print("Starting generate_html_content()")
        
        # Load SFIA data
        sfia_file = 'sfia_v8_custom.xlsx'
        print(f"Loading SFIA data from {sfia_file}")
        sfia = SFIA(sfia_file)
        print("SFIA data loaded successfully")
        
        # Load CAIDI data
        caidi_file = 'caidi-data-for-ACS-A.zip'
        print(f"Loading CAIDI data from {caidi_file}")
        cd = CAIDI(caidi_file)
        print("CAIDI data loaded successfully")
        
        # Load KnowledgeBase
        kb_file = 'CSSE-allprograms-outcome-mappings-20241011.xlsx'
        print(f"Loading KnowledgeBase data from {kb_file}")
        kb = KnowledgeBase(kb_file, sfia, cd)
        print("KnowledgeBase loaded successfully")
        
        # Create a list to store data for each course
        data = []
        print("Processing courses for criterion C")
        
        # Iterate through each course and its corresponding criterion
        for course, criterion in kb.criterionC.items():
            # Check if table_2_df exists and process it
            if hasattr(criterion, 'table_2_df'):
                df = criterion.table_2_df.copy()

                print(f"Data for course: {course}")
                print(df.head())  # Output the first few rows to inspect the data

                # Inspect the number of columns
                print(f"Original columns: {df.columns.tolist()}")
                print(f"Number of columns: {len(df.columns)}")

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
                    continue

                # Replace NaN values with empty strings
                df.fillna('', inplace=True)

                # Add the course name to the DataFrame as a new column
                df['Course'] = course
                data.append(df)
            else:
                print(f"Warning: 'table_2_df' not found for {course}")

        # Concatenate data from all courses into a single DataFrame
        if data:
            all_data = pd.concat(data, ignore_index=True)
            print("Data concatenated successfully")
        else:
            print("No data found")
            return "<p>No data found</p>"

        #  generate HTML content
        print("Generating HTML content")

        df = all_data
        # Group by course
        grouped = df.groupby('Course')

        # Define Jinja2 template
        html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
            {{ css }}
            </style>
        </head>
        <body>
            <div class="quick-nav-container">
            {% for course, units in data.items() %}
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
                        {% for unit in units %}
                        <tr>
                            <td class="project-name">{{ unit['Unit Code + Unit Name'] }}</td>
                            <td class="colorpurple">{{ unit['ICT Ethics']}}</td>
                            <td class="">{{ unit['Impacts of ICT']}}</td>
                            <td class="">{{ unit['Working Individually & Teamwork']}}</td>
                            <td class="">{{ unit['Professional Communication']}}</td>
                            <td class="">{{ unit['Professional Practitioner']}}</td>
                            <td class="">{{ unit['ICT Fundamentals']}}</td>
                            <td class="">{{ unit['ICT Infrastructure']}}</td>
                            <td class="">{{ unit['Information & Data Science & Engineering']}}</td>
                            <td class="">{{ unit['Computational Science & Engineering']}}</td>
                            <td class="">{{ unit['Application Systems']}}</td>
                            <td class="colorpurple">{{ unit['Cyber Security']}}</td>
                            <td class="colorpurple">{{ unit['ICT Project Management']}}</td>
                            <td class="">{{ unit['ICT management & governance']}}</td>
                            <td class="">{{ unit['In-depth']}}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            <br/>
            {% endfor %}
            </div>
        </body>
        </html>
        """

        # Convert the data into dictionary format
        course_data = {}
        for course, group in grouped:
            course_data[course] = group.to_dict('records')

        # Define CSS
        css = """
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
        """

        # Render the HTML using the Jinja2 template
        template = Template(html_template)
        html_content = template.render(data=course_data, css=css)
        print("HTML content rendered successfully")
        return html_content

    except Exception as e:
        print(f"An error occurred in generate_html_content: {e}")
        import traceback
        traceback.print_exc()
        return f"<p>An error occurred while generating content: {e}</p>"
