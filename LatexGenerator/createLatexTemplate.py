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
def createCriterionATable(dataDictionary):
    criterionAList = []
    for key in dataDictionary:
        ### Start loop for each program
        criterionASubSubSection = Subsubsection(f'{key}')
        criterionATable = LongTable(table_spec="|p{\criterionAEmptyCol}|p{\criterionACodeCol}|p{\criterionATitleCol}|p{\criterionACoordinatorCol}|p{\criterionAFileCol}|")
        criterionATable.add_hline()
        criterionATable.add_row((MultiColumn(5, align="|l|", data=NoEscape(r'\cellcolor{colorDarkBlue}')),))
        criterionATable.add_row((MultiColumn(5, align="|l|", data=NoEscape(r'\criterionAHeader{Program Details}')),))
        criterionATable.add_hline()
        criterionATable.add_row((MultiColumn(2, align="|l|", data=NoEscape(r'\colorcelllightblueitalic Code')), (MultiColumn(3, align="|l|", data=dataDictionary[key]["code"]))))
        criterionATable.add_hline()
        criterionATable.add_row((MultiColumn(2, align="|l|", data=NoEscape(r'\colorcelllightblueitalic Award title on Transcript/Testamur')), (MultiColumn(3, align="|l|", data=dataDictionary[key]["award_title"]))))
        criterionATable.add_hline()
        criterionATable.add_row((MultiColumn(2, align="|l|", data=NoEscape(r'\colorcelllightblueitalic EFT Years of Study')), (MultiColumn(3, align="|l|", data=dataDictionary[key]["eft"]))))
        criterionATable.add_hline()
        criterionATable.add_row((MultiColumn(2, align="|l|", data=NoEscape(r'\colorcelllightblueitalic First Year of Offer')), (MultiColumn(3, align="|l|", data=dataDictionary[key]["first_year_offered"]))))
        criterionATable.add_hline()
        criterionATable.add_row((MultiColumn(5, align="|l|", data=NoEscape(r'\cellcolor{colorDarkBlue}')),))
        criterionATable.add_row((MultiColumn(5, align="|l|", data=NoEscape(r'\criterionAHeader{Personnel}')),))
        criterionATable.add_hline()
        criterionATable.add_row((MultiColumn(2, align="|l|", data=NoEscape(r'\colorcelllightblueitalic Program Chair')), (MultiColumn(3, align="|l|", data=dataDictionary[key]["program_chair"]))))
        criterionATable.add_hline()
        criterionATable.add_row((MultiColumn(2, align="|l|", data=NoEscape(r'\colorcelllightblueitalic ICT Industry Liaison')), (MultiColumn(3, align="|l|", data=dataDictionary[key]["industry_liasion"]))))
        criterionATable.add_hline()
        criterionATable.add_row((MultiColumn(2, align="|l|", data=NoEscape(r'\colorcelllightblueitalic Key Academic Staff')), (MultiColumn(3, align="|l|", data=dataDictionary[key]["key_academic_staff"]))))
        criterionATable.add_hline()
        criterionATable.add_row((MultiColumn(5, align="|l|", data=NoEscape(r'\cellcolor{colorDarkBlue}')),))
        criterionATable.add_row((MultiColumn(5, align="|l|", data=NoEscape(r'\criterionAHeader{Outcomes}')),))
        criterionATable.add_hline()
        criterionATable.add_row((MultiColumn(5, align="|l|", data=NoEscape(r'\criterionAOutcomes{'+ dataDictionary[key]["outcomes"].replace('\n', ' \\\\ \\\\ ') +'}')),))
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
            NoEscape(r'\cellcolor{colorLightBlue}\textbf{Level}'),
            NoEscape(r'\cellcolor{colorLightBlue}\textbf{Code}'),
            NoEscape(r'\cellcolor{colorLightBlue}\textbf{Title}'),
            NoEscape(r'\cellcolor{colorLightBlue}\textbf{Unit Coordinator(s)}'),
            NoEscape(r'\cellcolor{colorLightBlue}\textbf{File \#}'),
        ))
        criterionATable.add_hline()
        for level in dataDictionary[key]["dataFrameGroupByLevel"]:
            groupByCourseType = {}
            for unit in dataDictionary[key]["dataFrameGroupByLevel"][level]:
                courseType = unit[key]
                if(courseType in groupByCourseType.keys()):
                    temp = groupByCourseType[courseType]
                    temp.append(unit)
                    groupByCourseType[courseType] = temp
                else:
                    groupByCourseType[courseType] = [unit]
            sorted_dict = dict(sorted(groupByCourseType.items()))
            for courseTypeIter in sorted_dict:
                for eachRow in range(len(groupByCourseType[courseTypeIter])):
                    unitCode = groupByCourseType[courseTypeIter][eachRow]['Unit Code']
                    unitName = groupByCourseType[courseTypeIter][eachRow]['Unit Name']
                    if(eachRow == 0):
                        criterionATable.add_row(NoEscape(r'\cellcolor{colorLightBlue}'), MultiColumn(4, align="|l|", data=NoEscape(r'\colorcellgreyitalic {%s}' %courseTypeIter)))                        
                        criterionATable.add_hline(2,5)
                        criterionATable.add_row(NoEscape(r'\cellcolor{colorLightBlue}'), NoEscape(unitCode), NoEscape(unitName), NoEscape(r''), NoEscape(r''))
                    elif(eachRow == len(groupByCourseType[courseTypeIter])-1):
                        criterionATable.add_row(MultiRow(NoEscape(-len(groupByCourseType[courseTypeIter])), data=NoEscape(r'\cellcolor{colorLightBlue}\textbf{%s}' %str(level))), NoEscape(unitCode), NoEscape(unitName), NoEscape(r''), NoEscape(r''))
                    else:
                        criterionATable.add_row(NoEscape(r'\cellcolor{colorLightBlue}'), NoEscape(unitCode), NoEscape(unitName), NoEscape(r''), NoEscape(r''))
                    if(eachRow == len(groupByCourseType[courseTypeIter])-1):
                        criterionATable.add_hline()
                    else:
                        criterionATable.add_hline(2,5)
        criterionASubSubSection.append(criterionATable)
        # Start longtable using the new command
        criterionASubSubSection.append(NoEscape(r'\begin{longtable}{|p{1\textwidth}|}%'))
        criterionASubSubSection.append(NoEscape(r'\hline%'))
        criterionASubSubSection.append(NoEscape(r'{\colorcelldarkbluebold Justification of Program Design} \\%'))
        criterionASubSubSection.append(NoEscape(r'\hline%'))
        criterionASubSubSection.append(NoEscape(r'{%s} \\' %dataDictionary[key]["justification"]))
        criterionASubSubSection.append(NoEscape(r'\hline%'))
        criterionASubSubSection.append(NoEscape(r'\end{longtable}%'))
        criterionASubSubSection.append(NoEscape(r'\rubric{Criterion A Rubric}'))
        criterionASubSubSection.generate_tex(f"criterionA-{key.strip()}")
        criterionAList.append(f"criterionA-{key.strip()}.tex")
    return criterionAList

# Table 2. Criterion B
def createCriterionBTable(dataDictionary):
    criterionBList = []
    ### Start loop for each program
    for key in dataDictionary:
        criterionBSubSubSection = Subsubsection(f"{key}")
        professionalSkills = dataDictionary[key][1]
        criterionBSubSubSection.append(f"ICT professional role: {professionalSkills}\n")
        sfiaSkills = ""
        for sfiaComponent in dataDictionary[key][0].keys():
            sfiaSkills = sfiaSkills+"+"+sfiaComponent[0]
        criterionBSubSubSection.append(f"SFIA skills: {sfiaSkills[1:]}\n")
        criterionBTable = LongTable(table_spec=NoEscape(r'|p{0.2\textwidth}|p{0.25\textwidth}|p{0.4\textwidth}|p{0.05\textwidth}|p{0.05\textwidth}|p{0.25\textwidth}|'))
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
        # Add some vertical space between tables
        criterionBSubSubSection.append(NoEscape(r'\vspace{1em}'))
        criterionBSubSubSection.append(NoEscape(r'\rubric{Criterion B Rubric || SFIA Code ( ) || SFIA Level ( ) || Unit Supporting SFIA Skill ( ) || SFIA Skill ( ) || Skill Description ( ) || Level Description ( )}'))
        criterionBSubSubSection.generate_tex(f"criterionB-{key.strip()}")
        criterionBList.append(f"criterionB-{key.strip()}.tex")
    return criterionBList

# Additional Table - Criterion B Justification Explanation
def createCriterionBJustificationTable(justificationdf):
    justificationExlpanationSubSubSection = Subsubsection("Justification Explanation")
    justificationExplanationTable = LongTable(table_spec=NoEscape(r'|p{0.3\textwidth}|p{0.7\textwidth}|'))
    justificationExplanationTable.add_hline()
    justificationExplanationTable.add_row(NoEscape(r'\criterionBHeaderCellColored{Justification Code}'),NoEscape(r'\criterionBHeaderCellColored{Justification Explanation}'))
    justificationExplanationTable.add_hline()
    justificationExplanationTable.end_table_header()
    for justification in justificationdf:
        justificationExplanationTable.add_row(justification, justificationdf[justification])
        justificationExplanationTable.add_hline()
    justificationExlpanationSubSubSection.append(justificationExplanationTable)
    justificationExlpanationSubSubSection.generate_tex("criterionB-justification_explanation")
    return "criterionB-justification_explanation.tex"

# Table 3. Criterion C
def createCriterionCTable(course, criterionC):
    criterionCList = []
    criterionCSubSubSection = Subsubsection(f'{course}\n')
    criterionCSubSubSection.append(NoEscape(r'\rubric{Criterion C Rubric}'))
    criterionCSubSubSection.append(NoEscape(r'\begin{adjustbox}{max width=\textwidth, center}'))
    criterionCTable = Tabular(table_spec=r"|p{9cm}|" + "p{0.9cm}|" * 14)
    criterionCTable.add_hline()
    criterionCTable.add_row((
        "CBoK Knowledge Areas", 
        MultiColumn(5, align="|c|", data=NoEscape(r"\cellcolor{lightOrange}")),
        MultiColumn(8, align="|c|", data=NoEscape(r"\cellcolor{lightGreen}")),
        MultiColumn(1, align="|c|", data=NoEscape(r"\cellcolor{colorLightBlue}"))
    ))
    criterionCTable.add_row((
        MultiColumn(1, align="|c|", data=""),
        MultiColumn(5, align="|c|", data=NoEscape(r"\criterionCEssentialHeader{PROFESSIONAL}")),
        MultiColumn(8, align="|c|", data=NoEscape(r"\criterionCGeneralHeader{CORE}")),
        MultiColumn(1, align="|c|", data=NoEscape(r"\lightGrayCell{IN-DEPTH}"))
    ))
    criterionCTable.add_hline()
    
    # Format the course name to be multi-line and centered
    formatted_course = course.replace(' ', r'\\')
    criterionCTable.add_row((
        MultiColumn(1, align="|c|", data=MultiRow(3, data=NoEscape(r"\raisebox{-10em}{\begin{tabular}[c]{@{}c@{}}" + formatted_course + r"\end{tabular}}"))), 
        # MultiColumn(14, align="|c|", data="") # maybe need to be changed to individual color
        NoEscape(r'\ictEthicsCell'),
        NoEscape(r'\impactsOfICTCell'),
        NoEscape(r'\workingIndividuallyTeamworkCell'),
        NoEscape(r'\professionalCommunicationCell'),
        NoEscape(r'\theProfessionalPractitionerCell'),
        NoEscape(r'\criterionCGeneralHeader{}'),
        NoEscape(r'\criterionCGeneralHeader{}'),
        NoEscape(r'\criterionCGeneralHeader{}'),
        NoEscape(r'\criterionCGeneralHeader{}'),
        NoEscape(r'\criterionCGeneralHeader{}'),
        NoEscape(r'\cyberSecurityCell'),
        NoEscape(r'\ictProjectManagementCell'),
        NoEscape(r'\criterionCGeneralHeader{}'),
        NoEscape(r'')
    ))
    
    criterionCTable.add_row((
        NoEscape(r'\rule{0pt}{200pt}'),
        NoEscape(r'\ictEthicsCell\myrotcell{ICT Ethics}'),
        NoEscape(r'\impactsOfICTCell\myrotcell{Impacts of ICT}'),
        NoEscape(r'\workingIndividuallyTeamworkCell\myrotcell{Working Individually \& Teamwork}'),
        NoEscape(r'\professionalCommunicationCell\myrotcell{Professional Communication}'),
        NoEscape(r'\theProfessionalPractitionerCell\myrotcell{The Professional Practitioner}'),
        NoEscape(r'\criterionCGeneralHeader{\myrotcell{ICT Fundamentals}}'),
        NoEscape(r'\criterionCGeneralHeader{\myrotcell{ICT Infrastructure}}'),
        NoEscape(r'\criterionCGeneralHeader{\myrotcell{Information \& Data Science \& Engineering}}'),
        NoEscape(r'\criterionCGeneralHeader{\myrotcell{Computational Science \& Engineering}}'),
        NoEscape(r'\criterionCGeneralHeader{\myrotcell{Application Systems}}'),
        NoEscape(r'\cyberSecurityCell\myrotcell{Cyber Security}'),
        NoEscape(r'\ictProjectManagementCell\myrotcell{ICT Project Management}'),
        NoEscape(r'\criterionCGeneralHeader{\myrotcell{ICT Management \& Governance}}'),
        NoEscape(r'\myrotcell{In-depth Knowledge}')
    ))
    criterionCTable.add_hline()

    # Define the expected columns
    expected_columns = [
        ('Professional', 'ICT Ethics'),
        ('Professional', 'Impacts of ICT'),
        ('Professional', 'Working Individually & Teamwork'),
        ('Professional', 'Professional Communication'),
        ('Professional', 'The Professional Practitioner'),
        ('Core', 'ICT Fundamentals'),
        ('Core', 'ICT Infrastructure'),
        ('Core', 'Information & Data Science & Engineering'),
        ('Core', 'Computational Science & Engineering'),
        ('Core', 'Application Systems'),
        ('Core', 'Cyber Security'),
        ('Core', 'ICT Project Management'),
        ('Core', 'ICT Management & Governance'),
        ('In-depth', 'In-depth Knowledge')
    ]

    # Populate the table with data from criterionC.table_2_df
    for index, row in criterionC.table_2_df.iterrows():
        unit_name = index
        
        data_row = [NoEscape(r"\begin{tabular}[c]{@{}l@{}}" + unit_name + r"\end{tabular}")]
        for column in expected_columns:
            if column in criterionC.table_2_df.columns:
                value = row[column]
                if pd.notna(value):
                    data_row.append(NoEscape(r"\cellcolor{white}"))  # Changed from lightGray to white
                else:
                    data_row.append("")
            else:
                data_row.append("")

        criterionCTable.add_row(tuple(data_row))
        criterionCTable.add_hline()

    criterionCSubSubSection.append(criterionCTable)
    criterionCSubSubSection.append(NoEscape(r'\end{adjustbox}'))
    criterionCSubSubSection.append(NewLine())
    
    # Additional Table - Criterion C Justification Explanation
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
    
    criterionCSubSubSection.generate_tex(f"criterionC-{course.strip()}")
    criterionCList.append(f"criterionC-{course.strip()}.tex")
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
                assessment_item = row.get('Assessment Item (for D: Advanced Algorithms and C: CBoK mapping)', '').strip()
                if(type(row.get('Justification')) == str):
                    justification = row.get('Justification', '').strip()
                else:
                    justification = ''
                
                if not (unit_code or unit_name or assessment_item or justification):
                    continue
                
                unit_code_and_name = f"{unit_code} {unit_name}".strip()
                
                justification = justification.replace('&', r'\&').replace('%', r'\%').replace('#', r'\#').replace('_', r'\_')
                assessment_item = assessment_item.replace('&', r'\&').replace('%', r'\%').replace('#', r'\#').replace('_', r'\_')
                
                table_content.append((unit_code_and_name, assessment_item, justification))

            if table_content:
                criterionDSubSubSection = Subsubsection(NoEscape(r'\criterionDcoursetitle{' + course + r'} \\\\'))
                criterionDSubSubSection.append(NoEscape(r'\rubric{Criterion D Rubric}'))

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
            criterionESubSubSection.append(NoEscape(r'\rubric{Criterion E Rubric}'))
            
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
def populateCriterionADictionary(criterionA):
    criterionAList = {}
    for course, criterionA in criterionA:
        courseName = course
        criterionA_df = criterionA.criterion_df
        # group by create a dictionary with level as first key the value is another dictionary with type as the key
        groupByLevel = {}
        for row in criterionA_df.iterrows():
            if(row[1]["Level"] in groupByLevel.keys()):
                temp = groupByLevel[row[1]["Level"]]
                temp.append(row[1])
                groupByLevel[row[1]["Level"]] = temp
            else:
                groupByLevel[row[1]["Level"]] = [row[1]]
        try:
            code = criterionA.code
            award_title = criterionA.award_title
            eft = criterionA.eft
            first_year_offered = criterionA.first_year_offered
            program_chair = criterionA.program_chair
            industry_liasion = criterionA.industry_liasion
            key_academic_staff = criterionA.key_academic_staff
            outcomes = criterionA.outcomes
            justification = criterionA.justification
        except AttributeError:
            code = "placeholderValue"
            award_title = "placeholderValue"
            eft = "placeholderValue"
            first_year_offered = "placeholderValue"
            program_chair = "placeholderValue"
            industry_liasion = "placeholderValue"
            key_academic_staff = "placeholderValue"
            outcomes = "placeholderValue"
            justification = "placeholderValue"
        criterionAList[courseName] = {
            "dataFrame":criterionA_df,
            "dataFrameGroupByLevel":groupByLevel,
            "code":code,
            "award_title":award_title,
            "eft":eft,
            "first_year_offered":first_year_offered,
            "program_chair":program_chair,
            "industry_liasion":industry_liasion,
            "key_academic_staff":key_academic_staff,
            "outcomes":outcomes,
            "justification":justification
        }
    return criterionAList

def populateCriterionBDictionary(criterionBItems, sfia):
    criterionBList = {}
    justificationExplanationList = {}
    #Criterion B
    for course, criterionB in criterionBItems.items():
        courseName = course
        value = {}
        for tableElement in criterionB.criterion_df.groupby(['Outcome','Level (SFIA/Bloom/UnitOutcome)']).agg(lambda x: ';'.join(x.astype(str)) if not x.empty else '').iterrows():
            cleanUpJustification = set(tableElement[1]['Justification'].split(";"))
            cleanUpJustification.discard('nan')
            joinedJustification = ';'.join(str(element) for element in cleanUpJustification)
            cleanUpJustificationCode = set(tableElement[1]['JustificationCode'].split(";"))
            cleanUpJustificationCode.discard('nan')
            joinedJustificationCode = ';'.join(str(element) for element in cleanUpJustificationCode)
            justificationExplanationList[joinedJustificationCode] = joinedJustification
            outcomeCode = tableElement[0][0]
            sfiaLevel = tableElement[0][1]
            sfiaSkillName = sfia[outcomeCode][sfiaLevel]['Skill']
            sfiaSkillDescription = sfia[outcomeCode][sfiaLevel]['Description']
            sfiaLevelDescription = sfia[outcomeCode][sfiaLevel]['Description22']
            value[(outcomeCode, sfiaLevel)] = [tableElement[1]['Unit Code'], joinedJustificationCode, sfiaSkillName, sfiaSkillDescription, sfiaLevelDescription]
        if len(value) > 0:
            professionalRoleForSkill = ' + '.join(criterionBItems[courseName].roles)
            criterionBList[f"{courseName}"] = [value, professionalRoleForSkill]
    return [criterionBList, justificationExplanationList]

    #Criterion D 
def populateCriterionDDictionary(criterionDItems):
    criterionDList = {}
    for course, criterionD in criterionDItems:
        if hasattr(criterionD, 'criterion_df'):
            # Ensure all necessary columns are present
            required_columns = ['Unit Code', 'Unit Title', 'Assessment Item (for D: Advanced Algorithms and C: CBoK mapping)', 'Complex Computing Criteria met']
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
    doc.packages.append(Package('lscape'))
    doc.preamble.append(NoEscape(r'\usepackage[table]{xcolor}'))
    
    # check for parameter dictionary, create table list, and add table name to the list
    if(generateCriterionDictionary["generateCriterionA"]):
        criterionAList = populateCriterionADictionary(kb.criterionA.items())
        criterionAFileNameList = createCriterionATable(criterionAList)
    
    if(generateCriterionDictionary["generateCriterionB"]):
        criterionBList, justificationExplanationList = populateCriterionBDictionary(kb.criterionB, sfia)
        criterionBFileNameList = createCriterionBTable(criterionBList)
        justificationExplanationTable = createCriterionBJustificationTable(justificationExplanationList)

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
                criterionASection.append(NoEscape(r'\input{%s}' %nameList))
            doc.append(criterionASection)
        
        doc.append(NoEscape(r'\newpage'))

        if(generateCriterionDictionary["generateCriterionB"]):
            ## Add section for criterion B
            doc.append(NoEscape(r'\begin{landscape}'))
            criterionBSection = Section("Criterion B: Professional ICT Role and Skills")
            for nameList in criterionBFileNameList:
                criterionBSection.append(NoEscape(r'\input{%s}' %nameList))
            doc.append(criterionBSection)
            doc.append(NoEscape(r'\end{landscape}'))
            ## add justification table description table
            doc.append(NoEscape(r'\input{criterionB-justification_explanation}'))

        doc.append(NoEscape(r'\newpage'))

        if(generateCriterionDictionary["generateCriterionC"]):
            ## Add section for criterion C
            criterionCSection = Section("Criterion C: Program Design")
            criterionCSection.append("Mapping of Units to the Australian Computer Society’s Core Body of Knowledge (CBoK)\n")
            # criterionCSection.append("Lorem Ipsum 2\n")
            for nameList in criterionCFileNameList:
                criterionCSection.append(NoEscape(r'\input{%s}' %nameList))
            doc.append(criterionCSection)

        doc.append(NoEscape(r'\newpage'))

        ## Add section for criterion D
        if(generateCriterionDictionary["generateCriterionD"]):
            criterionDSection = Section("Criterion D: Advanced ICT Units Addressing Complex Computing")
            for nameList in criterionDFileNameList:
                criterionDSection.append(NoEscape(r'\input{%s}' %nameList)),
            doc.append(criterionDSection)

        doc.append(NoEscape(r'\newpage'))

        ## Add section for criterion E
        if(generateCriterionDictionary["generateCriterionE"]):
            criterionESection = Section("Criterion E: Integrated and Applied ICT Knowledge")
            for nameList in criterionEFileNameList:
                criterionESection.append(NoEscape(r'\input{%s}' %nameList)),    
            doc.append(criterionESection)    

    # Sort by program
    elif(sortBy == 'program'):
        courseDictionary = {}

        for fileName in criterionAFileNameList:
            if(fileName.replace(".tex", "").replace("criterionA-", "") not in courseDictionary):
                courseDictionary[fileName.replace(".tex", "").replace("criterionA-", "")] = [fileName]
            else:
                tempList = courseDictionary[fileName.replace(".tex", "").replace("criterionA-", "")]
                tempList.append(fileName)
                courseDictionary[fileName.replace(".tex", "").replace("criterionA-", "")] = tempList

        for fileName in criterionBFileNameList:
            if(fileName.replace(".tex", "").replace("criterionB-", "") not in courseDictionary):
                courseDictionary[fileName.replace(".tex", "").replace("criterionB-", "")] = [fileName]
            else:
                tempList = courseDictionary[fileName.replace(".tex", "").replace("criterionB-", "")]
                tempList.append(fileName)
                courseDictionary[fileName.replace(".tex", "").replace("criterionB-", "")] = tempList

        for fileName in criterionCFileNameList:
            if(fileName.replace(".tex", "").replace("criterionC-", "") not in courseDictionary):
                courseDictionary[fileName.replace(".tex", "").replace("criterionC-", "")] = [fileName]
            else:
                tempList = courseDictionary[fileName.replace(".tex", "").replace("criterionC-", "")]
                tempList.append(fileName)
                courseDictionary[fileName.replace(".tex", "").replace("criterionC-", "")] = tempList
                
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
                criterionCourseSection.append(NoEscape(r'\input{%s}' %courseDictionary[course][0]))
    
            doc.append(NoEscape(r'\newpage'))
    
            if(generateCriterionDictionary["generateCriterionB"]):
                criterionCourseSection.append(NoEscape(r'\begin{landscape}'))
                criterionCourseSection.append("Criterion B: Professional ICT Role and Skills\n")
                criterionCourseSection.append(NoEscape(r'\input{%s}' %courseDictionary[course][1]))
                criterionCourseSection.append(NoEscape(r'\end{landscape}'))
    
            doc.append(NoEscape(r'\newpage'))
 
            if(generateCriterionDictionary["generateCriterionC"]):
                criterionCourseSection.append("Criterion C: Program Design\n")
                criterionCourseSection.append("Mapping of Units to the Australian Computer Society’s Core Body of Knowledge (CBoK)\n")
                criterionCourseSection.append(NoEscape(r'\input{%s}' %courseDictionary[course][2]))
    
            doc.append(NoEscape(r'\newpage'))
 
            if(generateCriterionDictionary["generateCriterionD"]):
                criterionCourseSection.append("Criterion D: Program Design\n")
                criterionCourseSection.append(NoEscape(r'\input{%s}' %courseDictionary[course][3]))
    
            doc.append(NoEscape(r'\newpage'))
 
            if(generateCriterionDictionary["generateCriterionE"]):
                criterionCourseSection.append("Criterion E: Program Design\n")
                criterionCourseSection.append(NoEscape(r'\input{%s}' %courseDictionary[course][4]))

            doc.append(criterionCourseSection)   
        doc.append(NoEscape(r'\input{criterionB-justification_explanation}'))


    doc.generate_tex(f"main-{sortBy}")

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