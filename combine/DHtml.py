import pandas as pd
from sfia import SFIA
from knowledgebase import KnowledgeBase
from jinja2 import Template

def generate_html_content():
    try:
        print("Starting generate_html_content()")
        
        # Step 1: Load SFIA data
        sfia_file = 'sfia_v8_custom.xlsx'
        print(f"Loading SFIA data from {sfia_file}")
        sfia = SFIA(sfia_file)
        print("SFIA data loaded successfully")
        
        # Step 2: Load KnowledgeBase
        kb_file = 'CSSE-allprograms-outcome-mappings-20240927.xlsx'
        print(f"Loading KnowledgeBase data from {kb_file}")
        kb = KnowledgeBase(kb_file, sfia)
        print("KnowledgeBase loaded successfully")
        
        # Check if 'criterionD' exists and is a dictionary
        if not hasattr(kb, 'criterionD') or not isinstance(kb.criterionD, dict):
            error_msg = "Error: 'criterionD' is missing or not a dictionary in KnowledgeBase."
            print(error_msg)
            return f"<p>{error_msg}</p>"
        
        data_frames = []
        
        # Iterate over criterionD data and extract DataFrame
        for course, criterion in kb.criterionD.items():
            print(f"Processing course: {course}")
            
            # Check if 'criterion_df' exists
            if not hasattr(criterion, 'criterion_df'):
                print(f"Error: 'criterion_df' is missing in criterion for course {course}.")
                continue  # Skip to the next iteration
        
            df = criterion.criterion_df
            if df is not None and not df.empty and isinstance(df, pd.DataFrame):
                required_columns = ['Unit Code', 'Unit Name', 'Justification']
                missing_columns = [col for col in required_columns if col not in df.columns]
                if missing_columns:
                    print(f"Warning: Missing columns {missing_columns} in DataFrame for course {course}.")
                    continue  # Skip this DataFrame
                
                df['Course Title'] = course  # Add a 'Course Title' column to the DataFrame
                df['Unit Code & Title'] = df['Unit Code'] + ' ' + df['Unit Name']  # Combine 'Unit Code' and 'Unit Name'
                
                # Split 'Justification' into 'Complex Computing Criteria met' and 'Assessment Item'
                def split_justification(justification):
                    if isinstance(justification, str):
                        if '.' in justification:
                            parts = justification.split('.', 1)
                            complex_computing = parts[0].strip()
                            assessment_item = parts[1].strip()
                            return complex_computing, assessment_item
                        else:
                            return "", justification  # Entire sentence is 'Assessment Item'
                    else:
                        return "", ""  # Non-string 'Justification'
                        
                try:
                    df[['Complex Computing Criteria met', 'Assessment Item']] = df['Justification'].apply(
                        lambda x: pd.Series(split_justification(x))
                    )
                except Exception as e:
                    print(f"Error processing 'Justification' for course {course}: {e}")
                    continue  # Skip this DataFrame
                    
                data_frames.append(df)
                print(f"Data processed for course: {course}")
            else:
                print(f"No valid data found in DataFrame for course {course}.")
        
        # Combine all DataFrames
        if data_frames:
            try:
                combined_df = pd.concat(data_frames, ignore_index=True)
                print("DataFrames combined successfully")
            except Exception as e:
                error_msg = f"Error combining DataFrames: {e}"
                print(error_msg)
                return f"<p>{error_msg}</p>"
            
            try:
                # Group by 'Course Title'
                grouped = combined_df.groupby('Course Title')
                print("Data grouped by 'Course Title' successfully")
            except Exception as e:
                error_msg = f"Error grouping combined DataFrame: {e}"
                print(error_msg)
                return f"<p>{error_msg}</p>"
            
            # Prepare data for rendering
            courses = {}
            try:
                for course_title, group in grouped:
                    courses[course_title] = group.to_dict(orient='records')
                print("Data prepared for rendering")
            except Exception as e:
                error_msg = f"Error preparing data for rendering: {e}"
                print(error_msg)
                return f"<p>{error_msg}</p>"
            
            # Jinja2 HTML template
            html_template = """
            <h1>Advanced ICT Units Addressing Complex Computing</h1>
            <div class="table-container">
            {% for course_title, units in courses.items() %}
            <h2>{{ course_title }}</h2>
            <table border="1" cellpadding="10">
                <thead>
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
            </div>
            <style>
            /* Add your CSS styling here */
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                font-size: 16px;
                text-align: left;
                background-color: #f9f9f9;
            }
            th, td {
                padding: 12px;
                border-bottom: 1px solid #ddd;
            }
            th {
                background-color: #e0e0e0;
            }
            tr:hover {
                background-color: #f1f1f1;
            }
            h1, h2 {
                color: #333;
            }
            .table-container {
                margin: 0;
                padding: 0;
            }
            </style>
            """
            
            # Render HTML template
            try:
                print("Rendering HTML content")
                template = Template(html_template)
                html_output = template.render(courses=courses)
                print("HTML content rendered successfully")
                return html_output
            except Exception as e:
                error_msg = f"Error rendering HTML template: {e}"
                print(error_msg)
                return f"<p>{error_msg}</p>"
        else:
            print("No data found in criterionD.")
            return "<p>No data found in criterionD.</p>"
    except Exception as e:
        error_msg = f"An error occurred in generate_html_content: {e}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        return f"<p>{error_msg}</p>"