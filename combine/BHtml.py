import pandas as pd
from sfia import SFIA
from knowledgebase import KnowledgeBase

def generate_html_content():
    try:
        print("Starting generate_html_content()")
        
        # Load Skills For the Information Age (SFIA) database from Excel
        sfia_file = 'sfia_v8_custom.xlsx'
        print(f"Loading SFIA data from {sfia_file}")
        sfia_data = pd.read_excel(sfia_file, usecols=['Skill', 'description', 'description22', 'code', 'level'])
        print("SFIA data loaded successfully")
        
        sfia_data['description22'] = sfia_data['description22'].str.replace('_x000D_', ' ', regex=False)
        print("SFIA data cleaned")
        
        # Drop duplicates based on the 'code' and 'level' columns
        sfia_data_unique = sfia_data.drop_duplicates(subset=['code', 'level'], keep='first')
        print("Duplicates dropped from SFIA data")
        
        # Load KnowledgeBase
        kb_file = 'CSSE-allprograms-outcome-mappings-20240927.xlsx'
        print(f"Loading KnowledgeBase data from {kb_file}")
        kb = KnowledgeBase(kb_file, SFIA(sfia_file))
        print("KnowledgeBase loaded successfully")
        
        # Create a dictionary to map SFIA skills to their descriptions
        sfia_skill_data = sfia_data_unique.set_index(['code', 'level']).to_dict(orient='index')
        print("SFIA skill data dictionary created")
        
        # Prepare HTML content without the outer HTML structure
        html_content = """
        <h1>Criterion B</h1>
        <input type="text" id="searchInput" onkeyup="searchTable()" placeholder="Search for SFIA skills..">
        <div class="table-container">
        <style>
        /* General styles for the table */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 16px;
            text-align: left;
            background-color: #f9f9f9;
            margin-left: 0 !important; /* Ensure no left margin */
            padding-left: 0 !important; /* Remove any padding */
        }

        /* Styles for table headers */
        th {
            background-color: #e0e0e0; /* Light grey header */
            color: #333;
            padding: 12px;
            font-weight: bold;
            border-bottom: 2px solid #ddd;
            text-align: left; /* Ensure text is left-aligned */
        }

        /* Styles for table rows */
        td {
            padding: 10px;
            border-bottom: 1px solid #ddd; /* Subtle borders for clean look */
            text-align: left; /* Ensure text is left-aligned */
        }

        /* Styling for hover effect */
        tr:hover {
            background-color: #f1f1f1; /* Light grey on row hover */
        }

        /* Style the table search input */
        input[type="text"] {
            width: 100%;
            padding: 8px;
            margin-bottom: 20px;
            font-size: 14px;
            border: 1px solid #ddd;
            border-radius: 4px;
            margin-left: 0 !important; /* Ensure input starts from left */
        }

        /* Style for the header section */
        .header-section {
            background-color: #e6eaf0;
            padding: 10px;
            border-radius: 5px;
            margin-left: 0 !important; /* Ensure header is aligned to the left */
        }

        .header-section h1 {
            margin: 0;
            font-size: 24px;
            color: #333;
        }

        /* Styles for the "Computer Science Major" box */
        .major-title {
            background-color: #d0d6df; /* Soft blue */
            padding: 12px;
            font-size: 18px;
            color: #333;
            font-weight: bold;
            border-radius: 4px;
            margin-bottom: 15px;
            margin-left: 0 !important; /* Ensure title box is aligned to the left */
        }

        /* Responsive Design */
        @media screen and (max-width: 600px) {
            table {
                font-size: 14px;
            }
        }
        </style>
        """
        print("Initial HTML content prepared")
        
        # Loop through the courses and add details
        for course_index, (course, criterionB) in enumerate(kb.criterionB.items()):
            course_id = f"section{course_index + 1}"
            course_title = f"<h2 class='collapsible' onclick='toggleCollapse(\"{course_id}\")'>{course}</h2>"
            html_content += course_title

            # Drop duplicates and start a table
            unique_df = criterionB.criterion_df.drop_duplicates(subset=['Outcome', 'Level (SFIA/Bloom)', 'Justification'])
            html_content += f"""
            <table id="{course_id}" class="content" style="margin-left: 0 !important; padding-left: 0 !important;">
                <thead>
                    <tr>
                        <th onclick="sortTable(0, '{course_id}')">SFIA Skill</th>
                        <th onclick="sortTable(1, '{course_id}')">Skill Description</th>
                        <th onclick="sortTable(2, '{course_id}')">Level Description</th>
                        <th onclick="sortTable(3, '{course_id}')">Code</th>
                        <th onclick="sortTable(4, '{course_id}')">Level</th>
                        <th onclick="sortTable(5, '{course_id}')">Units Supporting SFIA Skill</th>
                    </tr>
                </thead>
                <tbody>
            """
            print(f"Processing course: {course}")

            # Loop through the DataFrame rows
            for _, row in unique_df.iterrows():
                outcome = row['Outcome']
                level = row['Level (SFIA/Bloom)']
                justification = row['Justification']

                # Get corresponding SFIA skill data
                sfia_info = sfia_skill_data.get((outcome, level), None)
                if sfia_info:
                    skill = sfia_info.get('Skill', 'N/A')
                    description = sfia_info.get('description', 'N/A')
                    description2 = sfia_info.get('description22', 'N/A')
                else:
                    skill = 'N/A'
                    description = 'N/A'
                    description2 = 'N/A'

                # Add the data to the table
                html_content += f"""
                <tr>
                    <td>{skill}</td>
                    <td>{description}</td>
                    <td>{description2}</td>
                    <td>{outcome}</td>
                    <td>{level}</td>
                    <td>{justification}</td>
                </tr>
                """
            html_content += "</tbody></table>"
            print(f"Finished processing course: {course}")
        
        html_content += "</div>"
        
        # Add JavaScript functions
        html_content += """
        <script>
        function toggleCollapse(sectionId) {
            var element = document.getElementById(sectionId);
            if (element.style.display === "none" || element.style.display === "") {
                element.style.display = "table";
            } else {
                element.style.display = "none";
            }
        }

        function sortTable(n, tableId) {
            var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
            table = document.getElementById(tableId);
            switching = true;
            dir = "asc"; 
            while (switching) {
                switching = false;
                rows = table.rows;
                for (i = 1; i < (rows.length - 1); i++) {
                    shouldSwitch = false;
                    x = rows[i].getElementsByTagName("TD")[n];
                    y = rows[i + 1].getElementsByTagName("TD")[n];
                    if (dir == "asc") {
                        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                            shouldSwitch = true;
                            break;
                        }
                    } else if (dir == "desc") {
                        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                            shouldSwitch = true;
                            break;
                        }
                    }
                }
                if (shouldSwitch) {
                    rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                    switching = true;
                    switchcount++;
                } else {
                    if (switchcount == 0 && dir == "asc") {
                        dir = "desc";
                        switching = true;
                    }
                }
            }
        }

        function searchTable() {
            var input, filter, table, tr, td, i, j, txtValue;
            input = document.getElementById("searchInput");
            filter = input.value.toLowerCase();
            table = document.querySelectorAll("table");
            table.forEach(tbl => {
                tr = tbl.getElementsByTagName("tr");
                for (i = 1; i < tr.length; i++) {
                    tr[i].style.display = "none"; 
                    td = tr[i].getElementsByTagName("td");
                    for (j = 0; j < td.length; j++) {
                        if (td[j]) {
                            txtValue = td[j].textContent || td[j].innerText;
                            if (txtValue.toLowerCase().indexOf(filter) > -1) {
                                tr[i].style.display = "";
                                break;
                            }
                        }
                    }
                }
            });
        }
        </script>
        """
        print("HTML content generation completed successfully")
        return html_content
    except Exception as e:
        print(f"An error occurred in generate_html_content: {e}")
        import traceback
        traceback.print_exc()
        return f"<p>An error occurred while generating content: {e}</p>"