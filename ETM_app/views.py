import json
from rest_framework.decorators import api_view
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from openpyxl import Workbook
from io import BytesIO
from django.utils.timezone import make_naive


# Line No: 11 to 80 (CRUD operations of employees)
# Get all users
@api_view(['GET'])
def get_users(request):
    users = UserMaster.objects.all()
    serializer = UserMasterSerializer(users, many=True)
    return Response(serializer.data)


# Get a single user by ID
@api_view(['GET'])
def get_user(request, user_id):
    try:
        user = UserMaster.objects.get(id=user_id)
    except UserMaster.DoesNotExist:
        return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserMasterSerializer(user)
    return Response({"Message": "Fetched Successfully"}, serializer.data, status=status.HTTP_200_OK)


# Create a new user
@api_view(['POST'])
def create_user(request):
    serializer = UserMasterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"Message": "User Created Successfully", "data": serializer.data},
                        status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Update an existing user
@api_view(['PUT'])
def update_user(request):
    try:
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)
        user_id = data['user_id']
        print(user_id)
        user = UserMaster.objects.get(id=user_id)
    except UserMaster.DoesNotExist:
        return Response({"Message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserMasterSerializer(user, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"Message": "Data Updated Successfully", "Data": serializer.data},
                        status=status.HTTP_202_ACCEPTED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete a user
@api_view(['DELETE'])
def delete_user(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    user_id = data['user_id']
    print(user_id)
    if not user_id:
        return Response({"detail": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = UserMaster.objects.get(id=user_id)
    except UserMaster.DoesNotExist:
        return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    user.delete()
    return Response({"detail": "User deleted"}, status=status.HTTP_204_NO_CONTENT)


# Line No: 85 to 168  (Creation and Retrieval operations of tasks)
@api_view(['POST'])
def create_task(request):
    # Validate the data using the serializer
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        # Save the task
        serializer.save()
        return Response({"Message": "Task created successfully", "Data": serializer.data},
                        status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_tasks_by_employee(request):
    # Filter tasks by employee_id
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    employee_id = data['employee_id']
    print(employee_id)
    if not employee_id:
        return Response({"Message": "Employee ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        employee_det = UserMaster.objects.get(id=employee_id)
    except UserMaster.DoesNotExist:
        return Response({"Message": "Employee doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        # Fetch tasks for the employee
    tasks = Tasks.objects.filter(employee_id=employee_id).select_related('employee_id')
    if not tasks.exists():
        return Response({"Message": "No tasks found for this employee"}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskSerializer(tasks, many=True)

    if employee_det.user_status == 0:
        return Response({
            "Message_1": "Employee is in inactive state",
            "Message_2": "Tasks fetched successfully",
            "Data": serializer.data
        }, status=status.HTTP_200_OK)

    return Response({
        "Message_1": "Employee is in active state",
        "Message_2": "Tasks fetched successfully",
        "Data": serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_all_tasks(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    employee_id = data['employee_id']
    try:
        user = UserMaster.objects.get(id=employee_id)
        if user.role != 1:  # 1 = Super Admin
            return Response({"Message": "Access denied. Only Super Admins can perform this action."},
                            status=status.HTTP_403_FORBIDDEN)
    except UserMaster.DoesNotExist:
        return Response({"Message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
    # Retrieve all including comments
    tasks = Tasks.objects.select_related('employee_id').prefetch_related('comments')
    task_list = []
    for task in tasks:
        task_data = {
            "id": task.id,
            "employee_id": task.employee_id.id,
            "employee_name": f"{task.employee_id.firstname} {task.employee_id.lastname}",
            "task_name": task.task_name,
            "description": task.description,
            "time_logged": task.time_logged,
            "created_at": task.created_at,
            "comments": [
                {
                    "comment_id": comment.id,
                    "commented_by": comment.commented_by.username,
                    "comment": comment.comments,
                    "created_at": comment.created_at,
                }
                for comment in task.comments.all()
            ] if task.comments.exists() else None,  # Default to NULL if no comments
        }
        task_list.append(task_data)

    return Response({"Message": "Tasks retrieved successfully", "Data": task_list}, status=status.HTTP_200_OK)


# Line No: 172 to 207  (Creation of comments on each task)
@api_view(['POST'])
def admin_manage_tasks(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    task_id = data['task_id']
    comment_text = data['comment']

    if not task_id or not comment_text:
        return Response({"Message": "Both task_id and comment are required"}, status=status.HTTP_400_BAD_REQUEST)

    # Ensure the user is a Super Admin
    employee_id = data['employee_id']
    try:
        user_obj = UserMaster.objects.get(id=employee_id)
        if user_obj.role != 1:  # 1 = Super Admin
            return Response({"Message": "Access denied. Only Super Admins can perform this action."},
                            status=status.HTTP_403_FORBIDDEN)
    except UserMaster.DoesNotExist:
        return Response({"Message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

    # Verify task existence
    try:
        task = Tasks.objects.get(id=task_id)
    except Tasks.DoesNotExist:
        return Response({"Message": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
    existing_comment = Comment.objects.filter(task_id=task_id).first()
    if existing_comment:
        commented_by = existing_comment.commented_by
        return Response({"Message": f"Task already commented by {commented_by.username}"},
                        status=status.HTTP_400_BAD_REQUEST)
    # Create a new comment
    comment = Comment.objects.create(task_id=task, comments=comment_text, commented_by=user_obj)
    # Serialize and return the created comment
    serializer = CommentSerializer(comment)
    return Response({"Message": "Comment added successfully", "Comment_Details": serializer.data},
                    status=status.HTTP_201_CREATED)


# Line No: 212 to 256 (Weekly Excel Report Generation)
@api_view(['GET'])
def export_tasks_to_excel(request):
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
        # Iterate over all comments for the task
        for comment in task.comments.all():
            # Convert datetime objects to naive (timezone-unaware)
            task_created_at = make_naive(task.created_at) if task.created_at.tzinfo else task.created_at
            comment_created_at = make_naive(comment.created_at) if comment.created_at.tzinfo else comment.created_at

            row = [
                task.id,
                f"{task.employee_id.firstname} {task.employee_id.lastname}",
                task.task_name,
                task.description,
                task.time_logged,
                task_created_at,  # Use naive datetime
                comment.id,
                f"{comment.commented_by.firstname} {comment.commented_by.lastname}",
                comment.comments,
                comment_created_at  # Use naive datetime
            ]
            ws.append(row)

    # Save the workbook to a BytesIO object
    byte_io = BytesIO()
    wb.save(byte_io)
    byte_io.seek(0)

    # Prepare the response with the Excel file as an attachment
    response = HttpResponse(byte_io, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="tasks_and_comments_report.xlsx"'

    return response

