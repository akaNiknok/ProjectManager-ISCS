from django.contrib import admin

from .models import Project, User, Member, Task, TaskAssignment, Expense

admin.site.register(Project)
admin.site.register(User)
admin.site.register(Member)
admin.site.register(Task)
admin.site.register(TaskAssignment)
admin.site.register(Expense)
