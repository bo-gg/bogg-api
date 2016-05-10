from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class BoggUser(models.Model):
    # gender
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    # activity

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    calorie_goal = models.IntegerField(null=True, blank=True)
    auto_update_goal = models.BooleanField(default=True)
    height = models.IntegerField(help_text="Height in Inches", null=True, blank=True)
    activity_factor = models.DecimalField(max_digits=4, decimal_places=3, null=True, blank=True)

    '''
    BMR Formula
    Women: BMR = 655 + ( 4.35 x weight in pounds ) + ( 4.7 x height in inches ) - ( 4.7 x age in years )
    Men: BMR = 66 + ( 6.23 x weight in pounds ) + ( 12.7 x height in inches ) - ( 6.8 x age in year )
    '''

    '''
    Activity Factor
    If you are sedentary (little or no exercise) : Calorie-Calculation = BMR x 1.2
    If you are lightly active (light exercise/sports 1-3 days/week) : Calorie-Calculation = BMR x 1.375
    If you are moderatetely active (moderate exercise/sports 3-5 days/week) : Calorie-Calculation = BMR x 1.55
    If you are very active (hard exercise/sports 6-7 days a week) : Calorie-Calculation = BMR x 1.725
    If you are extra active (very hard exercise/sports & physical job or 2x training) : Calorie-Calculation = BMR x 1.9`
    '''

class ConsumptionEntry(models.Model):
    calories = models.IntegerField()
    note = models.CharField(max_length=255)
    dt_created = model.DateTimeField(auto_now_add=True)
    dt_occurred = model.DateTimeField(null=False, blank=False)

class ExerciseEntry(models.Model):
    calories = models.IntegerField()
    note = models.CharField(max_length=255)
    dt_created = model.DateTimeField(auto_now_add=True)
    dt_occurred = model.DateTimeField(null=False, blank=False)

class WeightEntry(models.Model):
    calories = models.IntegerField()
    dt_created = model.DateTimeField(auto_now_add=True)
    dt_occurred = model.DateTimeField(null=False, blank=False)
    calorie_goal = models.IntegerField(null=True, blank=True)
