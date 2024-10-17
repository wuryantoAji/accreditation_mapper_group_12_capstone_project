import os
import shutil
import subprocess
import tempfile
import json

# Constant
knowledge_base = "KnowledgeBase"
latex_generator = "LatexGenerator"
client_input = "ClientInput"
config_path = os.path.join(os.path.dirname(__file__), 'config.json')

def create_temp_folder():
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    print(f"Temporary directory created: {temp_dir}")
    return temp_dir

def copy_constant_files(temp_dir, excelClientInput, sfiaExcelInput, caidiZipInput):
    input_excel_file = os.path.join(client_input, excelClientInput) 
    caidi_zip_file = os.path.join(client_input, caidiZipInput)
    sfia_excel_file = os.path.join(knowledge_base, sfiaExcelInput)
    knowledge_base_python_file = os.path.join(knowledge_base, "knowledgebase.py")
    sfia_python_file = os.path.join(knowledge_base, "sfia.py")
    caidi_python_file = os.path.join(knowledge_base, "caidi.py")

    shutil.copy("pyproject.toml", temp_dir)
    shutil.copy(input_excel_file, temp_dir)
    shutil.copy(sfia_excel_file, temp_dir)
    shutil.copy(caidi_zip_file, temp_dir)
    shutil.copy(knowledge_base_python_file, temp_dir)
    shutil.copy(sfia_python_file, temp_dir)
    shutil.copy(caidi_python_file, temp_dir)
    print(f"Copied constant files to {temp_dir}")  

def copy_latex_program(temp_dir):
    latex_generator_python = os.path.join(latex_generator, "createLatexTemplate.py")
    latex_stylesheet_file = os.path.join(latex_generator, "latexStyleSheet.sty")

    shutil.copy(latex_generator_python, temp_dir)
    shutil.copy(latex_stylesheet_file, temp_dir)
    print(f"Copied latex program to {temp_dir}")

def run_python_program(temp_dir, clientInputFile, sfiaInputFile, caidiInputFile, latexConfig):
    # Run the Python program in the temporary directory using Poetry's environment
    script_path = os.path.join(temp_dir, "createLatexTemplate.py")
    if(latexConfig['generateAll']):
        result = subprocess.run(["python", script_path, '-s', latexConfig['sortBy'], '-i', clientInputFile, '-si', sfiaInputFile, '-ci', caidiInputFile], cwd=temp_dir)
    else:
        result = subprocess.run(["python", script_path, '-s', latexConfig['sortBy'], '-i', clientInputFile, '-si', sfiaInputFile, '-ci', caidiInputFile, '-ca', latexConfig['generateCriterionA'], '-cb', latexConfig['generateCriterionB'], '-cc', latexConfig['generateCriterionC'], '-cd', latexConfig['generateCriterionD'], '-ce', latexConfig['generateCriterionE']], cwd=temp_dir)
    
    if result.returncode != 0:
        raise Exception(f"Python script failed with exit code {result.returncode}")
    
    print("Python program executed successfully")

def copy_generated_files_to_output(temp_dir):
    latex_output_zip = os.path.join(temp_dir, "latex_output.zip")
    shutil.copy(latex_output_zip, '.')

def clean_up(temp_dir):
    # Remove the temporary directory
    if temp_dir and os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        print(f"Temporary directory {temp_dir} has been cleaned up")

def main():
    temp_dir = None
    try:
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                print("Configuration loaded successfully:", config)
        except FileNotFoundError:
            print(f"Error: config.json file not found at {config_path}")
        except json.JSONDecodeError:
            print("Error: Failed to decode the config.json file")
        temp_dir = create_temp_folder()
        copy_constant_files(temp_dir, config["clientInputFile"], config["sfiaFile"], config["caidiFile"])
        copy_latex_program(temp_dir)
        run_python_program(temp_dir, config["clientInputFile"], config["sfiaFile"], config["caidiFile"], config["latexConfig"])
        copy_generated_files_to_output(temp_dir)
    finally:
        if temp_dir:
            clean_up(temp_dir)

if __name__ == "__main__":
    main()
