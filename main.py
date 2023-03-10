import eel
import os

from io import BytesIO
from PyPDF2 import PdfReader

import xlsxwriter
from datetime import datetime

@eel.expose
def upload_file(file_name, file_size, file_type, file_data):
    # Print the file information
    print(f'File Name: {file_name}')
    print(f'File Size: {file_size}')
    print(f'File Type: {file_type}')

    # Check if the file type is PDF
    if file_type == 'application/pdf':
         # Create a BytesIO object from the file data
        pdf_data = BytesIO(bytes(file_data))

        # Create a PdfReader object from the BytesIO object
        reader = PdfReader(pdf_data)

        # Read the text from the PDF file
        text = ''
        for page in reader.pages:
            text += page.extract_text()
            print('===-======')
            print(text)
            print('===-======')

        # Return the text to JavaScript
        return text
    
    else:
        # Return an error message to JavaScript
        return f'Error: File "{file_name}" is not a PDF file.'



@eel.expose
def create_excel_file(content, fname):
    
    # Get the full path of the Excel file
    #filename = f'{datetime.now().strftime("%Y-%m-%d")}.xlsx'
    filename = f'{fname}.xlsx'
    filepath = os.path.join(os.path.expanduser("~"), filename)
    print('=================== file path ===================')
    print(filepath)
    
    # Check if the file already exists
    count = 0
    while os.path.exists(filepath):
        # If the file exists, append a number to the filename
        count += 1
        #new_filename = f'{datetime.now().strftime("%Y-%m-%d")}({count}).xlsx'
        new_filename = f'{fname}({count}).xlsx'
        filepath = os.path.join(os.path.expanduser("~"), new_filename)

     # Save the workbook to the specified filepath
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    workbook = xlsxwriter.Workbook(filepath)
    worksheet = workbook.add_worksheet()

    # Set the column widths
    worksheet.set_column(0, 0, 15)
    worksheet.set_column(1, 1, 15)
    worksheet.set_column(2, 2, 15)
    worksheet.set_column(3, 3, 25)

    # Write the headers
    worksheet.write(0, 0, 'Name')
    worksheet.write(0, 1, 'Price')
    worksheet.write(0, 2, 'Date')

    # Split the content into an array of lines
    lines = content.split('\n')

    # Write the data
    row = 1
    for line in lines:
        line = line.strip()
        print('==============')
        print(line)
        print('==============')
        if line:
            worksheet.write(row, 0, line)
            worksheet.write(row, 1, 1000 + row)
            worksheet.write(row, 2, datetime.now().strftime("%Y-%m-%d"))
            row += 1

    # Close the workbook
    workbook.close()

    # Return the filename of the Excel file
    return filepath

if __name__ == '__main__':
    # Set the path to the 'web' directory
    web_dir = os.path.join(os.path.dirname(__file__), 'web')

    # Start the EEL app
    eel.init(web_dir)
    eel.start('index.html', size=(600, 400))
