# hr_dashboard/serializers.py
from rest_framework import serializers
from .models import HiringRequest

class HiringRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = HiringRequest
        fields = '__all__'

