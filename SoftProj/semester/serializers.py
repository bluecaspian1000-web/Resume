from rest_framework import serializers
from Student.models import StudentSemester


class StudentSemesterUnitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSemester
        fields = ['min_units', 'max_units']

    def validate(self, data):
        # اگه فقط یکیش ارسال شد از قبلی استفاده میکنه
        min_u = data.get('min_units', self.instance.min_units)
        max_u = data.get('max_units', self.instance.max_units)

        if min_u > max_u:
            raise serializers.ValidationError(
                "min_units cannot be greater than max_units"
            )

        return data

    

class StudentSemesterSerializer(serializers.ModelSerializer):
    def validate_term(self, value):
        if value not in (1, 2, 3):
            raise serializers.ValidationError("Invalid term")
        return value

