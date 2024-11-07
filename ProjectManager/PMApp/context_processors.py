from .models import Project, User


def projects_processor(request):

    # Validate and retrieve current logged in user id
    user_id = request.COOKIES.get("user_id")
    if user_id is None:
        return {"projects": None}

    # Retrieve user obj
    user_obj = User.objects.get(user_id=user_id)

    # If manager/employee, get all projects the user is part of
    # If executive, get all projects
    if user_obj.staff_type != "X":
        project_objs = Project.objects.filter(member__user=user_obj)
    else:
        project_objs = Project.objects.all()

    return {"projects": project_objs, "user": user_obj}