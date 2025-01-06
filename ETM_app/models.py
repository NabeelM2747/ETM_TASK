from django.db import models


# Create your models here.

class UserMaster(models.Model):
    ROLE_CHOICES = (
        (1, 'Super Admin'),
        (2, 'Employee'),
    )
    User_Sts = (
        (0, 'In-Active'),
        (1, 'Active'),
    )
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    firstname = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150)
    role = models.IntegerField(choices=ROLE_CHOICES, default=2)  # Default to 'Employee'
    created_at = models.DateTimeField(auto_now_add=True)
    user_status = models.IntegerField(choices=User_Sts, default=1)  # Default to 'Active'

    def __str__(self):
        return f"User Details of {self.username}"


class Tasks (models.Model):
    id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(UserMaster, on_delete=models.CASCADE, related_name="tasks")
    task_name = models.CharField(max_length=255)
    description = models.TextField()
    time_logged = models.DurationField(help_text="Time logged in HH:MM:SS format")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task_name} by {self.employee_id.username}"


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    task_id = models.ForeignKey(Tasks, on_delete=models.CASCADE, related_name="comments")
    comments = models.TextField()
    commented_by = models.ForeignKey(UserMaster, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.commented_by.username} on {self.task_id.task_name}"
