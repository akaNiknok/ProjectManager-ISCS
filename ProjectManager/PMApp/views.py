from django.shortcuts import render, redirect, Http404
from django.http import HttpResponse
from django.db.models import Case, Value, When

from .models import Project, User, Member, Task, TaskAssignment, Expense

import bcrypt
import datetime 

def login(request):
    if request.method == "POST":
        # Get form fields
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Validate username
        try:
            user_obj = User.objects.get(username=username)
        except:
            return render(request, "login.html", {"error": True})
        
        # Validate password
        bytes = password.encode('utf-8')
        password_matches = bcrypt.checkpw(bytes, user_obj.password) 
        if not password_matches:
            return render(request, "login.html", {"error": True})
        
        # Login successful
        response = redirect("dashboard")
        response.set_cookie("user_id", user_obj.user_id)
        return response

    else:
        return render(request, "login.html")


def register(request):
    if request.method == "POST":
        # Get form fields
        name = request.POST.get("name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        retype_pass = request.POST.get("retype_pass")

        # Validate username
        if len(User.objects.filter(username=username)) != 0:
            return render(request, "register.html", {"username_error": True})
        
        # Validate password
        if password != retype_pass:
            return render(request, "register.html", {"password_error": True})
        
        # Hash password
        bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes, salt)

        user_obj = User.objects.create(
            name=name,
            username=username,
            password=hash,
            staff_type="Em"
        )
        
        # Login successful
        response = redirect("dashboard")
        response.set_cookie("user_id", user_obj.user_id)
        return response

    else:
        return render(request, "register.html")


def logout(request):
    response = redirect("login")
    response.delete_cookie("user_id")
    if request.session["current_project_id"]:
        del request.session["current_project_id"]
    request.session.modified = True
    return response


def dashboard(request):

    # Validate and retrieve current logged in user id
    user_id = request.COOKIES.get("user_id")

    if user_id is None:
        return redirect("login")
    
    # Retrieve user obj 
    user_obj = User.objects.get(user_id=user_id)

    # If manager/employee, get all projects the user is part of
    # If executive, get all projects
    if user_obj.staff_type != "X":
        project_objs = Project.objects.filter(member__user=user_obj)
    else:
        project_objs = Project.objects.all()

    # Get selected project obj
    try:
        project_id = request.session["current_project_id"]
        project_obj = Project.objects.get(project_id=project_id)
    except:
        # Default to the first project, when not specified
        if len(project_objs) > 0:
            project_obj = project_objs[0]
            project_id = project_obj.project_id
            request.session["current_project_id"] = project_id

        # If no project assigned, render empty dashboard
        else:
            request.session["current_project_id"] = None
            return render(
                request,
                "dashboard.html",
                {"user": user_obj,
                 "project": None,
                 "tasks_and_members": None,
                 "expenses": None,
                 "proj_members": None})
    
    priority_weights = Case(
            When(task_priority = Task.Priority.HIGH, then=Value(1)),
            When(task_priority = Task.Priority.MEDIUM, then=Value(2)),
            When(task_priority = Task.Priority.LOW, then=Value(3)),
            default = Value(3),)
    
    # Get tasks
    # If member is an employee, only show tasks for him/her
    if user_obj.staff_type == "Em":
        member_obj = Member.objects.get(project=project_obj, user=user_obj)
        task_objs = Task.objects.filter(project=project_obj, taskassignment__member=member_obj)
        task_objs = task_objs.order_by("task_status", priority_weights)
    else:
        task_objs = Task.objects.filter(project_id=project_id).order_by("task_status", priority_weights)

    # Get expenses
    # If member is an employee, only show tasks for him/her
    if user_obj.staff_type == "Em":
        expense_objs = Expense.objects.filter(project_id=project_id, member=member_obj)
    else:
        expense_objs = Expense.objects.filter(project_id=project_id)

    # Get members of the project for creating tasks
    proj_members_objs = Member.objects.filter(project=project_obj)

    # Get members of each task for displaying
    tasks_and_members = {}
    for task_obj in task_objs:
        member_objs = Member.objects.filter(taskassignment__task=task_obj)
        tasks_and_members[task_obj] = member_objs
    
    return render(request,
                  "dashboard.html",
                  {"user": user_obj,
                   "project": project_obj,
                   "tasks_and_members": tasks_and_members,
                   "expenses": expense_objs,
                   "proj_members": proj_members_objs})


def switch_project(request, project_id):

    # Validate and retrieve current logged in user id
    user_id = request.COOKIES.get("user_id")

    if user_id is None:
        return redirect("login")

    request.session["current_project_id"] = int(project_id)

    previous_url = request.META.get("HTTP_REFERER")
    previous_view = previous_url.rstrip('/').split('/')[-1]

    # If user was in update_project, redirect to view_project to prevent unwanted changes
    if previous_view == "update_project":
        previous_url = "view_project"

    return redirect(previous_url)


def create_project(request):

    # Validate and retrieve current logged in user id
    user_id = request.COOKIES.get("user_id")

    if user_id is None:
        return redirect("login")

    # Create project when user clicks submit
    if (request.method == "POST"):
            
        # Get submitted form values
        project_name = request.POST.get("project_name")
        project_desc = request.POST.get("project_desc")
        project_start = request.POST.get("project_start")
        project_end = request.POST.get("project_end")
        project_status = request.POST.get("project_status")
        members = [int(id) for id in request.POST.getlist('members')]

        # Set project end date to None if none specified
        if project_end == "":
            project_end = None

        # Create and save the new project
        new_project = Project.objects.create(
            project_name=project_name,
            project_desc=project_desc,
            project_start=project_start,
            project_end=project_end,
            project_status=project_status
        )

        # Automatically add the project manager as a member
        user_obj = User.objects.get(user_id=user_id)
        Member.objects.create(
            project = new_project,
            user = user_obj
        )

        # Add selected members as a member to the new project
        for member in members:
            new_user = User.objects.get(user_id = member)
            Member.objects.create(
                project = new_project,
                user = new_user
            )

        request.session["current_project_id"] = new_project.project_id
        return redirect("view_project")

    # Otherwise, display the form
    else:

        users = User.objects.exclude(staff_type="X").exclude(user_id=user_id)
        return render(request,
                      "create_project.html", {"users": users})


def view_project(request):

    # Retrieve current logged in user id
    user_id = request.COOKIES.get("user_id")

    if user_id is None:
        return redirect("login")

    project_id = request.session["current_project_id"]

    try:
        project_obj = Project.objects.get(project_id=project_id)
    except:
        raise Http404("Project does not exist")

    task_objs = Task.objects.filter(project__project_id = project_obj.project_id)

    completed_tasks = Task.objects.filter(project__project_id = project_obj.project_id, task_status = 2).count()
    review_tasks = Task.objects.filter(project__project_id = project_obj.project_id, task_status = 1).count()  
    progress_tasks = Task.objects.filter(project__project_id = project_obj.project_id, task_status = 0).count()

    if(completed_tasks != 0 and task_objs.count != 0):
        completed_tasks = (completed_tasks/task_objs.count()) * 100
    
    if(review_tasks != 0 and task_objs.count != 0):
        review_tasks = (review_tasks/task_objs.count()) * 100

    if(progress_tasks != 0 and task_objs.count != 0):
        progress_tasks = (progress_tasks / task_objs.count()) * 100

    start_to_now = (datetime.datetime.now().date() - project_obj.project_start).days

    if project_obj.project_end:
        end_to_now = (project_obj.project_end - datetime.datetime.now().date()).days
        start_to_end = (project_obj.project_end - project_obj.project_start).days
    else:
        end_to_now = 0
        start_to_end = 0
    
    if end_to_now < 0:
        start_to_now_percentage = 100
        end_to_now_percentage = 0
        start_to_now = start_to_end
    else:
        try:
            start_to_now_percentage = (start_to_now / start_to_end) * 100
        except:
            start_to_now_percentage = 0

        try:
            end_to_now_percentage = (end_to_now / start_to_end) * 100
        except:
            end_to_now_percentage = 0
        
    
    total_expenses = 0
    expense_objs = Expense.objects.filter(project_id=project_id)
    for expense in expense_objs:
        total_expenses = total_expenses + expense.expense_amt

    return render(request,
                  "view_project.html",
                  {"project": project_obj, "tasks": task_objs, "completed": completed_tasks ,
                   "review": review_tasks, "progress": progress_tasks, 
                   "start_to_now": start_to_now, "end_to_now": end_to_now,
                   "start_to_now_percentage": start_to_now_percentage,
                   "end_to_now_percentage": end_to_now_percentage,
                   "total_expenses": total_expenses
                   })


def update_project(request):

    # Retrieve current logged in user id
    user_id = request.COOKIES.get("user_id")

    if user_id is None:
        return redirect("login")

    project_id = request.session["current_project_id"]

    # Update project details when user clicks submit
    if (request.method == "POST"):
        # Get submitted form values
        project_name = request.POST.get("project_name")
        project_desc = request.POST.get("project_desc")
        project_start = request.POST.get("project_start")
        project_end = request.POST.get("project_end")
        project_status = request.POST.get("project_status")

        # Create and save the new project
        if project_end == "":
            project_end = None

        # Retrieve and edit the values of the project
        project_obj = Project.objects.get(project_id=project_id)

        project_obj.project_name = project_name
        project_obj.project_desc = project_desc
        project_obj.project_start = project_start
        project_obj.project_end = project_end
        project_obj.project_status = project_status

        project_obj.save()

        return redirect("view_project")

    # Otherwise, display the form
    else:
        try:
            project_obj = Project.objects.get(project_id=project_id)
        except:
            raise Http404("Project does not exist")

        return render(request,
                    "update_project.html",
                    {"project": project_obj})


def archive_project(request):

    # Retrieve current logged in user id
    user_id = request.COOKIES.get("user_id")

    if user_id is None:
        return redirect("login")

    project_id = request.session["current_project_id"]

    # Get project object
    try:
        project_obj = Project.objects.get(project_id=project_id)
    except:
        raise Http404("Project does not exist")

    # Toggle project status to "Archived" or "Finished"
    if project_obj.project_status != 2:
        project_obj.project_status = 2
    else:
        project_obj.project_status = 1
    project_obj.save()

    return redirect("view_project")


def delete_project(request):

    # Retrieve current logged in user id
    user_id = request.COOKIES.get("user_id")

    if user_id is None:
        return redirect("login")

    project_id = request.session["current_project_id"]

    # Get project object
    try:
        project_obj = Project.objects.get(project_id=project_id)
    except:
        raise Http404("Project does not exist")

    # Delete object
    project_obj.delete()

    return redirect("dashboard")


def create_task(request):
    # Retrieve current logged in user id
    user_id = request.COOKIES.get("user_id")

    if user_id is None:
        return redirect("login")

    # Create task when user clicks submit
    if (request.method == "POST"):

        # Get submitted form values
        task_name = request.POST.get("task_name")
        task_notes = request.POST.get("task_notes")
        task_priority = request.POST.get("task_priority")
        task_deadline = request.POST.get("task_deadline")
        members = request.POST.getlist('members')

        # Set deadline to None if not specified
        if task_deadline == "":
            task_deadline = None

        # Get current selected projected using the session variable
        current_project = Project.objects.get(project_id=request.session["current_project_id"])

        # Create the new task
        new_task = Task.objects.create(
            project=current_project,
            task_name=task_name,
            task_notes=task_notes,
            task_priority=task_priority,
            task_deadline=task_deadline
        )

        # Add assign members to task
        for member in members:
            member_obj = Member.objects.get(member_id=int(member))
            TaskAssignment.objects.create(task=new_task, member=member_obj)

        return redirect("dashboard")

    # Otherwise, redirect to dashboard 
    else:
        return redirect("dashboard")


def update_task(request, task_id):
    # Retrieve current logged in user id
    user_id = request.COOKIES.get("user_id")

    if user_id is None:
        return redirect("login")

    if (request.method == "POST"):

        # Get submitted form values
        status = request.POST.get("status")
        priority = request.POST.get("priority")
        notes = request.POST.get("notes")
        deadline = request.POST.get("deadline")
        new_members = [int(id) for id in request.POST.getlist('members')]

        # Set deadline to None if not specified
        if deadline == "":
            deadline = None

        # Get task object
        try:
            task_obj = Task.objects.get(task_id=task_id)
        except:
            raise Http404("Task does not exist")

        # Update object attributes
        task_obj.task_status = status
        task_obj.task_priority = priority
        task_obj.task_notes = notes
        task_obj.task_deadline = deadline
        task_obj.save()

        # Update members
        prev_members = Member.objects.filter(taskassignment__task=task_obj)

        # Remove members that has not been selected
        for member in prev_members:
            if member.member_id not in new_members:
                TaskAssignment.objects.get(task=task_obj, member=member).delete()
            else:
                new_members.remove(member.member_id)
        
        # Add new members
        for member in new_members:
            member_obj = Member.objects.get(member_id=member)
            TaskAssignment.objects.create(task=task_obj, member=member_obj)

        return redirect("dashboard")
    else:
        return redirect("dashboard")


def delete_task(request):
    # Retrieve current logged in user id
    user_id = request.COOKIES.get("user_id")

    if user_id is None:
        return redirect("login")

    if (request.method == "POST"):
        task_id = request.POST.get("task_id")

        # Get task object
        try:
            task_obj = Task.objects.get(task_id=task_id)
        except:
            raise Http404("Task does not exist")

        # Delete object
        task_obj.delete()

        return redirect("dashboard")
    else:
        return redirect("dashboard")


def view_members(request):
    # Retrieve current logged in user id
    user_id = request.COOKIES.get("user_id")

    if user_id is None:
        return redirect("login")

    # TODO: View member    project_id = request.session["current_project_id"]

    project_id = request.session["current_project_id"]

    # Get project object
    try:
        project_obj = Project.objects.get(project_id=project_id)
    except:
        raise Http404("Project does not exist")

    member_objs = Member.objects.filter(project__project_id = project_obj.project_id)

    return render(request, "view_members.html", {"project": project_obj, "members": member_objs})

def add_member(request):
    # Retrieve current logged in user id
    user_id = request.COOKIES.get("user_id")

    if user_id is None:
        return redirect("login")

    project_id = request.session["current_project_id"]
    if (request.method=="POST"):

        members = request.POST.getlist('member')

        #Get project object
        try:
            project_obj = Project.objects.get(project_id = project_id)
        except:
            raise Http404("Project does not exist")

        for member in members:
            new_user = User.objects.get(user_id = member)
            Member.objects.create(
                user = new_user,
                project = project_obj
            )
    
        return redirect("view_members")
    else:
        members = Member.objects.filter(project__project_id = project_id)  
        users = User.objects.exclude(staff_type="X").exclude(user_id__in = members.values_list('user__user_id'))
        return render(request, "add_member.html", {
            "users": users, "members": members 
        })
    

def remove_member(request, member_id):
    # Retrieve current logged in user id
    user_id = request.COOKIES.get("user_id")

    if user_id is None:
        return redirect("login")

    project_id = request.session["current_project_id"]

    #Get project object
    try: 
        project_obj = Project.objects.get(project_id = project_id)
    except:
        raise Http404("Project does not exist")

    member_obj = Member.objects.get(project__project_id = project_obj.project_id, member_id = member_id)
    member_obj.delete()
    return redirect("view_members")

def create_expense(request):
    # Retrieve current logged in user id
    user_id = request.COOKIES.get("user_id")

    if user_id is None:
        return redirect("login")

    # Create expense when user clicks submit
    if (request.method == "POST"):

        # Get submitted form values
        expense_date = request.POST.get("expense_date")
        expense_desc = request.POST.get("expense_desc")
        expense_amt = request.POST.get("expense_amt")

        # Get current user and selected projected using the session variable
        user_obj = User.objects.get(user_id=user_id)
        project_obj = Project.objects.get(project_id=request.session["current_project_id"])

        member_obj = Member.objects.get(project=project_obj, user=user_obj)

        # Create the new expense
        Expense.objects.create(
            project=project_obj,
            member=member_obj,
            expense_date=expense_date,
            expense_desc = expense_desc,
            expense_amt=expense_amt
        )

        return redirect("dashboard")

    # Otherwise, redirect to dashboard 
    else:
        return redirect("dashboard")


def update_expense(request, expense_id):

    # Retrieve current logged in user id
    user_id = request.COOKIES.get("user_id")

    if user_id is None:
        return redirect("login")

    if (request.method == "POST"):

        # Get submitted form values
        amount = request.POST.get("amount")
        desc = request.POST.get("desc")
        date = request.POST.get("date")

        # Set deadline to None if not specified
        if date == "":
            date = None

        # Get expense object
        try:
            expense_obj = Expense.objects.get(expense_id=expense_id)
        except:
            raise Http404("Expense does not exist")

        # Update object attributes
        expense_obj.expense_amt = amount
        expense_obj.expense_desc = desc
        expense_obj.expense_date = date
        expense_obj.save()

        return redirect("dashboard")
    else:
        return redirect("dashboard")


def delete_expense(request):
    
    # Retrieve current logged in user id
    user_id = request.COOKIES.get("user_id")

    if user_id is None:
        return redirect("login")

    if (request.method == "POST"):
        expense_id = request.POST.get("expense_id")

        # Get expense object
        try:
            expense_obj = Expense.objects.get(expense_id=expense_id)
        except:
            raise Http404("Expense does not exist")

        # Delete object
        expense_obj.delete()

        return redirect("dashboard")
    else:
        return redirect("dashboard")
