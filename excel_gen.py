import os
import django
from django.core.management import call_command
from django.test import Client

# Set the environment variable to specify settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ETM.settings')  # Replace with your project settings
django.setup()

# Initialize the Django test client
client = Client()

# Simulate the GET request to the export view
response = client.get('http://127.0.0.1:8000/api/tasks/export/')  # Replace with the correct URL

if response.status_code == 200:
    with open('tasks_and_comments_report.xlsx', 'wb') as f:
        f.write(response.content)
    print(f"Excel file generated successfully!: {response.status_code}")
else:
    print(f"Failed to generate Excel. Status code: {response.status_code}")
