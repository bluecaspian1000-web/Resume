
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Course 
from .serializers import PrerequisiteSerializer

# POST add prerequisite by code in request
@api_view(["POST"])
def add_prerequisite_by_code(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=404)

    serializer = PrerequisiteSerializer(
        data=request.data,
        context={"course": course, "mode": "add"}
    )
    serializer.is_valid(raise_exception=True)

    prereq = serializer.validated_data["prereq"]
    course.prerequisites.add(prereq)

    return Response({"message": "Prerequisite added"}, status=200)


# POST remove prerequisite by code in request
@api_view(["POST"])
def remove_prerequisite_by_code(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=404)

    serializer = PrerequisiteSerializer(
        data=request.data,
        context={"course": course, "mode": "remove"}
    )
    serializer.is_valid(raise_exception=True)

    prereq = serializer.validated_data["prereq"]
    course.prerequisites.remove(prereq)

    return Response({"message": "Prerequisite removed"}, status=200)
