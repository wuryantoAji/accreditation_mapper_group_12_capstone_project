import argparse
import os
import zipfile
import pandas as pd
from pylatex import Package, NoEscape, Section, Subsection, Subsubsection, Tabular, MultiColumn, MultiRow, Document, NewLine, LongTable
from sfia import SFIA
from knowledgebase import KnowledgeBase
from caidi import CAIDI

placeholderConstant = 'Placeholder'

# Transform a list of course into tables

# Table 1. Criterion A
def createCriterionATable(programName, listOfCourse):
    criterionAList = []
    ### Start loop for each program
    criterionASubSubSection = Subsubsection('Program Name\n')
    criterionASubSubSection.append(NoEscape(r'\rubric{Criterion A Rubric}'))
    criterionASubSubSection.append(NewLine())
    criterionASubSubSection.append(NoEscape(r'\begin{adjustbox}{max width=\textwidth}'))
    criterionATable = Tabular(table_spec="|p{\\criterionAEmptyCol}|p{\\criterionACodeCol}|p{\\criterionATitleCol}|p{\\criterionACoordinatorCol}|p{\\criterionAFileCol}|")
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(5, align="|l|", data=NoEscape(r'\cellcolor{colorDarkBlue}')),))
    criterionATable.add_row((MultiColumn(5, align="|l|", data=NoEscape(r'\criterionAHeader{Program Details}')),))
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(2, align="|l|", data=NoEscape(r'\colorcelllightblueitalic Code')), (MultiColumn(3, align="|l|", data="code-name"))))
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(2, align="|l|", data=NoEscape(r'\colorcelllightblueitalic Award title on Transcript/Testamur')), (MultiColumn(3, align="|l|", data="award-name"))))
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(2, align="|l|", data=NoEscape(r'\colorcelllightblueitalic EFT Years of Study')), (MultiColumn(3, align="|l|", data="study-duration"))))
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(2, align="|l|", data=NoEscape(r'\colorcelllightblueitalic First Year of Offer')), (MultiColumn(3, align="|l|", data="year-name"))))
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(5, align="|l|", data=NoEscape(r'\cellcolor{colorDarkBlue}')),))
    criterionATable.add_row((MultiColumn(5, align="|l|", data=NoEscape(r'\criterionAHeader{Personnel}')),))
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(2, align="|l|", data=NoEscape(r'\colorcelllightblueitalic Program Chair')), (MultiColumn(3, align="|l|", data="chair-name"))))
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(2, align="|l|", data=NoEscape(r'\colorcelllightblueitalic ICT Industry Liaison')), (MultiColumn(3, align="|l|", data="liaison-name"))))
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(2, align="|l|", data=NoEscape(r'\colorcelllightblueitalic Key Academic Staff')), (MultiColumn(3, align="|l|", data="[list-of-staff-name]"))))
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(5, align="|l|", data=NoEscape(r'\cellcolor{colorDarkBlue}')),))
    criterionATable.add_row((MultiColumn(5, align="|l|", data=NoEscape(r'\criterionAHeader{Outcomes}')),))
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(5, align="|l|", data="Lorem Ipsum"),))
    criterionATable.add_hline()
    criterionATable.add_row((
        MultiColumn(2, align="|l", data=NoEscape(r'\cellcolor{colorDarkBlue}')),
        MultiColumn(3, align="l|", data=NoEscape(r'\cellcolor{colorDarkBlue}'))
    ))
    criterionATable.add_row((
        MultiColumn(2, align="|l", data=NoEscape(r'\criterionAUnitSequence')),
        MultiColumn(3, align="l|", data=NoEscape(r'\cellcolor{colorDarkBlue}\multirow{-2}{*}{\criterionAKey}'))
    ))
    criterionATable.add_hline()
    criterionATable.add_row((
        NoEscape(r'\cellcolor{colorLightBlue}\textbf{}'),
        NoEscape(r'\cellcolor{colorLightBlue}\textbf{Code}'),
        NoEscape(r'\cellcolor{colorLightBlue}\textbf{Title}'),
        NoEscape(r'\cellcolor{colorLightBlue}\textbf{Unit Coordinator(s)}'),
        NoEscape(r'\cellcolor{colorLightBlue}\textbf{File \#}'),
    ))
    criterionATable.add_hline()
    criterionASubSubSection.append(criterionATable)
    criterionASubSubSection.append(NoEscape(r'\end{adjustbox}'))
    criterionASubSubSection.append(NewLine())
    criterionASubSubSection.generate_tex("criterionA-")
    criterionAList.append(f"criterionA-.tex")
    return criterionAList

# Table 2. Criterion B
def createCriterionBTable(dataDictionary):
    criterionBList = []
    ### Start loop for each program
    for key in dataDictionary:
        criterionBSubSubSection = Subsubsection(f"{key}\n")
        criterionBSubSubSection.append(NoEscape(r'\rubric{Criterion B Rubric || SFIA Code ( ) || SFIA Level ( ) || Unit Supporting SFIA Skill ( ) || SFIA Skill ( ) || Skill Description ( ) || Level Description ( )}'))
        professionalSkills = dataDictionary[key][1]
        criterionBSubSubSection.append(f"ICT professional role: {professionalSkills}\n")
        sfiaSkills = ""
        for sfiaComponent in dataDictionary[key][0].keys():
            sfiaSkills = sfiaSkills+"+"+sfiaComponent[0]
        criterionBSubSubSection.append(f"SFIA skills: {sfiaSkills[1:]}\n")
        # criterionBSubSubSection.append(NoEscape(r'\begin{adjustbox}{max width=1\textwidth}'))
        criterionBTable = LongTable(table_spec=NoEscape(r'|p{0.1\textwidth}|p{0.2\textwidth}|p{0.2\textwidth}|p{0.1\textwidth}|p{0.1\textwidth}|p{0.22\textwidth}|'))
        criterionBTable.add_hline()

        # table header
        criterionBTable.append(NoEscape(r'\criterionBEmptyColoredRow'))
        criterionBTable.append(NoEscape(r'\criterionBEmptyColoredRow'))
        criterionBTable.add_row(MultiRow(NoEscape(-3), data=NoEscape(r'\criterionBHeaderCellColored{SFIA Skill}')), 
                        MultiRow(NoEscape(-3), data=NoEscape(r'\criterionBHeaderCellColored{Skill Description}')), 
                        MultiRow(NoEscape(-3), data=NoEscape(r'\criterionBHeaderCellColored{Level Description}')), 
                        MultiRow(NoEscape(-3), data=NoEscape(r'\criterionBHeaderCellColored{Code}')), 
                        MultiRow(NoEscape(-3), data=NoEscape(r'\criterionBHeaderCellColored{Level}')), 
                        MultiRow(NoEscape(-3), data=NoEscape(r'\criterionBHeaderCellColored{Units supporting SFIA skill}')))

        criterionBTable.add_hline()
        criterionBTable.end_table_header()
        # table content
        for sfiaComponent in dataDictionary[key][0].keys():
            sfiaCode = sfiaComponent[0]
            sfiaLevel = sfiaComponent[1]
            unitList = dataDictionary[key][0][sfiaComponent][0]
            unitsSupportingSFIASkill = dataDictionary[key][0][sfiaComponent][1]
            sfiaSkill = dataDictionary[key][0][sfiaComponent][2]
            skillDescription = dataDictionary[key][0][sfiaComponent][3]
            levelDescription = dataDictionary[key][0][sfiaComponent][4].replace('_x000D_', '\n')
            criterionBTable.add_row(NoEscape(r'{%s}' % sfiaSkill),
                        NoEscape(r'{%s}' %skillDescription), 
                        NoEscape(r'{%s}' %levelDescription), 
                        f"{sfiaCode}", 
                        f"{sfiaLevel}", 
                        NoEscape(r'{%s}' %unitsSupportingSFIASkill))
            criterionBTable.add_hline()
        criterionBSubSubSection.append(criterionBTable)
        # criterionBSubSubSection.append(NoEscape(r'\end{adjustbox}'))
        criterionBSubSubSection.append(NewLine())
        criterionBSubSubSection.generate_tex(f"criterionB-{key.strip()}")
        criterionBList.append(f"criterionB-{key.strip()}.tex")
    return criterionBList

# Table 3. Criterion C
def createCriterionCTable(course, criterionC):
    criterionCList = []
    criterionCSubSubSection = Subsubsection(f'{course}\n')
    criterionCSubSubSection.append(NoEscape(r'\rubric{Criterion C Rubric}'))
    criterionCSubSubSection.append(NoEscape(r'\\[1em]'))
    criterionCSubSubSection.append(NewLine())
    criterionCSubSubSection.append(NoEscape(r'\begin{adjustbox}{max width=\textwidth}'))
    criterionCTable = Tabular(table_spec=r"|p{3cm}|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|")
    criterionCTable.add_hline()
    criterionCTable.add_row((
        "CBoK Knowledge Areas", 
        MultiColumn(8, align="|c|", data=NoEscape(r"\essentialKnowledgeCell ESSENTIAL CORE ICT KNOWLEDGE")),
        MultiColumn(11, align="|c|", data=NoEscape(r"\generalKnowledgeCell GENERAL ICT KNOWLEDGE"))
    ))
    criterionCTable.add_hline()
    
    # Format the course name to be multi-line
    formatted_course = course.replace(' ', r'\\')
    criterionCTable.add_row((
        MultiColumn(1, align="|c|", data=MultiRow(3, data=NoEscape(r"\begin{tabular}[c]{@{}c@{}}" + formatted_course + r"\end{tabular}"))), 
        MultiColumn(2, align="|c|", data=NoEscape(r"\lightGrayCell{Problem Solving}")), 
        MultiColumn(6, align="|c|", data=NoEscape(r"\professionalKnowledgeCell ICT Professional Knowledge")), 
        MultiColumn(3, align="|c|", data=NoEscape(r"\lightGrayCell{Technology Resources}")), 
        MultiColumn(4, align="|c|", data=NoEscape(r"\technologyBuildingCell Technology Building")), 
        MultiColumn(4, align="|c|", data=NoEscape(r"\lightGrayCell{ICT Management}"))
    ))
    criterionCTable.add_row((
        MultiColumn(1, align="|c|", data=""),
        MultiColumn(2, align="|c|", data=""),
        MultiColumn(6, align="|c|", data=""),
        MultiColumn(3, align="|c|", data=""),
        MultiColumn(4, align="|c|", data=""),
        MultiColumn(4, align="|c|", data="")
    ))
    criterionCTable.add_row((
        MultiColumn(1, align="|c|", data=""),
        MultiColumn(2, align="|c|", data=""),
        MultiColumn(6, align="|c|", data=""),
        MultiColumn(3, align="|c|", data=""),
        MultiColumn(4, align="|c|", data=""),
        MultiColumn(4, align="|c|", data="")
    ))
    criterionCTable.add_hline(2,20)
    criterionCTable.add_row((
        NoEscape(r'\rule{0pt}{175pt}'),
        NoEscape(r'\lightGrayCell{\myrotcell{Abstraction}}'),
        NoEscape(r'\lightGrayCell{\myrotcell{Design}}'),
        NoEscape(r'\lightBlueCell{\myrotcell{Ethics}}'),
        NoEscape(r'\lightBlueCell{\myrotcell{Professional expectations}}'),
        NoEscape(r'\lightBlueCell{\myrotcell{Teamwork concepts and issues}}'),
        NoEscape(r'\lightBlueCell{\myrotcell{Interpersonal communications}}'),
        NoEscape(r'\lightBlueCell{\myrotcell{Societal issues/legal issues/privacy}}'),
        NoEscape(r'\lightBlueCell{\myrotcell{Understanding the ICT profession}}'),
        NoEscape(r'\lightGrayCell{\myrotcell{Hardware \& software fundamentals}}'),
        NoEscape(r'\lightGrayCell{\myrotcell{Data \& information management}}'),
        NoEscape(r'\lightGrayCell{\myrotcell{Networking}}'),
        NoEscape(r'\lightBlueCell{\myrotcell{Programming}}'),
        NoEscape(r'\lightBlueCell{\myrotcell{Human factors}}'),
        NoEscape(r'\lightBlueCell{\myrotcell{Systems development}}'),
        NoEscape(r'\lightBlueCell{\myrotcell{Systems acquisition}}'),
        NoEscape(r'\lightGrayCell{\myrotcell{IT governance \& organisational issues}}'),
        NoEscape(r'\lightGrayCell{\myrotcell{IT project management}}'),
        NoEscape(r'\lightGrayCell{\myrotcell{Service management}}'),
        NoEscape(r'\lightGrayCell{\myrotcell{Cyber security}}')
    ))
    criterionCTable.add_hline()

    # Define the expected columns
    expected_columns = [
        ('Core', 'Abstraction'),
        ('Core', 'Design'),
        ('Professional', 'Ethics'),
        ('Professional', 'Professional expectations'),
        ('Professional', 'Teamwork concepts and issues'),
        ('Professional', 'Interpersonal communications'),
        ('Professional', 'Societal issues/legal issues/privacy'),
        ('Professional', 'Understanding the ICT profession'),
        ('Core', 'Hardware & software fundamentals'),
        ('Core', 'Data & information management'),
        ('Core', 'Networking'),
        ('Core', 'Programming'),
        ('Core', 'Human factors'),
        ('Core', 'Systems development'),
        ('Core', 'Systems acquisition'),
        ('Core', 'IT governance & organisational issues'),
        ('Core', 'IT project management'),
        ('Core', 'Service management'),
        ('Core', 'Cyber security')
    ]

    # Populate the table with data from criterionC.table_2_df
    for index, row in criterionC.table_2_df.iterrows():
        unit_name = index
        criterionCTable.add_row((MultiColumn(20, align="|l|", data=NoEscape(r"\colorcellverydarkblue " + unit_name)),))
        criterionCTable.add_hline()

        data_row = [NoEscape(r"\begin{tabular}[c]{@{}l@{}}Lectures\end{tabular}")]
        for column in expected_columns:
            if column in criterionC.table_2_df.columns:
                value = row[column]
                if pd.notna(value):
                    if column[0] == 'Professional' or column[0] == 'Core':
                        data_row.append(NoEscape(r'\lightBlueCell{X}'))
                    else:
                        data_row.append("X")
                else:
                    if column[0] == 'Professional' or column[0] == 'Core':
                        data_row.append(NoEscape(r'\lightBlueCell{}'))
                    else:
                        data_row.append("")
            else:
                # If the column is not in the DataFrame, add an empty cell
                if column[0] == 'Professional' or column[0] == 'Core':
                    data_row.append(NoEscape(r'\lightBlueCell{}'))
                else:
                    data_row.append("")

        criterionCTable.add_row(tuple(data_row))
        criterionCTable.add_hline()

    criterionCSubSubSection.append(criterionCTable)
    criterionCSubSubSection.append(NoEscape(r'\end{adjustbox}'))
    criterionCSubSubSection.append(NewLine())
    
    # Second table (unchanged)
    criterionCSubSubSection.append(NoEscape(r'\begin{longtable}{|p{0.25\textwidth}|p{0.10\textwidth}|p{0.10\textwidth}|p{0.45\textwidth}|}'))
    criterionCSubSubSection.append(NoEscape(r'\hline'))
    criterionCSubSubSection.append(NoEscape(r'\multicolumn{4}{|c|}{\textbf{Criterion C: Core Body of Knowledge (CBoK)}} \\'))
    criterionCSubSubSection.append(NoEscape(r'\hline'))
    criterionCSubSubSection.append(NoEscape(r'\textbf{CBoK outcome} & \textbf{Unit ID} & \textbf{Level ID} & \textbf{Justification} \\'))
    criterionCSubSubSection.append(NoEscape(r'\hline'))
    criterionCSubSubSection.append(NoEscape(r'\endhead'))
    
    # Use the entire table_3_df without filtering by course
    grouped = criterionC.table_3_df.groupby(['Outcome Group', 'Outcome'])
    
    for (outcome_group, outcome), group in grouped:
        cbok_outcome = f"{outcome_group} - {outcome}"
        
        for _, row in group.iterrows():
            unit_code = row['Unit Code + Unit Name'].split()[0]  # Extract unit code
            
            # Get the level from the original DataFrame
            level = criterionC.outcomes_mappings_df.loc[
                (criterionC.outcomes_mappings_df['Unit Code'] == unit_code) &
                (criterionC.outcomes_mappings_df['Outcome Group'] == outcome_group) &
                (criterionC.outcomes_mappings_df['Outcome'] == outcome),
                'Level (SFIA/Bloom/UnitOutcome)'
            ].values
            
            level = str(level[0]) if len(level) > 0 else 'N/A'
            
            justification = row['Justification']
            
            # Escape special characters for LaTeX
            cbok_outcome_escaped = cbok_outcome.replace('&', r'\&').replace('%', r'\%').replace('#', r'\#').replace('_', r'\_')
            justification_escaped = justification.replace('&', r'\&').replace('%', r'\%').replace('#', r'\#').replace('_', r'\_')
            
            criterionCSubSubSection.append(NoEscape(f"{cbok_outcome_escaped} & {unit_code} & {level} & {justification_escaped} \\\\"))
            criterionCSubSubSection.append(NoEscape(r'\hline'))

    criterionCSubSubSection.append(NoEscape(r'\end{longtable}'))
    
    criterionCSubSubSection.generate_tex(f"criterionC-{course.replace(' ', '_')}")
    criterionCList.append(f"criterionC-{course.replace(' ', '_')}.tex")
    return criterionCList

# Table 4. Criterion D
def createCriterionDTable(dataDictionary):
    criterionDList = []
    for course, criterionD in dataDictionary.items():
        if criterionD and hasattr(criterionD, 'criterion_df'):
            table_content = []
            for _, row in criterionD.criterion_df.iterrows():
                unit_code = row.get('Unit Code', '').strip()
                unit_name = row.get('Unit Name', '').strip()
                # assessment_item = row.get('Justification', '').strip()
                if(type(row.get('Justification')) == str):
                    justification = row.get('Justification', '').strip()
                    assessment_item = row.get('Justification', '').strip()
                else:
                    justification = ''
                    assessment_item = ''
                
                if not (unit_code or unit_name or assessment_item or justification):
                    continue
                
                unit_code_and_name = f"{unit_code} {unit_name}".strip()
                
                justification = justification.replace('&', r'\&').replace('%', r'\%').replace('#', r'\#').replace('_', r'\_')
                assessment_item = assessment_item.replace('&', r'\&').replace('%', r'\%').replace('#', r'\#').replace('_', r'\_')
                
                table_content.append((unit_code_and_name, assessment_item, justification))

            if table_content:
                criterionDSubSubSection = Subsubsection(NoEscape(r'\criterionDcoursetitle{' + course + r'} \\\\'))
                criterionDSubSubSection.append(NoEscape(r'\rubric{Criterion D Rubric} \\\\'))

                # Start longtable using the new command
                criterionDSubSubSection.append(NoEscape(r'\criterionDtable'))
                
                # Table header
                criterionDSubSubSection.append(NoEscape(r'\hline'))
                criterionDSubSubSection.append(NoEscape(r'\multicolumn{3}{|l|}{\colorcelldarkbluebold Criterion D: Advanced ICT Units Addressing Complex Computing} \\'))
                criterionDSubSubSection.append(NoEscape(r'\hline'))
                criterionDSubSubSection.append(NoEscape(r'\colorcelllightblueitalic Unit Code \& Title & \colorcelllightblueitalic Assessment Item & \colorcelllightblueitalic Complex Computing Criteria met \\'))
                criterionDSubSubSection.append(NoEscape(r'\hline'))
                criterionDSubSubSection.append(NoEscape(r'\endfirsthead'))

                # Continuation header
                criterionDSubSubSection.append(NoEscape(r'\hline'))
                criterionDSubSubSection.append(NoEscape(r'\multicolumn{3}{|l|}{\colorcelldarkbluebold Criterion D: Advanced ICT Units Addressing Complex Computing (continued)} \\'))
                criterionDSubSubSection.append(NoEscape(r'\hline'))
                criterionDSubSubSection.append(NoEscape(r'\colorcelllightblueitalic Unit Code \& Title & \colorcelllightblueitalic Assessment Item & \colorcelllightblueitalic Complex Computing Criteria met \\'))
                criterionDSubSubSection.append(NoEscape(r'\hline'))
                criterionDSubSubSection.append(NoEscape(r'\endhead'))

                # Add table content using the new column commands
                for row in table_content:
                    criterionDSubSubSection.append(NoEscape(
                        r'\unitcolumn{' + row[0] + r'} & \assessmentcolumn{' + row[1] + r'} & \complexcomputingcolumn{' + row[2] + r'} \\'
                    ))
                    criterionDSubSubSection.append(NoEscape(r'\hline'))

                criterionDSubSubSection.append(NoEscape(r'\end{longtable}'))
                
                # Add some vertical space between tables
                criterionDSubSubSection.append(NoEscape(r'\vspace{1em}'))

                criterionDSubSubSection.generate_tex(f"criterionD-{course.strip()}")
                criterionDList.append(f"criterionD-{course.strip()}.tex")
    return criterionDList

# Table 5. Criterion E
def createCriterionETable(dataDictionary):
    criterionEList = []
    
    for course, courseData in dataDictionary.items():
        if courseData:  # Only process courses with data
            # Add the course title using the command
            criterionESubSubSection = Subsubsection(NoEscape(r'\coursetitle{' + course + '} \\\\'))
            criterionESubSubSection.append(NoEscape(r'\rubric{Criterion E Rubric} \\\\'))
            
            # Start the tabular environment using the command
            criterionESubSubSection.append(NoEscape(r'\criterionTable'))
            criterionESubSubSection.append(NoEscape(r'\hline'))
            criterionESubSubSection.append(NoEscape(r'\multicolumn{2}{|l|}{\colorcelldarkbluebold Criterion E: Integrated and Applied ICT Knowledge} \\'))
            criterionESubSubSection.append(NoEscape(r'\hline'))
            criterionESubSubSection.append(NoEscape(r'\colorcelllightblueitalic Unit Code \& Title & \colorcelllightblueitalic Notes in support of Claim \\'))
            criterionESubSubSection.append(NoEscape(r'\hline'))
            
            for row in courseData:
                unit_code = row.get('Unit Code', '')
                unit_name = row.get('Unit Name', '')
                justification = row.get('Justification', '')
                
                # Combine Unit Code and Unit Name
                unit_code_and_name = f"{unit_code} {unit_name}"
                
                # Use the new specific column commands
                wrapped_unit_code_and_name = NoEscape(r'\unitcodecolumn{' + unit_code_and_name + '}')
                wrapped_justification = NoEscape(r'\justificationcolumn{' + justification + '}')
                
                criterionESubSubSection.append(NoEscape(f"{wrapped_unit_code_and_name} & {wrapped_justification} \\\\"))
                criterionESubSubSection.append(NoEscape(r'\hline'))
            
            criterionESubSubSection.append(NoEscape(r'\end{tabular}'))
            criterionESubSubSection.append(NoEscape(r'\\[1em]'))  # Add some space after each table
            criterionESubSubSection.generate_tex(f"criterionE-{course.strip()}")
            criterionEList.append(f"criterionE-{course.strip()}.tex")
    return criterionEList    

# main function
def populateCriterionBDictionary(criterionBItems, sfia):
    criterionBList = {}

    #Criterion B
    for course, criterionB in criterionBItems.items():
        courseName = course
        value = {}
        for tableElement in criterionB.criterion_df.groupby(['Outcome','Level (SFIA/Bloom/UnitOutcome)']).agg(lambda x: ';'.join(x.astype(str)) if not x.empty else '').iterrows():
            cleanUpJustification = set(tableElement[1]['Justification'].split(";"))
            cleanUpJustification.discard('nan')
            joinedJustification = ';'.join(str(element) for element in cleanUpJustification)
            outcomeCode = tableElement[0][0]
            sfiaLevel = tableElement[0][1]
            sfiaSkillName = sfia[outcomeCode][sfiaLevel]['Skill']
            sfiaSkillDescription = sfia[outcomeCode][sfiaLevel]['Description']
            sfiaLevelDescription = sfia[outcomeCode][sfiaLevel]['Description22']
            value[(outcomeCode, sfiaLevel)] = [tableElement[1]['Unit Code'], joinedJustification, sfiaSkillName, sfiaSkillDescription, sfiaLevelDescription]
        if len(value) > 0:
            professionalRoleForSkill = ' + '.join(criterionBItems[courseName].roles)
            criterionBList[f"{courseName}"] = [value, professionalRoleForSkill]
    return criterionBList

    #CriterionC
    

    #Criterion D 
def populateCriterionDDictionary(criterionDItems):
    criterionDList = {}
    for course, criterionD in criterionDItems:
        if hasattr(criterionD, 'criterion_df'):
            # Ensure all necessary columns are present
            required_columns = ['Unit Code', 'Unit Title', 'Complex Computing Criteria met']
            for col in required_columns:
                if col not in criterionD.criterion_df.columns:
                    criterionD.criterion_df[col] = ''
            criterionDList[course] = criterionD
    return criterionDList
    
    #Criterion E
def populateCriterionEDictionary(criterionEItems):
    criterionEList = {}
    for course, criterionE in criterionEItems:
        if criterionE.criterion_df is not None and not criterionE.criterion_df.empty:
            # Ensure 'Justification' column exists, if not, add an empty one
            if 'Justification' not in criterionE.criterion_df.columns:
                criterionE.criterion_df['Justification'] = ''
            criterionEList[course] = criterionE.criterion_df.to_dict('records')
        else:
            criterionEList[course] = []
    return criterionEList

def generateLatex(sortBy, clientInputFile, sfiaFile, caidiInput, generateCriterionDictionary):
    sfia = SFIA(sfiaFile)
    cd = CAIDI( caidiInput )
    kb = KnowledgeBase(clientInputFile, sfia, cd)
    #sort by criterion
    geometry_options = {"tmargin": "0.5in", "lmargin": "0.5in", "bmargin": "0.5in", "rmargin": "0.5in"}
    doc = Document(documentclass="report",geometry_options=geometry_options)
    doc.packages.append(Package('multirow'))
    doc.packages.append(Package('makecell'))
    doc.packages.append(Package('rotating'))
    doc.packages.append(Package('adjustbox'))
    doc.packages.append(Package('latexStyleSheet'))
    doc.packages.append(Package('longtable'))
    doc.preamble.append(NoEscape(r'\usepackage[table]{xcolor}'))
    
    # check for parameter dictionary, create table list, and add table name to the list
    if(generateCriterionDictionary["generateCriterionA"]):
        criterionAFileNameList = createCriterionATable("MIT",["CITS4401"])
    
    if(generateCriterionDictionary["generateCriterionB"]):
        criterionBList = populateCriterionBDictionary(kb.criterionB, sfia)
        criterionBFileNameList = createCriterionBTable(criterionBList)

    if(generateCriterionDictionary["generateCriterionC"]):
        criterionCFileNameList = []
    for course, criterionC in kb.criterionC.items():
        criterionCFileNameList.extend(createCriterionCTable(course, criterionC))
        
    if(generateCriterionDictionary["generateCriterionD"]):
        criterionDList = populateCriterionDDictionary(kb.criterionD.items())
        criterionDFileNameList = createCriterionDTable(criterionDList)
    
    if(generateCriterionDictionary["generateCriterionE"]):
        criterionEList = populateCriterionEDictionary(kb.criterionE.items())
        criterionEFileNameList = createCriterionETable(criterionEList)
    
    if(sortBy == 'criterion'):
        # Sort by criterion
        if(generateCriterionDictionary["generateCriterionA"]):
        ## Add section for criterion A
            criterionASection = Section("Criterion A: Program Design")
            for nameList in criterionAFileNameList:
                criterionASection.append(NoEscape(r'\include{%s}' %nameList))
            doc.append(criterionASection)
        
        if(generateCriterionDictionary["generateCriterionB"]):
            ## Add section for criterion B
            criterionBSection = Section("Criterion B: Professional ICT Role and Skills")
            for nameList in criterionBFileNameList:
                criterionBSection.append(NoEscape(r'\include{%s}' %nameList))
            doc.append(criterionBSection)
            ## add justification table description table

        if(generateCriterionDictionary["generateCriterionC"]):
            ## Add section for criterion C
            criterionCSection = Section("Criterion C: Program Design")
            criterionCSection.append("Mapping of Units to the Australian Computer Society’s Core Body of Knowledge (CBoK)\n")
            criterionCSection.append("Lorem Ipsum 2\n")
            for nameList in criterionCFileNameList:
                criterionCSection.append(NoEscape(r'\include{%s}' %nameList))
            doc.append(criterionCSection)

        ## Add section for criterion D
        if(generateCriterionDictionary["generateCriterionD"]):
            criterionDSection = Section("Criterion D: Advanced ICT Units Addressing Complex Computing")
            for nameList in criterionDFileNameList:
                criterionDSection.append(NoEscape(r'\include{%s}' %nameList)),
            doc.append(criterionDSection)

        ## Add section for criterion E
        if(generateCriterionDictionary["generateCriterionE"]):
            criterionESection = Section("Criterion E: Integrated and Applied ICT Knowledge")
            for nameList in criterionEFileNameList:
                criterionESection.append(NoEscape(r'\include{%s}' %nameList)),    
            doc.append(criterionESection)    

    # Sort by program
    elif(sortBy == 'program'):
        courseDictionary = {}
        
        for fileName in criterionBFileNameList:
            if(fileName.replace(".tex", "").replace("criterionB-", "") not in courseDictionary):
                courseDictionary[fileName.replace(".tex", "").replace("criterionB-", "")] = [fileName]
            else:
                tempList = courseDictionary[fileName.replace(".tex", "").replace("criterionB-", "")]
                tempList.append(fileName)
                courseDictionary[fileName.replace(".tex", "").replace("criterionB-", "")] = tempList
                
        for fileName in criterionDFileNameList:
            if(fileName.replace(".tex", "").replace("criterionD-", "") not in courseDictionary):
                courseDictionary[fileName.replace(".tex", "").replace("criterionD-", "")] = [fileName]
            else:
                tempList = courseDictionary[fileName.replace(".tex", "").replace("criterionD-", "")]
                tempList.append(fileName)
                courseDictionary[fileName.replace(".tex", "").replace("criterionD-", "")] = tempList
        
        for fileName in criterionEFileNameList:
            if(fileName.replace(".tex", "").replace("criterionE-", "") not in courseDictionary):
                courseDictionary[fileName.replace(".tex", "").replace("criterionE-", "")] = [fileName]
            else:
                tempList = courseDictionary[fileName.replace(".tex", "").replace("criterionE-", "")]
                tempList.append(fileName)
                courseDictionary[fileName.replace(".tex", "").replace("criterionE-", "")] = tempList
        
        for course in courseDictionary:
            criterionCourseSection = Section(f"{course}")

            if(generateCriterionDictionary["generateCriterionA"]):
                criterionCourseSection.append("Criterion A: Program Design\n")
                # criterionASection.append(NoEscape(r'\include{%s}' %nameList))

            if(generateCriterionDictionary["generateCriterionB"]):
                criterionCourseSection.append("Criterion B: Professional ICT Role and Skills\n")
                criterionCourseSection.append(NoEscape(r'\include{%s}' %courseDictionary[course][0]))

            if(generateCriterionDictionary["generateCriterionC"]):
                ## Add section for criterion C
                criterionCSection = Section("Criterion C: Core Body of Knowledge")
                criterionCSection.append("Mapping of Units to the Australian Computer Society's Core Body of Knowledge (CBoK)\n")
                for nameList in criterionCFileNameList:
                    criterionCSection.append(NoEscape(r'\include{%s}' %nameList))
                doc.append(criterionCSection)
                # criterionASection.append(NoEscape(r'\include{%s}' %nameList))

            if(generateCriterionDictionary["generateCriterionD"]):
                criterionCourseSection.append("Criterion D: Program Design\n")
                criterionCourseSection.append(NoEscape(r'\include{%s}' %courseDictionary[course][1]))

            if(generateCriterionDictionary["generateCriterionE"]):
                criterionCourseSection.append("Criterion E: Program Design\n")
                criterionCourseSection.append(NoEscape(r'\include{%s}' %courseDictionary[course][2]))

            # if(generateCriterionDictionary["generateCriterionA"]):
            #     criterionASection = Subsection("Criterion A: Program Design")
            #     # criterionASection.append(NoEscape(r'\include{%s}' %nameList))
            #     criterionCourseSection.append(criterionASection)

            # if(generateCriterionDictionary["generateCriterionB"]):
            #     criterionBSection = Subsection("Criterion B: Professional ICT Role and Skills")
            #     criterionBSection.append(NoEscape(r'\include{%s}' %courseDictionary[course][0]))
            #     criterionCourseSection.append(criterionBSection)

            # if(generateCriterionDictionary["generateCriterionC"]):
            #     criterionCSection = Subsection("Criterion C: Program Design")
            #     criterionCSection.append("Mapping of Units to the Australian Computer Society’s Core Body of Knowledge (CBoK)\n")
            #     criterionCSection.append("Lorem Ipsum 2\n")
            #     # criterionASection.append(NoEscape(r'\include{%s}' %nameList))
            #     criterionCourseSection.append(criterionCSection)

            # if(generateCriterionDictionary["generateCriterionD"]):
            #     criterionDSection = Subsection("Criterion D: Program Design")
            #     criterionDSection.append(NoEscape(r'\include{%s}' %courseDictionary[course][1]))
            #     criterionCourseSection.append(criterionDSection)

            # if(generateCriterionDictionary["generateCriterionE"]):
            #     criterionESection = Subsection("Criterion E: Program Design")
            #     criterionESection.append(NoEscape(r'\include{%s}' %courseDictionary[course][2]))
            #     criterionCourseSection.append(criterionESection)
        
            doc.append(criterionCourseSection)   


    doc.generate_tex("main")

def main():
    parser = argparse.ArgumentParser(description="Program to generate latex files for ACS submission")
    # Add arguments
    parser.add_argument('-s', '--sort', type=str, help='Sort By', default='criterion')
    parser.add_argument('-i', '--clientInput', type=str, help='Client Excel Input File', default='input.xlsx')
    parser.add_argument('-si', '--sfiaInput', type=str, help='SFIA Input File', default='sfia.xlsx')
    parser.add_argument('-ci', '--caidiInput', type=str, help='Caidi Input File', default='caidi.zip')
    parser.add_argument('-ca', '--criterionA', type=bool, help='Generate Criterion A', default=True)
    parser.add_argument('-cb', '--criterionB', type=bool, help='Generate Criterion B', default=True)
    parser.add_argument('-cc', '--criterionC', type=bool, help='Generate Criterion C', default=True)
    parser.add_argument('-cd', '--criterionD', type=bool, help='Generate Criterion D', default=True)
    parser.add_argument('-ce', '--criterionE', type=bool, help='Generate Criterion E', default=True)
    
    # Parse the arguments
    args = parser.parse_args()
    sortBy = args.sort
    clientInputFile = args.clientInput
    sfiaInputFile = args.sfiaInput
    caidiInputFile = args.caidiInput
    generateCriterionA = args.criterionA
    generateCriterionB = args.criterionB
    generateCriterionC = args.criterionC
    generateCriterionD = args.criterionD
    generateCriterionE = args.criterionE

    generateCriterionDictionary = {
        "generateCriterionA": generateCriterionA,
        "generateCriterionB": generateCriterionB,
        "generateCriterionC": generateCriterionC,
        "generateCriterionD": generateCriterionD,
        "generateCriterionE": generateCriterionE
    }
    
    generateLatex(sortBy, clientInputFile, sfiaInputFile, caidiInputFile, generateCriterionDictionary)

    with zipfile.ZipFile('latex_output.zip', 'w') as zipf:
    # Loop through all files in the folder
        for foldername, subfolders, filenames in os.walk('.'):
            for filename in filenames:
                # Check if the file ends with the desired extension
                if filename.endswith('.tex'):
                    file_path = os.path.join(foldername, filename)
                    # Add the file to the Zip archive
                    zipf.write(file_path, os.path.relpath(file_path, '.'))
                if filename.endswith('.sty'):
                    file_path = os.path.join(foldername, filename)
                    # Add the file to the Zip archive
                    zipf.write(file_path, os.path.relpath(file_path, '.'))

if __name__ == "__main__":
    main()