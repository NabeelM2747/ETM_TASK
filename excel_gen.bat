@echo off
cd C:\Users\HP\OneDrive\Desktop\Task\ETM :: Replace with the actual path to your project folder
call venv\Scripts\activate   :: Activate the virtual environment (adjust if different)
python excel_gen.py   :: Replace with your actual Django management command
deactivate
echo Excel file generated successfully!
pause