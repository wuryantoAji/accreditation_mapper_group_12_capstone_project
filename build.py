import os
import shutil
import subprocess
import tempfile

# Constant
knowledge_base = "KnowledgeBase"
latex_generator = "LatexGenerator"
client_input = "ClientInput"

def install_dependencies():
    # Install dependencies from requirements.txt using Poetry
    subprocess.run(["poetry", "install"], check=True)

    print("Dependencies installed.")

def create_temp_folder():
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    print(f"Temporary directory created: {temp_dir}")
    return temp_dir

def copy_constant_files(temp_dir):
    # TODO change to fetch the latest file by sort from new to old
    input_excel_file = os.path.join(client_input, "CSSE-allprograms-outcome-mappings-20240913.xlsx")
    # TODO change to fetch the latest file by sort from new to old also filter by .xlsx
    sfia_excel_file = os.path.join(knowledge_base, "sfiaskills.6.3.en.1.xlsx")
    knowledge_base_python_file = os.path.join(knowledge_base, "knowledgebase.py")
    sfia_python_file = os.path.join(knowledge_base, "sfia.py")

    shutil.copy("pyproject.toml", temp_dir)
    shutil.copy(input_excel_file, temp_dir)
    shutil.copy(sfia_excel_file, temp_dir)
    shutil.copy(knowledge_base_python_file, temp_dir)
    shutil.copy(sfia_python_file, temp_dir)
    print(f"Copied constant files to {temp_dir}")  

def copy_latex_program(temp_dir):
    latex_generator_python = os.path.join(latex_generator, "createLatexTemplate.py")
    latex_stylesheet_file = os.path.join(latex_generator, "latexStyleSheet.sty")

    shutil.copy(latex_generator_python, temp_dir)
    shutil.copy(latex_stylesheet_file, temp_dir)
    print(f"Copied latex program to {temp_dir}")

def run_python_program(temp_dir):
    # Run the Python program in the temporary directory using Poetry's environment
    script_path = os.path.join(temp_dir, "createLatexTemplate.py")
    result = subprocess.run(["poetry", "run", "python", script_path], cwd=temp_dir)
    
    if result.returncode != 0:
        raise Exception(f"Python script failed with exit code {result.returncode}")
    
    print("Python program executed successfully")

def copy_generated_files_to_output(temp_dir):
    latex_stylesheet_file = os.path.join(temp_dir, "latexStyleSheet.sty")
    latex_main_file = os.path.join(temp_dir, "main.tex")
    latex_criterionA_file = os.path.join(temp_dir, "criterionA.tex")
    latex_criterionB_file = os.path.join(temp_dir, "criterionB.tex")
    latex_criterionC_file = os.path.join(temp_dir, "criterionC.tex")
    latex_criterionD_file = os.path.join(temp_dir, "criterionD.tex")
    # latex_criterionE_file = os.path.join(temp_dir, "criterionE.tex")
    
    latexDirectoryPath = os.path.join('.', 'latexFiles')
    latexDirectory = os.mkdir(latexDirectoryPath)

    shutil.copy(latex_stylesheet_file, latexDirectoryPath)
    shutil.copy(latex_main_file, latexDirectoryPath)
    shutil.copy(latex_criterionA_file, latexDirectoryPath)
    shutil.copy(latex_criterionB_file, latexDirectoryPath)
    shutil.copy(latex_criterionC_file, latexDirectoryPath)
    shutil.copy(latex_criterionD_file, latexDirectoryPath)
    # shutil.copy(latex_criterionE_file, latexDirectoryPath))
    

def clean_up(temp_dir):
    # Remove the temporary directory
    if temp_dir and os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        print(f"Temporary directory {temp_dir} has been cleaned up")

def main():
    temp_dir = None
    try:
        install_dependencies()
        temp_dir = create_temp_folder()
        copy_constant_files(temp_dir)
        copy_latex_program(temp_dir)
        run_python_program(temp_dir)
        copy_generated_files_to_output(temp_dir)
    finally:
        if temp_dir:
            clean_up(temp_dir)

if __name__ == "__main__":
    main()
