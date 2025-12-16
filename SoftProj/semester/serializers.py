# serializers.py
from rest_framework import serializers
from .models import Semester

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['id', 'year', 'term', 'code', 'is_active']
        read_only_fields = ['code'] 
