# courses/api_views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Course
from .serializers import CourseSerializer


# GET all courses
@api_view(['GET'])
def get_courses(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


# GET single course
@api_view(['GET'])
def get_course(request, id):
    try:
        course = Course.objects.get(id=id)
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=404)


# CREATE new course
@api_view(['POST'])
def create_course(request):
    serializer = CourseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


# UPDATE course
@api_view(['PUT'])
def update_course(request, id):
    try:
        course = Course.objects.get(id=id)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=404)


# DELETE course
@api_view(['DELETE'])
def delete_course(request, id):
    try:
        course = Course.objects.get(id=id)
        course.delete()
        return Response(status=204)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=404)



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

    course.prerequisties.add(prereq)
    return Response({"message": "Prerequisite added"}, status=200)



# DELETE remove-prerequisite by course-ID in url
@api_view(["DELETE"])
def remove_prerequisite(request, course_id, prereq_id):
    try:
        course = Course.objects.get(id=course_id)
        prereq = Course.objects.get(id=prereq_id)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=404)

    course.prerequisties.remove(prereq)
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

    course.prerequisties.add(prereq)
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

    course.prerequisties.remove(prereq)
    return Response({"message": "Prerequisite removed"}, status=200)





