from pylatex import Package, NoEscape, Section, Subsection, Subsubsection, Tabular, MultiColumn, MultiRow, Document, NewLine
from sfia import SFIA
from knowledgebase import KnowledgeBase

placeholderConstant = 'Placeholder'

# Utility function
def putNewLine(longString):
    words = longString.split()

    # Initialize an empty list to store the result
    result = []

    # Iterate over the words in chunks of 6
    for i in range(0, len(words), 6):
        # Add the next 6 words to the result
        result.extend(words[i:i + 6])
        # Add a backslash after every 6 words, except after the last group
        if i + 6 < len(words):
            result.append('\\\\')

    # Join the result list back into a single string with spaces
    return ' '.join(result)

# Transform a list of course into tables

# Table 1. Criterion A
def createCriterionATable(programName, listOfCourse):
    ## Add subsub section for criterion A
    criterionASubSubSection = Subsubsection("Criterion A: Program Design")
    
    ### Start loop for each program
    criterionASubSubSection.append('Program Name\n')
    criterionASubSubSection.append(NoEscape(r'\begin{adjustbox}{max width=\textwidth}'))
    criterionATable = Tabular(table_spec="|p{\criterionAEmptyCol}|p{\criterionACodeCol}|p{\criterionATitleCol}|p{\criterionACoordinatorCol}|p{\criterionAFileCol}|")
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
    criterionASubSubSection.append(NoEscape(r'\rubric{Criterion A Rubric}'))
    criterionASubSubSection.generate_tex("criterionA")

# Table 2. Criterion B
def createCriterionBTable(dataDictionary):
    ## Add subsub section for criterion B
    criterionBSubSubSection = Subsubsection("Criterion B: Professional ICT Role and Skills")
    ### Start loop for each program
    for key in dataDictionary:
        criterionBSubSubSection.append(f"{key}\n")
        criterionBSubSubSection.append(f"ICT professional role: {placeholderConstant}\n")
        sfiaSkills = ""
        for sfiaComponent in dataDictionary[key].keys():
            sfiaSkills = sfiaSkills+"+"+sfiaComponent[0]
        criterionBSubSubSection.append(f"SFIA skills: {sfiaSkills[1:]}\n")
        criterionBSubSubSection.append(NoEscape(r'\begin{adjustbox}{max width=1\textwidth}'))
        criterionBTable = Tabular(table_spec=NoEscape(r'|p{0.2\textwidth}|p{0.3\textwidth}|p{0.3\textwidth}|p{0.1\textwidth}|p{0.1\textwidth}|p{0.3\textwidth}|'))
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
        # table content
        for sfiaComponent in dataDictionary[key].keys():
            sfiaCode = sfiaComponent[0]
            sfiaLevel = sfiaComponent[1]
            unitList = dataDictionary[key][sfiaComponent][0]
            unitsSupportingSFIASkill = dataDictionary[key][sfiaComponent][1]
            sfiaSkill = dataDictionary[key][sfiaComponent][2]
            skillDescription = dataDictionary[key][sfiaComponent][3]
            levelDescription = dataDictionary[key][sfiaComponent][4].replace('_x000D_', '\n')
            criterionBTable.add_row(NoEscape(r'{%s}' % sfiaSkill),
                        NoEscape(r'{%s}' %skillDescription), 
                        NoEscape(r'{%s}' %levelDescription), 
                        f"{sfiaCode}", 
                        f"{sfiaLevel}", 
                        NoEscape(r'{%s}' %unitsSupportingSFIASkill))
            criterionBTable.add_hline()
        criterionBSubSubSection.append(criterionBTable)
        criterionBSubSubSection.append(NoEscape(r'\end{adjustbox}'))
        criterionBSubSubSection.append(NewLine())
        criterionBSubSubSection.append(NoEscape(r'\rubric{Criterion B Rubric || SFIA Code ( ) || SFIA Level ( ) || Unit Supporting SFIA Skill ( ) || SFIA Skill ( ) || Skill Description ( ) || Level Description ( )}'))
        criterionBSubSubSection.append(NewLine())
        criterionBSubSubSection.append(NewLine())
    criterionBSubSubSection.generate_tex("criterionB")

# Table 3. Criterion C
def createCriterionCTable(programName, listOfCourse):
    criterionCSubSubSection = Subsubsection("Criterion C: Program Design")
    criterionCSubSubSection.append("Mapping of Units to the Australian Computer Society’s Core Body of Knowledge (CBoK)\n")
    criterionCSubSubSection.append("Lorem Ipsum 2\n")
    ### Start loop for each program
    criterionCSubSubSection.append('Program Name\n')
    criterionCSubSubSection.append(NoEscape(r'\begin{adjustbox}{max width=\textwidth}'))
    criterionCTable = Tabular(table_spec="|l|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|")
    criterionCTable.add_hline()
    criterionCTable.add_row(
        ("CBoK Knowledge Areas", (MultiColumn(8, align="|c|", data="ESSENTIAL CORE ICT KNOWLEDGE")),(MultiColumn(11, align="|c|", data="GENERAL ICT KNOWLEDGE")))
    )
    criterionCTable.add_hline()
    criterionCTable.add_row(
        (MultiColumn(1, align="|c|", data=MultiRow(2, data="Program Name")), (MultiColumn(2, align="|c|", data=MultiRow(2, data="Problem Solving"))), (MultiColumn(6, align="|c|", data=MultiRow(2, data="ICT Professional Knowledge"))), (MultiColumn(3, align="|c|", data=MultiRow(2, data="Technology Resources"))), (MultiColumn(4, align="|c|", data=MultiRow(2, data="Technology Building"))), (MultiColumn(4, align="|c|", data=MultiRow(2, data="ICT Management"))))
    )
    criterionCTable.add_row(
        (MultiColumn(1, align="|c|", data=""), MultiColumn(2, align="|c|", data=""), MultiColumn(6, align="|c|", data=""), MultiColumn(3, align="|c|", data=""), MultiColumn(4, align="|c|", data=""), MultiColumn(4, align="|c|", data=""))
    )
    criterionCTable.add_hline(2,20)
    criterionCTable.add_row((NoEscape(r'\rule{0pt}{175pt}'),NoEscape(r'\myrotcell{Abstraction}'),NoEscape(r'\myrotcell{Design}'),NoEscape(r'\myrotcell{Ethics}'),NoEscape(r'\myrotcell{Professional expectations}'),NoEscape(r'\myrotcell{Teamwork concepts and issues}'),NoEscape(r'\myrotcell{Interpersonal communications}'),NoEscape(r'\myrotcell{Societal issues/legal issues/privacy}'),NoEscape(r'\myrotcell{Understanding the ICT profession}'),NoEscape(r'\myrotcell{Hardware \& software fundamentals}'),NoEscape(r'\myrotcell{Data \& information management}'),NoEscape(r'\myrotcell{Networking}'),NoEscape(r'\myrotcell{Programming}'),NoEscape(r'\myrotcell{Human factors}'),NoEscape(r'\myrotcell{Systems development}'),NoEscape(r'\myrotcell{Systems acquisition}'),NoEscape(r'\myrotcell{IT governance \& organisational issues}'),NoEscape(r'\myrotcell{IT project management}'),NoEscape(r'\myrotcell{Service management}'),NoEscape(r'\myrotcell{Cyber security}')))
    criterionCTable.add_hline()
    criterionCTable.add_row((MultiColumn(20, align="|l|", data="CITS1001 Software Engineering with Java (Core)"),))
    criterionCTable.add_hline()
    criterionCTable.add_row(("Lectures","X","X","","","X","","","X","X","X","","X","","X","X","","","",""))
    criterionCTable.add_hline()
    criterionCTable.add_row(("Mid-semester test","X","X","","","X","","","X","X","X","","X","","X","X","","","",""))
    criterionCTable.add_hline()
    criterionCTable.add_row(("Programming Exercises","X","X","","","X","","","X","X","X","","X","","X","X","","","",""))
    criterionCTable.add_hline()
    criterionCTable.add_row(("Exam","X","X","","","X","","","X","X","X","","X","","X","X","","","",""))
    criterionCTable.add_hline()
    criterionCSubSubSection.append(criterionCTable)
    criterionCSubSubSection.append(NoEscape(r'\end{adjustbox}'))
    criterionCSubSubSection.append(NewLine())
    criterionCSubSubSection.append(NoEscape(r'\rubric{Criterion C Rubric}'))
    criterionCSubSubSection.generate_tex("criterionC")

# Table 4. Criterion D
def createCriterionDTable(dataDictionary):
    criterionDSubSubSection = Subsubsection("Criterion D: Advanced ICT Units Addressing Complex Computing")

    for course, criterionD in dataDictionary.items():
        if criterionD and hasattr(criterionD, 'criterion_df'):
            table_content = []
            for _, row in criterionD.criterion_df.iterrows():
                unit_code = row.get('Unit Code', '').strip()
                unit_name = row.get('Unit Name', '').strip()
                assessment_item = row.get('Assessment Item (for D: Advanced Algorithms and C: CBoK mapping)', '').strip()
                justification = row.get('Justification', '').strip()
                
                if not (unit_code or unit_name or assessment_item or justification):
                    continue
                
                unit_code_and_name = f"{unit_code} {unit_name}".strip()
                
                justification = justification.replace('&', r'\&').replace('%', r'\%').replace('#', r'\#').replace('_', r'\_')
                assessment_item = assessment_item.replace('&', r'\&').replace('%', r'\%').replace('#', r'\#').replace('_', r'\_')
                
                table_content.append((unit_code_and_name, assessment_item, justification))

            if table_content:
                # Add program title using the new command
                criterionDSubSubSection.append(NoEscape(r'\criterionDcoursetitle{' + course + r'}'))
                criterionDSubSubSection.append(NewLine())

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
                criterionDSubSubSection.append(NoEscape(r'\rubric{Criterion D Rubric} \\\\'))
                
                # Add some vertical space between tables
                criterionDSubSubSection.append(NoEscape(r'\vspace{1em}'))

    criterionDSubSubSection.generate_tex("criterionD")

# Table 5. Criterion E
def createCriterionETable(dataDictionary):
    criterionESubSubSection = Subsubsection("Criterion E: Integrated and Applied ICT Knowledge")
    
    for course, courseData in dataDictionary.items():
        if courseData:  # Only process courses with data
            # Add the course title using the command
            criterionESubSubSection.append(NoEscape(r'\coursetitle{' + course + '}'))
            
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
            
            criterionESubSubSection.append(NoEscape(r'\end{tabular} \\\\'))
            criterionESubSubSection.append(NoEscape(r'\rubric{Criterion E Rubric} \\\\'))
            criterionESubSubSection.append(NoEscape(r'\\[1em]'))  # Add some space after each table
    criterionESubSubSection.generate_tex("criterionE")

# main function
def populateCriterionBDictionary(criterionBItems, sfia):
    criterionBList = {}
    
    #Criterion B
    for course, criterionB in criterionBItems:
        courseName = course
        value = {}
        for tableElement in criterionB.criterion_df.groupby(['Outcome','Level (SFIA/Bloom)']).agg(lambda x: ';'.join(x.astype(str)) if not x.empty else '').iterrows():
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
            criterionBList[f"{courseName}"] = value
    return criterionBList

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

def generateLatex():
    sfia = SFIA('sfia_v8_custom.xlsx') # TODO change this into parameter instead
    kb = KnowledgeBase('CSSE-allprograms-outcome-mappings-20240913.xlsx', sfia) # TODO change this into parameter instead
    #sort by criterion
    criterionBList = populateCriterionBDictionary(kb.criterionB.items(), sfia)
    criterionDList = populateCriterionDDictionary(kb.criterionD.items())
    criterionEList = populateCriterionEDictionary(kb.criterionE.items())
    geometry_options = {"tmargin": "0.5in", "lmargin": "0.5in", "bmargin": "0.5in", "rmargin": "0.5in"}
    doc = Document(documentclass="report",geometry_options=geometry_options)
    doc.packages.append(Package('multirow'))
    doc.packages.append(Package('makecell'))
    doc.packages.append(Package('rotating'))
    doc.packages.append(Package('adjustbox'))
    doc.packages.append(Package('latexStyleSheet'))
    doc.packages.append(Package('longtable'))
    doc.preamble.append(NoEscape(r'\usepackage[table]{xcolor}'))

    # Add Section for ICT Program Specification and Implementation
    programSpecificationAndImplementationICTSection = Section("ICT Program Specification and Implementation")
    
    # Add all subsub section part to sub section
    createCriterionATable("MIT",["CITS4401"])
    programSpecificationAndImplementationICTSection.append(NoEscape(r'\include{criterionA}'))
    createCriterionBTable(criterionBList)
    programSpecificationAndImplementationICTSection.append(NoEscape(r'\include{criterionB}'))
    createCriterionCTable("MIT",["CITS4401"])
    programSpecificationAndImplementationICTSection.append(NoEscape(r'\include{criterionC}'))
    createCriterionDTable(criterionDList)
    programSpecificationAndImplementationICTSection.append(NoEscape(r'\include{criterionD}'))
    createCriterionETable(criterionEList)
    programSpecificationAndImplementationICTSection.append(NoEscape(r'\include{criterionE}'))

    # Add section to the document
    doc.append(programSpecificationAndImplementationICTSection)
    doc.generate_tex("main")

def main():
    generateLatex()

if __name__ == "__main__":
    main()