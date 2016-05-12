from django.contrib.auth.models import User, Group
from track.models import Bogger, CalorieEntry, DailyEntry, Goal
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

class DailyEntrySerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False)
    calories_consumed = serializers.ReadOnlyField()
    calories_expended = serializers.ReadOnlyField()

    class Meta:
        model = DailyEntry
        fields = (
            'bogger', 'date', 'calories_consumed', 'calories_expended', 'net_calories', 'calories_remaining'
        )

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = (
            'bogger', 'date', 'daily_weight_goal', 'dt_created'
        )



