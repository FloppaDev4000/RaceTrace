from rest_framework import serializers
from .models import Race

# serializers to show all data
class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = "__all__"

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = "__all__"