from celery import shared_task
from io import BytesIO
from openpyxl import Workbook
from django.core.files.storage import default_storage
from .models import Tasks
from django.utils.timezone import make_naive


@shared_task
def export_to_excel():
    # Fetch all tasks with their comments
    tasks = Tasks.objects.select_related('employee_id').prefetch_related('comments')

    # Create an in-memory workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Task Report"

    # Create the header row
    header = ["Task ID", "Employee Name", "Task Name", "Description", "Time Logged", "Created At",
              "Comment ID", "Commented By", "Comment", "Comment Created At"]
    ws.append(header)

    # Iterate through tasks and their comments to populate the Excel file
    for task in tasks:
        for comment in task.comments.all():
            task_created_at = make_naive(task.created_at) if task.created_at.tzinfo else task.created_at
            comment_created_at = make_naive(comment.created_at) if comment.created_at.tzinfo else comment.created_at

            row = [
                task.id,
                f"{task.employee_id.firstname} {task.employee_id.lastname}",
                task.task_name,
                task.description,
                task.time_logged,
                task_created_at,
                comment.id,
                f"{comment.commented_by.firstname} {comment.commented_by.lastname}",
                comment.comments,
                comment_created_at
            ]
            ws.append(row)

    # Save the workbook to the file system
    file_name = "tasks_and_comments_report.xlsx"
    byte_io = BytesIO()
    wb.save(byte_io)
    byte_io.seek(0)

    # Save the Excel file into the default storage
    with default_storage.open(file_name, 'wb') as f:
        f.write(byte_io.read())

    # Log the file path to check if it's being created
    print(f"Excel file saved to: {default_storage.path(file_name)}")

    return file_name
