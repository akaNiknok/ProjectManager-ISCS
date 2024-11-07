from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date


class Project(models.Model):

    class Status(models.IntegerChoices):
        ONGOING = 0, _("Ongoing")
        FINISHED = 1, _("Finished")
        ARCHIVED = 2, _("Archived")

    project_id = models.SmallAutoField(primary_key=True)
    project_name = models.CharField(max_length=255)
    project_desc = models.TextField()
    project_start = models.DateField(default=date.today)
    project_end = models.DateField(default=None, blank=True, null=True)
    project_status = models.IntegerField(choices=Status, default=Status.ONGOING)

    def __str__(self):
        return "{}: {} ({})".format(self.project_id, self.project_name, self.project_status)


class User(models.Model):

    class sType(models.TextChoices):
        EXECUTIVE = "X", _("Executive")
        MANAGER = "M", _("Manager")
        EMPLOYEE = "Em", _("Employee")

    user_id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.BinaryField()
    # TODO: profile pics
    staff_type = models.CharField(max_length=2, choices=sType, default=sType.EMPLOYEE)

    def __str__(self):
        return "{}: {} ({})".format(self.user_id, self.name, self.staff_type)


class Member(models.Model):

    member_id = models.SmallAutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{} is a member of {}".format(self.user.name, self.project.project_name)


class Task(models.Model):

    class Status(models.IntegerChoices):
        INPROGRESS = 0, _("In Progress")
        FORREVIEW = 1, _("For Review")
        COMPLETED = 2, _("Completed")
    
    class Priority(models.TextChoices):
        HIGH = "H", _("High")
        MEDIUM = "M", _("Medium")
        LOW = "L", _("Low")

    task_id = models.SmallAutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=255)
    task_notes = models.TextField(blank=True, null=True)
    task_deadline = models.DateField(default=date.today, blank=True, null=True)
    task_status = models.IntegerField(choices=Status, default=Status.INPROGRESS)
    task_priority = models.CharField(max_length=1, choices=Priority)

    def __str__(self):
        return "{}: {} ({} - {})".format(
            self.task_id,
            self.task_name,
            self.task_status,
            self.task_priority
        )


class TaskAssignment(models.Model):

    assignment_id = models.SmallAutoField(primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return "{} is tasked to {}".format(self.member.user.name, self.task.task_name)


class Expense(models.Model):

    expense_id = models.SmallAutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    expense_date = models.DateField(default=date.today)
    expense_desc = models.TextField()
    expense_amt = models.DecimalField(max_digits=11, decimal_places=2)  # TODO: Change in data dictionary

    def __str__(self):
        return "{}: PHP {} to {}".format(
            self.expense_id,
            self.expense_amt,
            self.project.project_name
        )


class Notification(models.Model):

    class Status(models.IntegerChoices):
        UNREAD = 0, _("Unread")
        READ = 1, _("Read")

    notif_id = models.SmallAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notif_datetime = models.DateTimeField()
    notif_text = models.CharField(max_length=255)
    notif_status = models.IntegerField(choices=Status, default=Status.UNREAD)
