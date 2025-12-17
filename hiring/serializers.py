# hr_dashboard/serializers.py
from .models import HiringRequisition, CandidateApplication, NewOnboarding, UpdateOnboarding

class HiringRequisitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HiringRequisition
        fields = '__all__'

class CandidateApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateApplication
        fields = '__all__'

class NewOnboardingSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewOnboarding
        fields = '__all__'

class UpdateOnboardingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpdateOnboarding
        fields = '__all__'
