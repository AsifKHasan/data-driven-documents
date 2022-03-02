# Software and Tools required
1. Python 3.8 or higher - https://www.python.org/downloads/
2. Git -  https://git-scm.com/downloads
3. MikTex - https://miktex.org/download
4. LibreOffice - https://www.libreoffice.org/download/download/
5. Pandoc - https://pandoc.org/installing.html


# Verify the installations
1. create a directory in your laptop where you keep your office files and programs. Normally I keep them all under D:\projects. Chose your own directory
2. open a command prompt and cd to D:\projects (or whatever your chosen directory is)
3. run command ```python -version``` and send me the output
4. run command ```python -m pip install --upgrade pip``` and send me the output
5. run command ```pip --version``` and send me the output
6. run command ```git --version``` and send me the output
7. run command ```miktex --version``` and send me the output
8. run command ```"C:\Program Files\LibreOffice\program\soffice"  --version``` and send me the output
9. run command ```pandoc --version``` and send me the output


# Get the scripts/programs
## data-driven-documents
1. cd to D:\projects
2. run ```git clone https://github.com/AsifKHasan/data-driven-documents.git``` and send me the output
3. cd to D:\projects\data-driven-documents\document-from-data
4. run command ```pip install -r requirements.txt```. See if there is any error or not. If you get errors share the output with me.
5. cd to D:\projects\data-driven-documents\salary-sheet
6. run command ```pip install -r requirements.txt```. See if there is any error or not. If you get errors share the output with me.

## gsheet-to-docx
1. cd to d:\projects
2. run ```git clone https://github.com/AsifKHasan/gsheet-to-docx.git``` and send me the output
3. cd to D:\projects\gsheet-to-docx
4. run command ```pip install -r requirements.txt```. See if there is any error or not. If you get errors share the output with me.


# Configure the scripts/programs
## data-driven-documents/document-from-data
1. get a file named *credential.json* from me and paste/copy to D:\projects\data-driven-documents\document-from-data\conf

## data-driven-documents/document-from-data
1. get a file named *credential.json* from me and paste/copy to D:\projects\data-driven-documents\salary-sheet\conf

## gsheet-to-docx
1. get a file named *credential.json* from me and paste/copy to D:\projects\gsheet-to-docx\conf
2. copy the file D:\projects\gsheet-to-docx\conf\config.yml.dist as a new file D:\projects\gsheet-to-docx\conf\config.yml


# Running scripts/programs
# offer-letter
1. cd to D:\projects\data-driven-documents\document-from-data\src
if working for Spectrum
2.  run command ```python spectrum-offer-letter.py```
3. if everything goes well you will get individual letters in D:\projects\data-driven-documents\document-from-data\out\spectrum\offer-letter\tmp and combined letters in D:\projects\data-driven-documents\document-from-data\out\spectrum\offer-letter

# transfer-letter
1. cd to D:\projects\data-driven-documents\document-from-data\src
if working for Spectrum
2.  run command ```python spectrum-transfer-notice-letter.py```
3. if everything goes well you will get individual letters in D:\projects\data-driven-documents\document-from-data\out\spectrum\transfer-notice\tmp and combined letters in D:\projects\data-driven-documents\document-from-data\out\spectrum\transfer-notice

# salary-sheet
1. cd to D:\projects\data-driven-documents\salary-sheet\src
2a. if working for Spectrum run command ```python spectrum-salary-advice-app.py```
2b. if working for SSCL run command ```python sscl-salary-advice-app.py```
