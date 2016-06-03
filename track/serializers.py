from django.contrib.auth.models import User, Group
from django.utils import timezone
from track.models import Bogger, CalorieEntry, DailyEntry, Goal, Measurement
from rest_framework import serializers



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
            'weight', 'activity_factor', 'daily_weight_goal',
            'current_age', 'current_hbe', 'current_bmr', 'current_calorie_goal',
        )

class UserSerializer(serializers.HyperlinkedModelSerializer):
    bogger = BoggerSerializer(many=False)
    height = serializers.IntegerField(write_only=True)
    weight = serializers.IntegerField(write_only=True)
    activity_factor = serializers.DecimalField(max_digits=4, decimal_places=3, write_only=True)
    daily_weight_goal = serializers.DecimalField(max_digits=4, decimal_places=3, write_only=True)

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()

        bogger_data = validated_data['bogger']
        user.bogger.gender = bogger_data['gender']
        user.bogger.birthdate = bogger_data['birthdate']
        user.bogger.auto_update_goal = bogger_data['auto_update_goal']
        user.bogger.save()

        Measurement.objects.create(
            bogger=user.bogger,
            height=validated_data['height'],
            weight=validated_data['weight'],
            activity_factor=validated_data['activity_factor'],
            date=timezone.now().date(),
        )

        Goal.objects.create(
            bogger=user.bogger,
            daily_weight_goal=validated_data['daily_weight_goal'],
            date=timezone.now().date(),
        )

        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'bogger', 'height', 'weight',
                  'activity_factor', 'daily_weight_goal')
        write_only_fields = ('password', 'height', 'weight', 'activity_factor', 'daily_weight_goal')


class CalorieEntrySerializer(serializers.ModelSerializer):
    dt_created = serializers.ReadOnlyField()
    date = serializers.ReadOnlyField()

    class Meta:
        model = CalorieEntry
        fields = (
            'entry_type', 'calories', 'note', 'dt_created', 'dt_occurred', 'date'
        )

class DailyEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyEntry
        fields = (
            'date', 'calories_consumed', 'calories_expended', 'net_calories',
            'calories_remaining',
        )

class GoalSerializer(serializers.ModelSerializer):
    dt_created = serializers.ReadOnlyField()

    class Meta:
        model = Goal
        fields = (
            'date', 'daily_weight_goal', 'dt_created'
        )
