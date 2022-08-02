import logging
from rest_framework import serializers
from .models import TeamMember,UserType
from django.contrib.auth.models import User


logger = logging.getLogger(__name__)

class TeamMemberStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = '__all__'

class TeamMemberDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = '__all__'
