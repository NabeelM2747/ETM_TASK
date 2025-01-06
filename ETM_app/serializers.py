from rest_framework import serializers
from .models import *


class UserMasterSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    user_status_display = serializers.CharField(source='get_user_status_display', read_only=True)

    class Meta:
        model = UserMaster
        fields = ['id', 'username', 'email', 'firstname', 'lastname', 'role', 'role_display', 'user_status',
                  'user_status_display', 'created_at']


class TaskSerializer(serializers.ModelSerializer):
    employee_username = serializers.CharField(source='employee_id.username', read_only=True)
    employee_name = serializers.SerializerMethodField()  # Custom field for full name

    class Meta:
        model = Tasks
        fields = [
            'id', 'employee_id', 'employee_username', 'employee_name', 'task_name', 'description', 'time_logged',
            'created_at']

    def get_employee_name(self, obj):
        return f"{obj.employee_id.firstname} {obj.employee_id.lastname}"


class CommentSerializer(serializers.ModelSerializer):
    task_name = serializers.CharField(source='task_id.task_name', read_only=True)
    task_description = serializers.CharField(source='task_id.description', read_only=True)
    employee_username = serializers.CharField(source='task_id.employee_id.username', read_only=True)
    task_done_by = serializers.SerializerMethodField()
    commented_by_username = serializers.CharField(source='commented_by.username', read_only=True)
    commented_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'task_id', 'task_name', 'task_description', 'comments',
            'commented_by', 'commented_by_username', 'commented_by_name',
            'employee_username', 'task_done_by', 'created_at'
        ]

    def get_commented_by_name(self, obj):
        return f"{obj.commented_by.firstname} {obj.commented_by.lastname}"

    def get_task_done_by(self, obj):
        return f"{obj.task_id.employee_id.firstname} {obj.task_id.employee_id.lastname}"

