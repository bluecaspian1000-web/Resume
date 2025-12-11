# courses/api_views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Course , CourseSchedule
from .serializers import CourseSerializer , CourseScheduleSerializer
from django.db.models import Q
from rest_framework import status


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
    

# Search course by name or prof
@api_view(['GET'])
def search_courses(request):
    course_name = request.GET.get('course_name', '')
    professor_name = request.GET.get('professor_name', '')

    queryset = Course.objects.all()

    if course_name:
        queryset = queryset.filter(name__icontains=course_name)

    if professor_name:
        queryset = queryset.filter(
            Q(professor__user__first_name__icontains=professor_name) |
            Q(professor__user__last_name__icontains=professor_name)
        )

    serializer = CourseSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Search course by name or prof (in a semester)
@api_view(['GET'])
def search_courses_by_semester(request):
    semester = request.GET.get('semester')
    course_name = request.GET.get('course_name', '')
    professor_name = request.GET.get('professor_name', '')

    if not semester:
        return Response(
            {"error": "semester parameter is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    queryset = CourseSchedule.objects.filter(semester=semester)

    if course_name:
        queryset = queryset.filter(name__icontains=course_name)

    if professor_name:
        queryset = queryset.filter(
            Q(professor__user__first_name__icontains=professor_name) |
            Q(professor__user__last_name__icontains=professor_name)
        )

    serializer = CourseScheduleSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# search courses by semester
@api_view(['GET'])
def list_courses_by_semester(request, semester):
    queryset = CourseSchedule.objects.filter(semester=semester)
    
    if not queryset.exists():
        return Response(
            {"error": f"No courses found for semester {semester}"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = CourseScheduleSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



