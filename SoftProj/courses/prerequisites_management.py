
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Course 


# POST add-prerequisite by course-ID in url
@api_view(["POST"])
def add_prerequisite(request, course_id, prereq_id):
    try:
        course = Course.objects.get(id=course_id)
        prereq = Course.objects.get(id=prereq_id)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=404)

    if course.id == prereq.id:
        return Response({"error": "A course cannot be prerequisite of itself"}, status=400)

    course.prerequisites.add(prereq)
    return Response({"message": "Prerequisite added"}, status=200)



# DELETE remove-prerequisite by course-ID in url
@api_view(["DELETE"])
def remove_prerequisite(request, course_id, prereq_id):
    try:
        course = Course.objects.get(id=course_id)
        prereq = Course.objects.get(id=prereq_id)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=404)

    course.prerequisites.remove(prereq)
    return Response({"message": "Prerequisite removed"}, status=200)


# POST add prerequisite by code in request
@api_view(["POST"])
def add_prerequisite_by_code(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=404)

    code = request.data.get("code")
    if not code:
        return Response({"error": "code is required"}, status=400)

    try:
        prereq = Course.objects.get(code=code)
    except Course.DoesNotExist:
        return Response({"error": "Prerequisite not found"}, status=404)

    if course.id == prereq.id:
        return Response({"error": "A course cannot be prerequisite of itself"}, status=400)

    course.prerequisites.add(prereq)
    return Response({"message": "Prerequisite added"}, status=200)


# POST remove prerequisite by code in request
@api_view(["POST"])
def remove_prerequisite_by_code(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=404)

    code = request.data.get("code")
    if not code:
        return Response({"error": "code is required"}, status=400)

    try:
        prereq = Course.objects.get(code=code)
    except Course.DoesNotExist:
        return Response({"error": "Prerequisite not found"}, status=404)

    course.prerequisites.remove(prereq)
    return Response({"message": "Prerequisite removed"}, status=200)