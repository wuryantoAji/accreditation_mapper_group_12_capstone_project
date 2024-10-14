def generate_html_content():
    from sfia import SFIA
    from knowledgebase import KnowledgeBase
    import pandas as pd
    from jinja2 import Template
    from caidi import CAIDI
    import os

    # Step 1: Extract data and store it as a DataFrame
    try:
        cd = CAIDI('caidi-data-for-ACS-A.zip')
    except FileNotFoundError as e:
        print(f"Error loading CAIDI data: {e}")
        return "<p>Error loading CAIDI data.</p>"

    # Skills For the Information Age database
    try:
        sfia = SFIA('sfia_v8_custom.xlsx')
    except FileNotFoundError as e:
        print(f"Error loading SFIA data: {e}")
        return "<p>Error loading SFIA data.</p>"

    # KnowledgeBase - processes the input from the client
    try:
        kb = KnowledgeBase('CSSE-allprograms-outcome-mappings-20241011.xlsx', sfia, cd)
    except FileNotFoundError as e:
        print(f"Error loading KnowledgeBase data: {e}")
        return "<p>Error loading KnowledgeBase data.</p>"

    # Assume your KnowledgeBase object and data processing part have been initialized
    data_frames = []

    # Iterate over criterionD data and extract DataFrame
    for course, criterion in kb.criterionD.items():

        print(f"Processing course: {course}")
        
        df = criterion.criterion_df
        if df is not None and not df.empty:
            print(f"Headers in DataFrame for course {course}: {df.columns.tolist()}")
            # Make sure column names exist and match
            if 'Assessment Item (for D: Advanced Algorithms and C: CBoK mapping)' in df.columns:
                df['Assessment Item'] = df['Assessment Item (for D: Advanced Algorithms and C: CBoK mapping)']
                df.drop(columns=['Assessment Item (for D: Advanced Algorithms and C: CBoK mapping)'], inplace=True)
        
            
            if 'Justification' in df.columns:
                df['Complex Computing Criteria met'] = df['Justification'].fillna('N/A')
            else:
                df['Complex Computing Criteria met'] = 'N/A'
                print(f"'Justification' column not found in DataFrame for course {course}.")

            df['Course Title'] = course  # Add a 'Course Title' column to the DataFrame
            df['Unit Code & Title'] = df['Unit Code'] + ' ' + df['Unit Name']  # Combine 'Unit Code' and 'Unit Name'
            # Optionally print the first few values from the Justification column
            # print(df['Justification'].head())
            data_frames.append(df)
        else:
            print(f"No data found for course {course}.")

    # Combine all DataFrames
    if data_frames:
        combined_df = pd.concat(data_frames)

        # Group by 'Course Title'
        grouped = combined_df.groupby('Course Title')

        # Jinja2 HTML template with basic inline CSS for styling
        html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Advanced ICT Units Addressing Complex Computing</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 20px;
                }
                h1 {
                    color: #333;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 20px;
                }
                th, td {
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                }
                th {
                    background-color: #f2f2f2;
                    font-weight: bold;
                }
                tr:nth-child(even) {
                    background-color: #f9f9f9;
                }
                .title-row {
                    background-color: #d3d3d3;
                    color: white;
                }
            </style>
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
        try:
            template = Template(html_template)
            html_output = template.render(courses=courses)
            return html_output
        except Exception as e:
            print(f"Error rendering HTML template: {e}")
            return f"<p>Error rendering HTML template: {e}</p>"
    else:
        print("No data found in criterionD.")
        return "<p>No data found in criterionD.</p>"