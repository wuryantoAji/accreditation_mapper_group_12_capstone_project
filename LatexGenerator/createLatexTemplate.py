from pylatex import Package, NoEscape, Section, Subsection, Subsubsection, Tabular, MultiColumn, MultiRow, Document


# Transform a list of course into tables

# Table 1. Criterion A
def createCriterionATable(programName, listOfCourse):
    ## Add subsub section for criterion A
    criterionASubSubSection = Subsubsection("Criterion A: Program Design")
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
    return criterionASubSubSection

# Table 2. Criterion B
def createCriterionBTable(programName, listOfCourse):
    ## Add subsub section for criterion B
    criterionBSubSubSection = Subsubsection("Criterion B: Professional ICT Role and Skills")
    ### Start loop for each program
    criterionBSubSubSection.append('Program Name\n')
    criterionBSubSubSection.append(NoEscape(r'\begin{adjustbox}{max width=\textwidth}'))
    criterionBTable = Tabular(table_spec="|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|")
    criterionBTable.add_hline()
    criterionBTable.add_row(MultiColumn(9, align="|l|", data=MultiRow(2, data="B:ICT Skills for Professional Role")), (MultiColumn(11, align="|l|", data=MultiRow(2, data="Role: [lists-of-role-name]"))))
    criterionBTable.add_row(MultiColumn(9, align="|l|", data=""), (MultiColumn(11, align="|l|", data="")))
    criterionBTable.add_hline()
    criterionBTable.add_row((MultiColumn(9, align="|l|", data="SFIA Skill Code"), (MultiColumn(3, align="|c|", data="Problem Solving")), (MultiColumn(8, align="|l|", data="ICT Professional Knowledge"))))
    criterionBTable.add_hline()
    criterionBSubSubSection.append(criterionBTable)
    criterionBSubSubSection.append(NoEscape(r'\end{adjustbox}'))
    return criterionBSubSubSection

# Table 3. Criterion C
def createCriterionCTable(programName, listOfCourse):
    criterionCSubSubSection = Subsubsection("Criterion C: Program Design")
    criterionCSubSubSection.append("Mapping of Units to the Australian Computer Society’s Core Body of Knowledge (CBoK)\n")
    criterionCSubSubSection.append("Lorem Ipsum 2\n")
    ### Start loop for each program
    criterionCSubSubSection.append('Program Name\n')
    criterionCSubSubSection.append(NoEscape(r'\begin{adjustbox}{max width=\textwidth}'))
    criterionCTable = Tabular(table_spec="|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|")
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
    criterionCSubSubSection.append(criterionCTable)
    criterionCSubSubSection.append(NoEscape(r'\end{adjustbox}'))
    return criterionCSubSubSection


# Table 4. Criterion D
def createCriterionDTable(programName, listOfCourse):
    ## Add subsub section for criterion D
    criterionDSubSubSection = Subsubsection("Criterion D: Program Design")
    ### Start loop for each program
    criterionDSubSubSection.append('Program Name\n')
    criterionDSubSubSection.append(NoEscape(r'\begin{adjustbox}{max width=\textwidth}'))
    criterionDTable = Tabular(table_spec="|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|")
    criterionDTable.add_hline()
    criterionDTable.add_row((MultiColumn(20, align="|c|", data=MultiRow(2, data="Criterion D: Advanced ICT Units Addressing Complex Computing")),))
    criterionDTable.add_row((MultiColumn(20, align="|l|", data=""),))
    criterionDTable.add_hline()
    criterionDTable.add_row((MultiColumn(6, align="|l|", data="SFIA Skill Code"), (MultiColumn(7, align="|l|", data="Problem Solving")), (MultiColumn(7, align="|l|", data="ICT Professional Knowledge"))))
    criterionDTable.add_hline()
    criterionDSubSubSection.append(criterionDTable)
    criterionDSubSubSection.append(NoEscape(r'\end{adjustbox}'))
    return criterionDSubSubSection

# Table 5. Criterion E
def createCriterionETable(programName, listOfCourse):
    ## Add subsub section for criterion E
    criterionESubSubSection = Subsubsection("Criterion E: Program Design")
    ### Start loop for each program
    criterionESubSubSection.append('Program Name\n')
    criterionESubSubSection.append(NoEscape(r'\begin{adjustbox}{max width=\textwidth}'))
    criterionETable = Tabular(table_spec="|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|")
    criterionETable.add_hline()
    criterionETable.add_row((MultiColumn(20, align="|l|", data=MultiRow(2, data="Criterion E: Integrated and Applied ICT Knowledge")),))
    criterionETable.add_row((MultiColumn(20, align="|l|", data=""),))
    criterionETable.add_hline()
    criterionETable.add_row((MultiColumn(9, align="|l|", data="Unit Code & Title"), (MultiColumn(11, align="|l|", data="Notes in support of Claim"))))
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
    geometry_options = {"tmargin": "0.5in", "lmargin": "0.5in", "bmargin": "0.5in", "rmargin": "0.5in"}
    doc = Document(geometry_options=geometry_options)
    doc.packages.append(Package('multirow'))
    doc.packages.append(Package('makecell'))
    doc.packages.append(Package('rotating'))
    doc.packages.append(Package('adjustbox'))
    doc.preamble.append(NoEscape(r'\newcommand{\myrotcell}[1]{\rotcell{\makebox[0pt][l]{#1}}}'))

    # Add Section for ICT Program Specification and Implementation
    programSpecificationAndImplementationICTSection = Section("ICT Program Specification and Implementation")
    ## Add subsection for ICT Program Specification
    programSpecICTSubsection = Subsection("ICT Program Specification")
    programSpecICTSubsection.append("Lorem Ipsum")
    # Add all subsub section part to sub section
    programSpecICTSubsection.append(createCriterionATable("MIT",["CITS4401"]))
    programSpecICTSubsection.append(createCriterionBTable("MIT",["CITS4401"]))
    programSpecICTSubsection.append(createCriterionCTable("MIT",["CITS4401"]))
    programSpecICTSubsection.append(createCriterionDTable("MIT",["CITS4401"]))
    programSpecICTSubsection.append(createCriterionETable("MIT",["CITS4401"]))
    programSpecICTSubsection.append(createCriterionFTable("MIT",["CITS4401"]))

    # Add sub section part to section
    programSpecificationAndImplementationICTSection.append(programSpecICTSubsection)

    # Add section to the document
    doc.append(programSpecificationAndImplementationICTSection)
    doc.generate_tex("criterionAtoFTable")

generateLatex()