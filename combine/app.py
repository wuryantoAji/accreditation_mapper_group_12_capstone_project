# app.py
from flask import Flask, render_template
import BHtml

app = Flask(__name__, static_url_path='/static', static_folder='static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/A')
def execute_A():
    return render_template('criteria_A.html')

# app.py
@app.route('/B')
def criteria_b():
    html_content = BHtml.generate_html_content()
    print(html_content)  # This will print the content to the console
    return render_template('criteria_B.html', script_output=html_content)

@app.route('/C')
def execute_C():
    return render_template('criteria_C.html')

@app.route('/D')
def execute_D():
    return render_template('criteria_D.html')

@app.route('/E')
def execute_E():
    return render_template('criteria_E.html')

if __name__ == '__main__':
    app.run(debug=True)