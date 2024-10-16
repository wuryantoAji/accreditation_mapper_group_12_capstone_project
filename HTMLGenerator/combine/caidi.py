import pandas as pd
import zipfile
from io import BytesIO
from openpyxl import load_workbook
from bs4 import BeautifulSoup

class CAIDI:
    def __read_first_sentence_from_html(self, content):
        # Parse the HTML content
        soup = BeautifulSoup(content, 'html.parser')

        # Remove the title element
        if soup.title:
            soup.title.decompose()

        # Get the text and split it into sentences
        text = soup.get_text()
        sentences = text.split('.')

        # Print the first sentence, stripping whitespace
        first_sentence = sentences[0].strip() + '.' if sentences else ''
        return first_sentence
    
    def __init__(self, caidi_zip_file ):
        self.course = {}
        self.units = {}

        try:
            with zipfile.ZipFile(caidi_zip_file, 'r') as zip_file:
                # Print the list of file names in the ZIP file
                for file_info in zip_file.infolist():
                    # Check if the file is an Excel file
                    if file_info.filename.endswith(('.xls', '.xlsx')):
                        with zip_file.open(file_info) as file:
                            # Read the file content into a BytesIO object
                            file_bytes = BytesIO(file.read())

                            # Load the workbook from the BytesIO object
                            workbook = load_workbook(file_bytes)
                            # Select the active worksheet
                            worksheet = workbook.active
                            # Get the value from cell A1
                            course = str(worksheet['A2'].value)
                            course = course[course.index('units in '):]

                            file_bytes.seek(0)
                            self.units[course] = pd.read_excel(file_bytes, header=2)
                    # Check if the file is a HTML file
                    elif file_info.filename.endswith(('.htm', '.html')):
                        print(file_info.filename)
                        grand_table = pd.DataFrame()
                        with zip_file.open(file_info) as file:
                            # Read the file content into a BytesIO object
                            file_bytes = BytesIO(file.read())

                            tables = pd.read_html( file_bytes )

                            for table in tables:
                                # Tables with key/value pairs only have two columns
                                if len(table.columns) == 2 and [value for value in [0, 1] if value in table.columns]:
                                    grand_table = pd.concat([grand_table, table], ignore_index=True)
                                #if len(table.columns) == 4:
                                #    print(table)

                            result_dict = {}
                            for index, row in grand_table.iterrows():
                                key = row[0]
                                value = row[1]
                                result_dict[key] = value

                            file_bytes.seek(0)
                            first_sentence = self.__read_first_sentence_from_html(file_bytes)
                            #print(first_sentence)
                            if first_sentence.startswith('Active postgraduate'):
                                code = result_dict['Course code']
                            if first_sentence.startswith('Active major'):
                                code =  result_dict['Code']
                            if code in self.course:
                                self.course[code] = {**self.course[code], **result_dict}
                            else:
                                self.course[code] = result_dict
                                

        except FileNotFoundError:
            print(f"The file {caidi_zip_file} does not exist.")
        except zipfile.BadZipFile:
            print(f"The file {caidi_zip_file} is not a valid ZIP file.")

        return