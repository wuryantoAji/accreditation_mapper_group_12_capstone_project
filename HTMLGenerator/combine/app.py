# app.py
from flask import Flask, render_template
import AHtml
import BHtml
import EHtml
import DHtml
import CHtml
from knowledgebase import KnowledgeBase
from sfia import SFIA
from urllib.parse import unquote
from generate_course_html import generate_course_html
from caidi import CAIDI

cd = CAIDI( 'caidi-data-for-ACS-A.zip')

app = Flask(__name__, static_url_path='/static', static_folder='static')

# Initialize the KnowledgeBase and SFIA
kb = KnowledgeBase('CSSE-allprograms-outcome-mappings-20241011.xlsx', SFIA('sfia_v8_custom.xlsx'), cd)

@app.route('/')
def home():
    # Pass a flag to indicate this is the "criteria" sidebar
    return render_template('index.html', sidebar_type='criteria', sidebar_active=False)

@app.route('/coursebased')
def course_based():
    # Fetch course names dynamically from the knowledge base
    course_names = list(kb.criterionB.keys())  # Get the course names from the KnowledgeBase
    return render_template('coursebased.html', courses=course_names, sidebar_type='courses', sidebar_active=True)

@app.route('/coursebased/course/<course_name>')
def course_details(course_name):
    # Decode the course name if necessary
    course_name = unquote(course_name.replace('_', ' '))

    # Fetch course names dynamically from the knowledge base
    course_names = list(kb.criterionB.keys())  # Get the course names from the KnowledgeBase

    # Generate the HTML content for this course
    html_content = generate_course_html(course_name)

    # Render the course with the course sidebar
    return render_template('course_criteria.html', course_name=course_name, course_content=html_content, sidebar_type='courses', courses=course_names, sidebar_active=True)
@app.route('/A')
def execute_A():
    html_content = AHtml.generate_html_content()
    return render_template('criteria_A.html', script_output=html_content,sidebar_type='criteria', sidebar_active=False)

@app.route('/B')
def criteria_b():
    html_content = BHtml.generate_html_content()
    return render_template('criteria_B.html', script_output=html_content, sidebar_type='criteria', sidebar_active=False)

@app.route('/C')
def execute_C():
    html_content = CHtml.generate_html_content()    
    return render_template('criteria_C.html',script_output=html_content, sidebar_type='criteria', sidebar_active=False)

@app.route('/D')
def criteria_d():
    html_content = DHtml.generate_html_content()
    return render_template('criteria_D.html', script_output=html_content, sidebar_type='criteria', sidebar_active=False)

@app.route('/E')
def criteria_e():
    html_content = EHtml.generate_html_content()
    return render_template('criteria_E.html', script_output=html_content, sidebar_type='criteria', sidebar_active=False)

if __name__ == '__main__':
    app.run(debug=True)