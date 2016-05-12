from django.contrib.auth.models import User, Group
from track.models import Bogger, CalorieEntry
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class BoggerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bogger
        fields = (
            'user', 'gender', 'birthdate', 'auto_update_goal', 'current_height',
            'current_weight', 'current_activity_factor', 'current_daily_weight_goal'
        )

class CalorieEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CalorieEntry
        fields = (
            'bogger', 'entry_type', 'calories', 'note', 'dt_created', 'dt_occurred', 'date'
        )
