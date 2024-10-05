import pandas as pd
from sfia import SFIA
from knowledgebase import KnowledgeBase

def generate_html_content():
    print("Starting generate_html_content()")
    try:
        # Load Skills For the Information Age (SFIA) database from Excel
        sfia_file = 'sfia_v8_custom.xlsx'
        print(f"Loading SFIA data from {sfia_file}")
        try:
            sfia_instance = SFIA(sfia_file)
            print("SFIA data loaded successfully")
        except FileNotFoundError:
            print(f"Error: The SFIA file '{sfia_file}' was not found.")
            return f"<p>Error: The SFIA file '{sfia_file}' was not found.</p>"
        except Exception as e:
            print(f"Error loading SFIA data: {e}")
            return f"<p>Error loading SFIA data: {e}</p>"
        
        # Load KnowledgeBase
        kb_file = 'CSSE-allprograms-outcome-mappings-20240913.xlsx'
        print(f"Loading KnowledgeBase data from {kb_file}")
        try:
            kb = KnowledgeBase(kb_file, sfia_instance)
            print("KnowledgeBase loaded successfully")
        except FileNotFoundError:
            print(f"Error: The KnowledgeBase file '{kb_file}' was not found.")
            return f"<p>Error: The KnowledgeBase file '{kb_file}' was not found.</p>"
        except Exception as e:
            print(f"Error loading KnowledgeBase data: {e}")
            return f"<p>Error loading KnowledgeBase data: {e}</p>"
        
        # Prepare HTML content
        html_content = """
        <html>
        <head>
            <title>Criterion E: Integrated and Applied ICT Knowledge</title>
            <style>
                /* General table styling */
                body {
                    font-family: Arial, sans-serif;
                    font-size: 14px;
                }
                .course-name {
                    font-weight: bold;
                    margin: 15px 0 5px 0;
                    cursor: pointer;
                }
                .criterion-header {
                    background-color: #B7CDE2; /* Light blue background */
                    padding: 10px;
                    font-size: 14px;
                    font-weight: bold;
                }
                .table-container {
                    margin-left: 0;  /* Align the table container to the left */
                    padding-left: 0;  /* Remove any extra padding on the left */
                    width: 100%
                    margin-bottom: 20px;
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
                    margin-left: 0;  /* Align the table container to the left */
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
                .collapsible {
                    cursor: pointer;
                }
                .active + .content {
                    display: block;
                }
            </style>
            <script>
                // Accordion-like function to toggle the visibility of the table
                function toggleCollapse(sectionId) {
                    var element = document.getElementById(sectionId);

                    if (!element) {
                        console.error(`Element with ID ${sectionId} not found`);
                        return;
                    }

                    // Get the current computed display value of the element
                    var currentDisplay = window.getComputedStyle(element).display;

                    // Log the current display to the console for debugging
                    console.log(`Current display of ${sectionId}: ${currentDisplay}`);

                    // Toggle the display property based on current value
                    if (currentDisplay === 'none') {
                        element.style.display = 'table';  // Show the section
                    } else {
                        element.style.display = 'none';   // Hide the section
                    }
                }
            </script>
        </head>
        <body>
            <h1>Criterion E: Integrated and Applied ICT Knowledge</h1>
        """
        print("Initial HTML content prepared")
        
        # Loop through courses and their corresponding criterion data
        try:
            criterionE_items = kb.criterionE.items()
        except AttributeError:
            print("Error: 'criterionE' attribute not found in KnowledgeBase.")
            return "<p>Error: 'criterionE' attribute not found in KnowledgeBase.</p>"
        except Exception as e:
            print(f"Error accessing criterionE data: {e}")
            return f"<p>Error accessing criterionE data: {e}</p>"
        
        for course_index, (course, criterion) in enumerate(criterionE_items):
            course_id = f"section{course_index + 1}"
            table_id = f"table_{course_id}"  # Create the ID for the table container

            # Create the clickable course title that toggles the table
            course_title = f'<div class="course-name collapsible" onclick="toggleCollapse(\'{table_id}\')">{course}</div>'
            
            # Check if 'Justification' exists in criterion_df
            try:
                if 'Justification' in criterion.criterion_df.columns:
                    filtered_criterion_df = criterion.criterion_df.loc[
                        criterion.criterion_df['Justification'].notna() & (criterion.criterion_df['Justification'] != '')
                    ]
                else:
                    filtered_criterion_df = pd.DataFrame()
            except AttributeError:
                print(f"Error: 'criterion_df' attribute not found in criterion for course {course}.")
                filtered_criterion_df = pd.DataFrame()
            except Exception as e:
                print(f"Error processing 'criterion_df' for course {course}: {e}")
                filtered_criterion_df = pd.DataFrame()
            
            # Check if 'Justification' exists in criterion_qa_df
            try:
                if 'Justification' in criterion.criterion_qa_df.columns:
                    filtered_criterion_qa_df = criterion.criterion_qa_df.loc[
                        criterion.criterion_qa_df['Justification'].notna() & (criterion.criterion_qa_df['Justification'] != '')
                    ]
                else:
                    filtered_criterion_qa_df = pd.DataFrame()
            except AttributeError:
                print(f"Error: 'criterion_qa_df' attribute not found in criterion for course {course}.")
                filtered_criterion_qa_df = pd.DataFrame()
            except Exception as e:
                print(f"Error processing 'criterion_qa_df' for course {course}: {e}")
                filtered_criterion_qa_df = pd.DataFrame()
        
            # Add the course section only if there's justification data in either DataFrame
            if not filtered_criterion_df.empty or not filtered_criterion_qa_df.empty:
                # Add course title with correct ID for the table
                html_content += course_title

                # Add Criterion header
                html_content += '<div class="criterion-header">Criterion E: Integrated and Applied ICT Knowledge</div>'
                
                # Start collapsible table container with the correct ID
                html_content += f"""
                <div class="table-container content" id="{table_id}">
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
                        try:
                            unit_code = row.get('Unit Code', 'N/A')
                            justification = row.get('Justification', 'N/A')
                            html_content += f"""
                            <tr>
                                <td>{unit_code}</td>
                                <td>{justification}</td>
                            </tr>
                            """
                        except Exception as e:
                            print(f"Error processing row in 'filtered_criterion_df' for course {course}: {e}")
                            continue
                
                # Add Criterion QA DataFrame as table rows (if applicable)
                if not filtered_criterion_qa_df.empty:
                    for _, row in filtered_criterion_qa_df.iterrows():
                        try:
                            unit_code = row.get('Unit Code', 'N/A')
                            justification = row.get('Justification', 'N/A')
                            html_content += f"""
                            <tr>
                                <td>{unit_code}</td>
                                <td>{justification}</td>
                            </tr>
                            """
                        except Exception as e:
                            print(f"Error processing row in 'filtered_criterion_qa_df' for course {course}: {e}")
                            continue
                
                # Close table
                html_content += """
                    </tbody>
                </table>
                </div>
                """
                print(f"Finished processing course: {course}")
        
        # Close the HTML content
        html_content += """
        </body>
        </html>
        """
        print("HTML content generation completed successfully")
        return html_content
    except Exception as e:
        print(f"An unexpected error occurred in generate_html_content: {e}")
        import traceback
        traceback.print_exc()
        return f"<p>An unexpected error occurred while generating content: {e}</p>"