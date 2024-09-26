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
    # criterionASubSubSection.append('Bachelor of Science (Computer Science)\\n')
    # criterionASubSubSection.append(NoEscape(r'\\begin{adjustbox}{max width=1\\textwidth}'))
    
    # criterionATable = Tabular(table_spec="|l|l|l|l|l|l|l|l|l|l|l|l|l|l|l|l|l|l|l|l|")
    # criterionATable.add_hline()
    # criterionATable.add_row((MultiColumn(20, align="|l|", data=NoEscape(r'\\headerstyle \\textbf{Program Details}')),))
    # criterionATable.add_row((MultiColumn(20, align="|l|", data=""),))
    # criterionATable.add_hline()
    # criterionATable.add_row((MultiColumn(9, align="|l|", data="Code"), MultiColumn(11, align="|l|", data="MJD-CMPSC")))
    # criterionATable.add_hline()
    # criterionATable.add_row((MultiColumn(9, align="|l|", data="Award title on Transcript/Testamur"), MultiColumn(11, align="|l|", data="Bachelor of Science (Computer Science)")))
    # criterionATable.add_hline()
    # criterionATable.add_row((MultiColumn(9, align="|l|", data="EFT Years of Study"), MultiColumn(11, align="|l|", data="3 Years")))
    # criterionATable.add_hline()
    # criterionATable.add_row((MultiColumn(9, align="|l|", data="First Year of Offer"), MultiColumn(11, align="|l|", data="2012")))
    # criterionATable.add_hline()
    # criterionATable.add_row((MultiColumn(20, align="|l|", data=MultiRow(2, data=NoEscape(r'\\headerstyle \\textbf{Personnel}'))),))
    # criterionATable.add_row((MultiColumn(20, align="|l|", data=""),))
    # criterionATable.add_hline()
    # criterionATable.add_row((MultiColumn(9, align="|l|", data="Program Chair"), MultiColumn(11, align="|l|", data="Dr Chris McDonald")))
    # criterionATable.add_row((MultiColumn(1, align="|l|", data=""),MultiColumn(3, align="|l|", data="Code"),MultiColumn(8, align="|l|", data="Title"),MultiColumn(6, align="|l|", data="Unit Coordinator(s)"),MultiColumn(2, align="|l|", data="File #"),))
    # criterionATable.add_hline()
    # criterionASubSubSection.append(criterionATable)
    # criterionASubSubSection.append(NoEscape(r'\end{adjustbox}'))
    # return criterionASubSubSection
     ### Start loop for each program
    criterionASubSubSection.append('Program Name\n')
    criterionASubSubSection.append(NoEscape(r'\begin{adjustbox}{max width=\textwidth}'))
    criterionATable = Tabular(table_spec="|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|")
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(20, align="|l|", data=MultiRow(2, data="Program Details")),))
    criterionATable.add_row((MultiColumn(20, align="|l|", data=""),))
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(9, align="|l|", data="Code"), (MultiColumn(11, align="|l|", data="code-name"))))
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(9, align="|l|", data="Award title on Transcript/Testamur"), (MultiColumn(11, align="|l|", data="award-name"))))
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(9, align="|l|", data="EFT Years of Study"), (MultiColumn(11, align="|l|", data="study-duration"))))
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(9, align="|l|", data="First Year of Offer"), (MultiColumn(11, align="|l|", data="year-name"))))
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(20, align="|l|", data=MultiRow(2, data="Personnel")),))
    criterionATable.add_row((MultiColumn(20, align="|l|", data=""),))
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(9, align="|l|", data="Program Chair"), (MultiColumn(11, align="|l|", data="chair-name"))))
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(9, align="|l|", data="ICT Industry Liaison"), (MultiColumn(11, align="|l|", data="liaison-name"))))
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(9, align="|l|", data="Key Academic Staff"), (MultiColumn(11, align="|l|", data="[list-of-staff-name]"))))
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(20, align="|l|", data=MultiRow(2, data="Outcomes")),))
    criterionATable.add_row((MultiColumn(20, align="|l|", data=""),))
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(20, align="|l|", data="Lorem Ipsum"),))
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(8, align="|l", data=MultiRow(2, data="Unit Sequence")), MultiColumn(12, align="l|", data=MultiRow(2, data="Key: *advanced units (Criterion D) and ^integrated and applied units (Criterion E)"))))
    criterionATable.add_row((MultiColumn(20, align="|l|", data=""),))
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(1, align="|l|", data=""),MultiColumn(3, align="|l|", data="Code"),MultiColumn(8, align="|l|", data="Title"),MultiColumn(6, align="|l|", data="Unit Coordinator(s)"),MultiColumn(2, align="|l|", data="File #"),))
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
        criterionBTable.add_row("","","","","","", color=r'colorDarkBlue')
        criterionBTable.add_row("","","","","","", color=r'colorDarkBlue')
        criterionBTable.add_row(MultiRow(NoEscape(-3), data=NoEscape(r'\textit{SFIA Skill}')), 
                        MultiRow(NoEscape(-3), data=NoEscape(r'\textit{Skill Description}')), 
                        MultiRow(NoEscape(-3), data=NoEscape(r'\textit{Level Description}')), 
                        MultiRow(NoEscape(-3), data=NoEscape(r'\textit{Code}')), 
                        MultiRow(NoEscape(-3), data=NoEscape(r'\textit{Level}')), 
                        MultiRow(NoEscape(-3), data=NoEscape(r'\textit{Units supporting SFIA skill}')), color=r'colorDarkBlue')

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
        criterionBSubSubSection.append(NoEscape(r'\rubric{Criterion B Rubric}'))
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
                
                # Skip this row if all fields are empty
                if not (unit_code or unit_name or assessment_item or justification):
                    continue
                
                unit_code_and_name = f"{unit_code} {unit_name}".strip()
                
                # Escape special LaTeX characters
                justification = justification.replace('&', r'\&').replace('%', r'\%').replace('#', r'\#').replace('_', r'\_')
                assessment_item = assessment_item.replace('&', r'\&').replace('%', r'\%').replace('#', r'\#').replace('_', r'\_')
                
                table_content.append((unit_code_and_name, assessment_item, justification))

            # Only create the table if there's content
            if table_content:
                # Add program title
                criterionDSubSubSection.append(NoEscape(r'\noindent\textbf{' + course + r'}'))
                criterionDSubSubSection.append(NewLine())

                # Start longtable
                criterionDSubSubSection.append(NoEscape(r'\begin{longtable}{|p{0.2\textwidth}|p{0.3\textwidth}|p{0.45\textwidth}|}'))
                
                # Table header1
                criterionDSubSubSection.append(NoEscape(r'\hline'))
                criterionDSubSubSection.append(NoEscape(r'\multicolumn{3}{|l|}{\cellcolor{colorDarkBlue} \textbf{Criterion D: Advanced ICT Units Addressing Complex Computing}} \\'))
                criterionDSubSubSection.append(NoEscape(r'\hline'))
                criterionDSubSubSection.append(NoEscape(r'\cellcolor{colorLightBlue} \textit{Unit Code \& Title} & \cellcolor{colorLightBlue} \textit{Assessment Item} & \cellcolor{colorLightBlue} \textit{Complex Computing Criteria met} \\'))
                criterionDSubSubSection.append(NoEscape(r'\hline'))
                criterionDSubSubSection.append(NoEscape(r'\endfirsthead'))


                # Add table content
                for row in table_content:
                    criterionDSubSubSection.append(NoEscape(
                        row[0] + r' & ' + row[1] + r' & ' + row[2] + r' \\'
                    ))
                    criterionDSubSubSection.append(NoEscape(r'\hline'))

                criterionDSubSubSection.append(NoEscape(r'\end{longtable}'))
                criterionDSubSubSection.append(NoEscape(r'\rubric{Criterion D Rubric}'))
                
                # Add some vertical space between tables
                criterionDSubSubSection.append(NoEscape(r'\vspace{1em}'))

    criterionDSubSubSection.generate_tex("criterionD")

# Table 5. Criterion E
def createCriterionETable(dataDictionary):
    criterionESubSubSection = Subsubsection("Criterion E: Integrated and Applied ICT Knowledge")
    
    for course, courseData in dataDictionary.items():
        if courseData:  # Only process courses with data
            # Add the course title
            criterionESubSubSection.append(NoEscape(r'\\noindent\\textbf{' + course + r'}\\\\[0.5em]'))
            
            # Start the tabular environment directly (no table float)
            criterionESubSubSection.append(NoEscape(r'\\noindent\\begin{tabular}{|p{0.20\\textwidth}|p{0.77\\textwidth}|}'))
            criterionESubSubSection.append(NoEscape(r'\\hline'))
            criterionESubSubSection.append(NoEscape(r'\\multicolumn{2}{|l|}{\\headerstyle \\textbf{Criterion E: Integrated and Applied ICT Knowledge}} \\\\'))
            criterionESubSubSection.append(NoEscape(r'\\hline'))
            criterionESubSubSection.append(NoEscape(r'\\subheaderstyle \\textit{Unit Code \\& Title} & \\subheaderstyle \\textit{Notes in support of Claim} \\\\'))
            criterionESubSubSection.append(NoEscape(r'\\hline'))
            
            for row in courseData:
                unit_code = row.get('Unit Code', '')
                unit_name = row.get('Unit Name', '')
                justification = row.get('Justification', '')
                
                # Combine Unit Code and Unit Name
                unit_code_and_name = f"{unit_code} {unit_name}"
                
                # Ensure proper text wrapping for all columns
                wrapped_unit_code_and_name = NoEscape(r'\\parbox[t]{0.20\\textwidth}{' + unit_code_and_name + '}')
                wrapped_justification = NoEscape(r'\\parbox[t]{0.77\\textwidth}{' + justification + '}')
                
                criterionESubSubSection.append(NoEscape(f"{wrapped_unit_code_and_name} & {wrapped_justification} \\\\\\\\"))
                criterionESubSubSection.append(NoEscape(r'\\hline'))

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
        criterionBList[f"{courseName}"] = value
    return criterionBList

def populateCriterionDDictionary(criterionDItems):
    criterionDList = {}
    #Criterion D 
    for course, criterionD in criterionDItems:
        if hasattr(criterionD, 'criterion_df'):
            # Ensure all necessary columns are present
            required_columns = ['Unit Code', 'Unit Title', 'Assessment Item (for D: Advanced Algorithms and C: CBoK mapping)', 'Complex Computing Criteria met']
            for col in required_columns:
                if col not in criterionD.criterion_df.columns:
                    criterionD.criterion_df[col] = ''
            criterionDList[course] = criterionD
    return criterionDList

def populateCriterionEDictionary(criterionEItems):
    criterionEList = {}
    #Criterion E
    for course, criterionE in criterionEItems:
        if criterionE.criterion_df is not None and not criterionE.criterion_df.empty:
            # Ensure 'Justification' column exists, if not, add an empty one
            if 'Justification' not in criterionE.criterion_df.columns:
                criterionE.criterion_df['Justification'] = ''
            criterionEList[course] = criterionE.criterion_df.to_dict('records')
        else:
            criterionEList[course] = []
    return criterionEList

# main function
def generateLatex():
    sfia = SFIA('sfia_v8_custom.xlsx')
    kb = KnowledgeBase('CSSE-allprograms-outcome-mappings-20240913.xlsx', sfia)
    #sort by criterion
    criterionBList = populateCriterionBDictionary(kb.criterionB.items(), sfia)
    criterionDList = populateCriterionDDictionary(kb.criterionD.items())
    criterionEList = populateCriterionEDictionary(kb.criterionE.items())
    
    #sort by course

    geometry_options = {"tmargin": "0.5in", "lmargin": "0.5in", "bmargin": "0.5in", "rmargin": "0.5in"}
    doc = Document(documentclass="report",geometry_options=geometry_options)
    doc.packages.append(Package('multirow'))
    doc.packages.append(Package('makecell'))
    doc.packages.append(Package('rotating'))
    doc.packages.append(Package('adjustbox'))
    doc.packages.append(Package('latexStyleSheet'))
    doc.packages.append(Package('longtable'))
    doc.preamble.append(NoEscape(r'\newcommand{\myrotcell}[1]{\rotcell{\makebox[0pt][l]{#1}}}'))
    doc.preamble.append(NoEscape(r'\usepackage[table]{xcolor}'))
    doc.preamble.append(NoEscape(r'\newcommand{\rubric}[1]{{\color{red}#1}}'))
    doc.preamble.append(NoEscape(r'%\newcommand{\rubric}[1]{}'))

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
    programSpecificationAndImplementationICTSection.append(createCriterionETable(criterionEList))
    # createCriterionETable(criterionEList)
    # programSpecICTSubsection.append(NoEscape(r'\include{criterionE}'))

    # Add section to the document
    doc.append(programSpecificationAndImplementationICTSection)
    doc.generate_tex("main")

def main():
    generateLatex()

if __name__ == "__main__":
    main()