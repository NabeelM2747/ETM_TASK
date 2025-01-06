# ETM_TASK

Employee Task Management System

Project Overview
This project is designed to manage employees' tasks. It supports the following features:

CRUD Operations for Employees: Create, Read, Update, and Delete employee records.
Task Creation: Tasks can be assigned to employees.
Task Retrieval: Retrieve tasks of individual employees, all tasks, and add comments to tasks by a super admin.
Export to Excel: Generate an Excel report of tasks and comments for all employees.

Setup Instructions
1. Clone the repository and set up the virtual environment:

git clone <repository-url>
cd <project-folder>
python -m venv venv
venv\Scripts\activate

2. Install dependencies:

pip install -r requirements.txt

3. Set up Django:
Ensure that you have your Django project set up with appropriate settings in settings.py.
Run database migrations:

python manage.py migrate

Additional Files
1. Batch File
The batch file used for scheduling the export to Excel task is included in the project directory. It is designed to:

Activate the virtual environment.
Run the excel_gen.py script that generates the Excel file.
Deactivate the virtual environment after the task is completed.
The batch file is scheduled to run at a specified time using Windows Task Scheduler.

2. Postman Collections
The Postman collections for testing the API endpoints are also included in the project. You can import these collections into Postman for testing the following features:

Additional Notes
Scheduling Issue: Initially, an attempt was made to use Celery and Redis for scheduling the export to Excel task. Due to limited experience with these technologies, the correct output wasn't achieved. A Windows batch file was used as a workaround to generate and export the Excel file.
