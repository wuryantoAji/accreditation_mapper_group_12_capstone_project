from sfia import SFIA
from knowledgebase import KnowledgeBase
import pandas as pd
from jinja2 import Template

# Step 1: Extract data and store it as a DataFrame

# Skills For the Information Age database
sfia = SFIA('KnowledgeBase/sfiaskills.6.3.en.1.xlsx')

# KnowledgeBase - processes the input from the client
kb = KnowledgeBase('KnowledgeBase/CSSE-allprograms-outcome-mappings-20240821.xlsx', sfia)

# 假设你的 KnowledgeBase 对象和数据处理部分已经初始化
data_frames = []

# 遍历 criterionD 数据并提取 DataFrame
for course, criterion in kb.criterionD.items():
    print(f"Processing course: {course}")
    
    df = criterion.criterion_df
    if df is not None and not df.empty:
        df['Course Title'] = course  # 为 DataFrame 添加课程标题列
        df['Unit Code & Title'] = df['Unit Code'] + ' ' + df['Unit Name']  # 合并 Unit Code 和 Unit Name
        
        # 根据句号分割 Justification 成 Complex Computing Criteria met 和 Assessment Item
        def split_justification(justification):
            if '.' in justification:
                parts = justification.split('.', 1)
                complex_computing = parts[0].strip()  # 句号前的部分
                assessment_item = parts[1].strip()  # 句号后的部分
                return complex_computing, assessment_item
            else:
                return "", justification  # 如果只有一个句子，则Complex Computing Criteria met为空，整个句子是Assessment Item
        
        df[['Complex Computing Criteria met', 'Assessment Item']] = df['Justification'].apply(
            lambda x: pd.Series(split_justification(x))
        )
        
        data_frames.append(df)

# 合并所有 DataFrame
if data_frames:
    combined_df = pd.concat(data_frames)

    # 按 Course Title 进行分组
    grouped = combined_df.groupby('Course Title')

    # Jinja2 HTML 模板
    html_template = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced ICT Units Addressing Complex Computing</title>
    <link rel="stylesheet" href="criterion.css">
</head>
<body>

    {% for course_title, units in courses.items() %}
    <h1>{{ course_title }}</h1>

    <table border="1" cellpadding="10">
        <thead>
            <tr class="title-row">
                <td colspan="3">Criterion D: Advanced ICT Units Addressing Complex Computing</td>
            </tr>
            <tr>
                <th>Unit Code & Title</th>
                <th>Assessment Item</th>
                <th>Complex Computing Criteria met</th>
            </tr>
        </thead>
        <tbody>
            {% for unit in units %}
            <tr>
                <td>{{ unit['Unit Code & Title'] }}</td>
                <td>{{ unit['Assessment Item'] }}</td>
                <td>{{ unit['Complex Computing Criteria met'] }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% endfor %}

</body>
</html>
    """

    # 数据准备：按 Course Title 分组，生成用于渲染的数据结构
    courses = {}
    for course_title, group in grouped:
        courses[course_title] = group.to_dict(orient='records')

    # 渲染 HTML 模板
    template = Template(html_template)
    html_output = template.render(courses=courses)

    # 将 HTML 写入文件
    with open("output_criterion_D.html", "w") as f:
        f.write(html_output)

    print("HTML file output_criterion_D.html generated successfully.")

else:
    print("No data found in criterionD.")