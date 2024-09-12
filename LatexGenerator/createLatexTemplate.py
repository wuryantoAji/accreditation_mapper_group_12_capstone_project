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
    criterionASubSubSection.append('Bachelor of Science (Computer Science)\n')
    criterionASubSubSection.append(NoEscape(r'\begin{adjustbox}{max width=1\textwidth}'))
    criterionATable = Tabular(table_spec="|l|l|l|l|l|l|l|l|l|l|l|l|l|l|l|l|l|l|l|l|")
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(20, align="|l|", data=MultiRow(2, data="Program Details")),))
    criterionATable.add_row((MultiColumn(20, align="|l|", data=""),))
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(9, align="|l|", data="Code"), (MultiColumn(11, align="|l|", data="MJD-CMPSC"))))
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(9, align="|l|", data="Award title on Transcript/Testamur"), (MultiColumn(11, align="|l|", data="Bachelor of Science (Computer Science)"))))
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(9, align="|l|", data="EFT Years of Study"), (MultiColumn(11, align="|l|", data="3 Years"))))
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(9, align="|l|", data="First Year of Offer"), (MultiColumn(11, align="|l|", data="2012"))))
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(20, align="|l|", data=MultiRow(2, data="Personnel")),))
    criterionATable.add_row((MultiColumn(20, align="|l|", data=""),))
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(9, align="|l|", data="Program Chair"), (MultiColumn(11, align="|l|", data="Dr Chris McDonald"))))
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(9, align="|l|", data="ICT Industry Liaison"), (MultiColumn(11, align="|l|", data="Christopher Kings-Lynne"))))
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(9, align="|l|", data="Key Academic Staff"), (MultiColumn(11, align="|l|", data="Amitava Datta, Lyndon While, Chris McDonald, Rachel Cardell-Oliver"))))
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(20, align="|l|", data=MultiRow(2, data="Outcomes")),))
    criterionATable.add_row((MultiColumn(20, align="|l|", data=""),))
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(20, align="|l|", data=NoEscape(r'\makecell[tl]{Students are able to: \\ 1. develop and implement systems level software in the procedural language C; \\ 2. understand software engineering principles of problem decomposition, and design and implement solutions in the \\ object oriented language Java; \\ 3. understand the role played by databases for persistent storage in networked systems; \\ 4. design appropriate schemas for storing information in databases, and access, sort and join data using query languages; \\ 5. understand the mechanics of, and be able to implement, the primary data structures and associated algorithms that \\ underly computer solutions; \\ 6. understand the computational complexity and correctness of algorithms and operations on data structures, and use \\ this knowledge to be able to choose algorithms and structures appropriate to the task; \\ 7. understand how algorithms can be extended with heuristics to solve problems, the issues of algorithms interacting \\ autonomously with the environment, and the complexity and correctness of those algorithms; \\ 8. understand how those algorithms form the basis of search, problem solving, learning and decision-making in intelligent \\ agents, and be able to implement examples of those agents; \\ 9. understand the interconnected components that comprise computing systems and networks, the principles and \\ standards through which they interact, and alternative algorithms and their trade-offs for controlling the interactions; \\ 10. understand the technologies that allow humans and computers to interact through the medium of visual data, \\ including graphics and animation that underpin the computer games and multimedia industries; \\ 11. work in teams to carry out projects in a professional setting for an industry or third party client, including requirements \\ analysis, design, implementation, testing and documentation; \\ 12. appreciate the ethical responsibilities of professional practice in computing; \\ 13. communicate effectively in various media, including writing and oral presentations; and \\ 14. demonstrate basic research skills that can be applied in higher level studies.}')),))
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(8, align="|l", data=MultiRow(2, data="Unit Sequence")), MultiColumn(12, align="l|", data=MultiRow(2, data="Key: *advanced units (Criterion D) and ^integrated and applied units (Criterion E)"))))
    criterionATable.add_row((MultiColumn(20, align="|l|", data=""),))
    criterionATable.add_hline()
    criterionATable.add_row((MultiColumn(1, align="|l|", data=""),MultiColumn(3, align="|l|", data="Code"),MultiColumn(8, align="|l|", data="Title"),MultiColumn(6, align="|l|", data="Unit Coordinator(s)"),MultiColumn(2, align="|l|", data="File #"),))
    criterionATable.add_hline()
    ## Loop for row content
    ### Each level/Core/Optional List
    criterionATable.add_row(MultiColumn(1, align="|c|", data=MultiRow(6, data=NoEscape(r'\myrotcell{Level 1}'))), MultiColumn(19, align="|l|", data="Take all core units (12 points);"))
    #### Unit lists for those level/core/optional
    criterionATable.add_hline(2,20)
    criterionATable.add_row(MultiColumn(1, align="|l|", data=""), MultiColumn(3, align="|l|", data="CITS1001"), MultiColumn(8, align="|l|", data="Software Engineering with Java (Sem-1, Sem-2)"), MultiColumn(6, align="|l|", data=NoEscape(r'\makecell[tl]{Lyndon While (S1)\\Ajmal Mian (S2)}')),MultiColumn(2, 
    align="|c|", data="01"))
    criterionATable.add_hline(2,20)
    criterionATable.add_row(MultiColumn(1, align="|l|", data=""), MultiColumn(3, align="|l|", data="CITS1402"), MultiColumn(8, align="|l|", data="Relational Database Management Systems (Sem-2)"), MultiColumn(6, align="|l|", data=NoEscape(r'\makecell[tl]{Gordon Royle}')),MultiColumn(2, align="|c|", data="04"))
    criterionATable.add_hline(2,20)
    criterionATable.add_row(MultiColumn(1, align="|l|", data=""), MultiColumn(19, align="|l|", data="Take complementary unit (6 points):"))
    criterionATable.add_row(MultiColumn(1, align="|l|", data=""), MultiColumn(19, align="|l|", data="Not required for students who have Maths Methods ATAR or equivalent or higher."))
    criterionATable.add_hline(2,20)
    criterionATable.add_row(MultiColumn(1, align="|l|", data=""), MultiColumn(3, align="|l|", data="MATH1721"), MultiColumn(8, align="|l|", data="Mathematics Foundations: Methods (Sem-1, Sem-2)"), MultiColumn(6, align="|l|", data=NoEscape(r'\makecell[tl]{Nazim Khan}')),MultiColumn(2, align="|c|", data="70"))
    criterionATable.add_hline()
    criterionASubSubSection.append(criterionATable)
    criterionASubSubSection.append(NoEscape(r'\end{adjustbox}'))
    return criterionASubSubSection

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
            levelDescription = dataDictionary[key][sfiaComponent][4]
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
        criterionBSubSubSection.append(NewLine())
        criterionBSubSubSection.append(NewLine())
    return criterionBSubSubSection

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
    return criterionCSubSubSection


# Table 4. Criterion D
def createCriterionDTable(programName, listOfCourse):
    ## Add subsub section for criterion D
    criterionDSubSubSection = Subsubsection("Criterion D: Program Design")
    ### Start loop for each program
    criterionDSubSubSection.append('Bachelor of Science (Computer Science)\n')
    criterionDSubSubSection.append(NoEscape(r'\begin{adjustbox}{max width=1\textwidth}'))
    criterionDTable = Tabular(table_spec="|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|")
    criterionDTable.add_hline()
    criterionDTable.add_row((MultiColumn(20, align="|l|", data=MultiRow(2, data="Criterion D: Advanced ICT Units Addressing Complex Computing")),))
    criterionDTable.add_row((MultiColumn(20, align="|l|", data=""),))
    criterionDTable.add_hline()
    criterionDTable.add_row((MultiColumn(6, align="|l|", data="SFIA Skill Code"), (MultiColumn(7, align="|l|", data="Problem Solving")), (MultiColumn(7, align="|l|", data="ICT Professional Knowledge"))))
    criterionDTable.add_hline()
    criterionDTable.add_row((MultiColumn(6, align="|l|", data=NoEscape(r'\makecell[tl]{CITS3001 Algorithms, \\ Agents and Artificial \\ Intelligence}')), (MultiColumn(7, align="|l|", data=NoEscape(r'\makecell[tl]{Group Project (Research, \\ implement and validate game \\ playing AI)}'))), (MultiColumn(7, align="|l|", data=NoEscape(r'\makecell[tl]{Requires students to research (2, 3) and implement \\ novel solutions (5, 9), and validate the solution (4, 8)}')))))
    criterionDTable.add_hline()
    criterionDTable.add_row((MultiColumn(6, align="|l|", data="CITS3002 Computer Networks"), (MultiColumn(7, align="|l|", data="Networked communication within a transportation network to solve a scheduling problem")), (MultiColumn(7, align="|l|", data="Has no obvious solution, and requires conceptual thinking and innovative analysis to formulate suitable abstract models (SA2), and is a high-level problem possibly including many component parts or sub-problems (SA8)."))))
    criterionDTable.add_hline()
    criterionDSubSubSection.append(criterionDTable)
    criterionDSubSubSection.append(NoEscape(r'\end{adjustbox}'))
    return criterionDSubSubSection

# Table 5. Criterion E
def createCriterionETable(programName, listOfCourse):
    ## Add subsub section for criterion E
    criterionESubSubSection = Subsubsection("Criterion E: Program Design")
    ### Start loop for each program
    criterionESubSubSection.append('Bachelor of Science (Computer Science)\n')
    criterionESubSubSection.append(NoEscape(r'\begin{adjustbox}{max width=\textwidth}'))
    criterionETable = Tabular(table_spec="|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|")
    criterionETable.add_hline()
    criterionETable.add_row((MultiColumn(20, align="|l|", data=MultiRow(2, data="Criterion E: Integrated and Applied ICT Knowledge")),))
    criterionETable.add_row((MultiColumn(20, align="|l|", data=""),))
    criterionETable.add_hline()
    criterionETable.add_row((MultiColumn(9, align="|l|", data="Unit Code & Title"), (MultiColumn(11, align="|l|", data="Notes in support of Claim"))))
    criterionETable.add_hline()
    criterionETable.add_row((MultiColumn(9, align="|l|", data="CITS3200 Professional Computing "), (MultiColumn(11, align="|l|", data=NoEscape(r'\makecell[tl]{Capstone team project with a real industry client and software professional mentor. \\ Assessed on delivered project quality and a professional portfolio}')))))
    criterionETable.add_hline()
    criterionESubSubSection.append(criterionETable)
    criterionESubSubSection.append(NoEscape(r'\end{adjustbox}'))
    return criterionESubSubSection

def createCriterionFTable(programName, listOfCourse):
    ## Add subsub section for criterion F
    criterionFSubSubSection = Subsubsection("Criterion F: Program Design")
    criterionFSubSubSection.append("Lorem Ipsum 3")    
    return criterionFSubSubSection

# main function
def generateLatex():
    sfia = SFIA('sfiaskills.6.3.en.1.xlsx')
    kb = KnowledgeBase('CSSE-allprograms-outcome-mappings-20240821.xlsx', sfia)
    criterionBList = {}
    # debugSet = []
    for course, criterionB in kb.criterionB.items():
        courseName = course
        value = {}
        for x in criterionB.criterion_df.groupby(['Outcome','Level (SFIA/Bloom)']).agg(lambda x: ';'.join(x.astype(str)) if not x.empty else '').iterrows():
            cleanUpJustification = set(x[1]['Justification'].split(";"))
            cleanUpJustification.discard('nan')
            joinedJustification = ';'.join(str(element) for element in cleanUpJustification)
            outcomeCode = x[0][0]
            sfiaLevel = x[0][1]
            # TODO don't forget to delete this if
            if(outcomeCode != 'HPCC'):
                sfiaSkillName = sfia[outcomeCode][sfiaLevel]['Skill']
                sfiaSkillDescription = sfia[outcomeCode][sfiaLevel]['Description']
                sfiaLevelDescription = sfia[outcomeCode][sfiaLevel]['Description22']
                value[(outcomeCode, sfiaLevel)] = [x[1]['Unit Code'], joinedJustification, sfiaSkillName, sfiaSkillDescription, sfiaLevelDescription]
        criterionBList[f"{courseName}"] = value        

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
    doc.preamble.append(NoEscape(r'\definecolor{header3}{RGB}{211,211,211}'))

    # Add Section for ICT Program Specification and Implementation
    programSpecificationAndImplementationICTSection = Section("ICT Program Specification and Implementation")
    ## Add subsection for ICT Program Specification
    programSpecICTSubsection = Subsection("ICT Program Specification")
    programSpecICTSubsection.append("Lorem Ipsum")
    # Add all subsub section part to sub section
    programSpecICTSubsection.append(createCriterionATable("MIT",["CITS4401"]))
    programSpecICTSubsection.append(createCriterionBTable(criterionBList))
    programSpecICTSubsection.append(createCriterionCTable("MIT",["CITS4401"]))
    programSpecICTSubsection.append(createCriterionDTable("MIT",["CITS4401"]))
    programSpecICTSubsection.append(createCriterionETable("MIT",["CITS4401"]))
    programSpecICTSubsection.append(createCriterionFTable("MIT",["CITS4401"]))

    # Add sub section part to section
    programSpecificationAndImplementationICTSection.append(programSpecICTSubsection)

    # Add section to the document
    doc.append(programSpecificationAndImplementationICTSection)
    doc.generate_tex("criterionAtoFTable")

def main():
    generateLatex()

if __name__ == "__main__":
    main()