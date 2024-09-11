import pandas as pd
from sfia import SFIA
from knowledgebase import KnowledgeBase

# Load Skills For the Information Age (SFIA) database from Excel
sfia_data = pd.read_excel('sfiaskills.6.3.en.1.xlsx', usecols=['Skill', 'description', 'description22', 'code', 'level'])

# Drop duplicates based on the 'code' and 'level' columns (keep the first occurrence)
sfia_data_unique = sfia_data.drop_duplicates(subset=['code', 'level'], keep='first')

# Load KnowledgeBase - this processes the input from the client
kb = KnowledgeBase('CSSE-allprograms-outcome-mappings-20240821.xlsx', SFIA('sfiaskills.6.3.en.1.xlsx'))

# Create a dictionary to map SFIA skills to their descriptions (Skill, Description, and Description2)
sfia_skill_data = sfia_data_unique.set_index(['code', 'level']).to_dict(orient='index')

# Prepare HTML content to display course titles, outcomes, levels, and justifications in table format
html_content = """
<html>
<head>
    <title>Course Outcomes, Levels, and Justifications</title>
    <style>
        table {
            width: 80%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
        }
        th {
            background-color: #DCE6F1;
            text-align: left;
            cursor: pointer;
        }
        .collapsible {
            width: 50%; /* Limit the width */
            margin: 20px 0; /* Center the element horizontally */
            cursor: pointer;
            background-color: #B7CDE2;
            padding: 10px;
            text-align: left;
            font-weight: bold;
            border: 1px solid #ccc;
        }
        .content {
            display: none;
        }
        .active {
            display: table;
        }
        input[type="text"] {
            margin-bottom: 15px;
            padding: 5px;
            width: 30%;
            font-size: 16px;
        }
    </style>
</head>
<body>
    <h1>Criterion B</h1>

    <!-- Add a search box to filter the table -->
    <input type="text" id="searchInput" onkeyup="searchTable()" placeholder="Search for SFIA skills..">
"""

# Loop through the courses and add the titles, outcomes, levels, and justifications to the HTML content
for course_index, (course, criterionB) in enumerate(kb.criterionB.items()):
    course_id = f"section{course_index + 1}"
    course_title = f"<h2 class='collapsible' onclick='toggleCollapse(\"{course_id}\")'>{course}</h2>"
    
    # Add the course title to the HTML content
    html_content += course_title

    # Drop duplicates from the criterion DataFrame (based on Outcome, Level, and Justification)
    unique_df = criterionB.criterion_df.drop_duplicates(subset=['Outcome', 'Level (SFIA/Bloom)', 'Justification'])

    # Start a table for outcomes, levels, and justifications with renamed headers
    html_content += f"""
    <table id="{course_id}" class="content">
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

    # Loop through each unique row in the criterion DataFrame to get outcomes, levels, and justifications
    for _, row in unique_df.iterrows():

        outcome = row['Outcome']  # Renamed as "Code" in the table
        level = row['Level (SFIA/Bloom)']
        justification = row['Justification']  # Renamed as "Units Supporting SFIA Skill"

        # Get the corresponding SFIA skill data based on the Outcome (code) and Level
        sfia_info = sfia_skill_data.get((outcome, level), {'Skill': 'N/A', 'description': 'N/A', 'description22': 'N/A'})

        skill = sfia_info.get('Skill', 'N/A')
        description = sfia_info.get('description', 'N/A')
        description2 = sfia_info.get('description22', 'N/A')

        # Add a row to the table with outcome, level, justification, and SFIA skill information
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
    
    # Close the table for this course
    html_content += """
        </tbody>
    </table>
    """

# Close the HTML content
html_content += """
<script>
// Function to toggle collapsible sections by ID
function toggleCollapse(sectionId) {
    var element = document.getElementById(sectionId);
    if (element.style.display === "none" || element.style.display === "") {
        element.style.display = "table";
    } else {
        element.style.display = "none";
    }
}

// Function to sort the table by column within a specific table
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

// Function to filter/search through the table
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
</body>
</html>
"""

# Write the HTML content to a new file
output_html_path = 'course_outcomes_filtered_by_sfia_navi_1.html'
with open(output_html_path, 'w') as f:
    f.write(html_content)

print(f"Filtered course outcomes, levels, and justifications (matched by code and level) have been written to {output_html_path}")
