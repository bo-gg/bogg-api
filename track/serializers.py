from django.contrib.auth.models import User, Group
from track.models import Bogger, CalorieEntry, DailyEntry, Goal
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    bogger = serializers.HyperlinkedRelatedField(queryset=Bogger.objects.all(), view_name='bogger', many=False)
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups', 'bogger')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class BoggerSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    height = serializers.ReadOnlyField(source='current_height')
    weight = serializers.ReadOnlyField(source='current_weight')
    activity_factor = serializers.ReadOnlyField(source='current_activity_factor')
    daily_weight_goal = serializers.ReadOnlyField(source='current_daily_weight_goal')

    class Meta:
        model = Bogger
        fields = (
            'user', 'gender', 'birthdate', 'auto_update_goal', 'height',
            'weight', 'activity_factor', 'daily_weight_goal'
        )

class CalorieEntrySerializer(serializers.ModelSerializer):
    bogger = BoggerSerializer(read_only=True)
    dt_created = serializers.ReadOnlyField()
    date = serializers.ReadOnlyField()

    class Meta:
        model = CalorieEntry
        fields = (
            'bogger', 'entry_type', 'calories', 'note', 'dt_created', 'dt_occurred', 'date'
        )

class DailyEntrySerializer(serializers.ModelSerializer):
    bogger = BoggerSerializer(read_only=True)

    class Meta:
        model = DailyEntry
        fields = (
            'bogger', 'date', 'calories_consumed', 'calories_expended', 'net_calories', 'calories_remaining'
        )

class GoalSerializer(serializers.ModelSerializer):
    bogger = BoggerSerializer(read_only=True)
    dt_created = serializers.ReadOnlyField()

    class Meta:
        model = Goal
        fields = (
            'bogger', 'date', 'daily_weight_goal', 'dt_created'
        )
