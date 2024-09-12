import pandas as pd
from sfia import SFIA
from knowledgebase import KnowledgeBase

# Skills For the Information Age database
sfia = SFIA('sfiaskills.6.3.en.1.xlsx')

# KnowledgeBase - processes the input from the client
kb = KnowledgeBase('CSSE-allprograms-outcome-mappings-20240821.xlsx', sfia)

# Prepare HTML content to save the output
html_content = """
<html>
<head>
    <title>Course Outcomes and Criterion Data</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            font-size: 14px;
        }
        .course-name {
            font-weight: bold;
            margin: 15px 0 5px 0;
        }
        .criterion-header {
            background-color: #B7CDE2; /* Light blue background */
            padding: 10px;
            font-size: 14px;
            font-weight: bold;
        }
        .table-container {
            margin-bottom: 20px;
            width: 100%;
        }
        .table-header {
            background-color: #4F81BD; /* Darker blue background */
            color: white;
            font-weight: bold;
            padding: 8px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 5px;
        }
        th, td {
            border: 1px solid #000;
            padding: 5px;
            text-align: left;
            font-size: 12px;
        }
        th {
            background-color: #DCE6F1; /* Lighter blue for table headers */
            font-weight: bold;
            text-align: left;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9; /* Alternate row background */
        }
    </style>
</head>
<body>
    <h1>Criterion E: Integrated and Applied ICT Knowledge</h1>
"""

# Loop through courses and their corresponding criterion data
for course, criterion in kb.criterionE.items():
    # Check if 'Justification' exists in criterion_df
    if 'Justification' in criterion.criterion_df.columns:
        filtered_criterion_df = criterion.criterion_df.loc[
            criterion.criterion_df['Justification'].notna() & (criterion.criterion_df['Justification'] != '')
        ]
    else:
        filtered_criterion_df = pd.DataFrame()  # Create an empty DataFrame if 'Justification' column doesn't exist
    
    # Check if 'Justification' exists in criterion_qa_df
    if 'Justification' in criterion.criterion_qa_df.columns:
        filtered_criterion_qa_df = criterion.criterion_qa_df.loc[
            criterion.criterion_qa_df['Justification'].notna() & (criterion.criterion_qa_df['Justification'] != '')
        ]
    else:
        filtered_criterion_qa_df = pd.DataFrame()  # Create an empty DataFrame if 'Justification' column doesn't exist

    # Add the course section only if there's justification data in either DataFrame
    if not filtered_criterion_df.empty or not filtered_criterion_qa_df.empty:
        # Add course name
        html_content += f'<div class="course-name">{course}</div>'
        
        # Add Criterion header
        html_content += '<div class="criterion-header">Criterion E: Integrated and Applied ICT Knowledge</div>'
        
        # Start table
        html_content += """
        <div class="table-container">
        <table>
            <thead>
                <tr>
                    <th class="table-header">Unit Code & Title</th>
                    <th class="table-header">Notes in Support of Claim</th>
                </tr>
            </thead>
            <tbody>
        """
        
        # Add Criterion DataFrame as table rows
        if not filtered_criterion_df.empty:
            for _, row in filtered_criterion_df.iterrows():
                html_content += f"""
                <tr>
                    <td>{row['Unit Code']} IT Capstone Project</td>
                    <td>{row['Justification']}</td>
                </tr>
                """
        
        # Add Criterion QA DataFrame as table rows (if applicable)
        if not filtered_criterion_qa_df.empty:
            for _, row in filtered_criterion_qa_df.iterrows():
                html_content += f"""
                <tr>
                    <td>{row['Unit Code']} IT Capstone Project</td>
                    <td>{row['Justification']}</td>
                </tr>
                """
        
        # Close table
        html_content += """
            </tbody>
        </table>
        </div>
        """

# Close the HTML content
html_content += """
</body>
</html>
"""

# Write the HTML content to a new file
output_html_path = 'E_updated.html'
with open(output_html_path, 'w') as f:
    f.write(html_content)

print(f"Filtered courses with justifications have been saved to {output_html_path}")
