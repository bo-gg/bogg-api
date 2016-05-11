from __future__ import unicode_literals

import logging

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from datetime import date


class Bogger(models.Model):
    ''' A bogg user '''
    # gender
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    # activity factor
    '''
    Activity Factor
    If you are sedentary (little or no exercise) : Calorie-Calculation = BMR x 1.2
    If you are lightly active (light exercise/sports 1-3 days/week) : Calorie-Calculation = BMR x 1.375
    If you are moderatetely active (moderate exercise/sports 3-5 days/week) : Calorie-Calculation = BMR x 1.55
    If you are very active (hard exercise/sports 6-7 days a week) : Calorie-Calculation = BMR x 1.725
    If you are extra active (very hard exercise/sports & physical job or 2x training) : Calorie-Calculation = BMR x 1.9`
    '''
    SEDENTARY = '1.2'
    LIGHTLY_ACTIVE = '1.375'
    MODERATELY_ACTIVE = '1.55'
    VERY_ACTIVE = '1.725'
    EXTRA_ACTIVE = '1.9'
    ACTIVITY_FACTOR_CHOICES = (
        (SEDENTARY, 'Sedentary'),
        (LIGHTLY_ACTIVE, 'Lightly Active'),
        (MODERATELY_ACTIVE, 'Moderately Active'),
        (VERY_ACTIVE, 'Very Active'),
        (EXTRA_ACTIVE, 'Extra Active'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    auto_update_goal = models.BooleanField(default=True)
    height = models.DecimalField(help_text="Height in Inches", decimal_places=2, max_digits=5, null=True, blank=True)
    activity_factor = models.DecimalField(max_digits=4, decimal_places=3, null=True, blank=True)
    bmr = models.IntegerField(help_text="BMR", null=True, blank=True)
    daily_weight_goal = models.DecimalField(decimal_places=5, max_digits=7, null=True, blank=True)

    @property
    def age(self):
        today = date.today()
        return today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))

    @property
    def bmr(self):
        '''
        BMR Formula
        Women: BMR = 655 + ( 4.35 x weight in pounds ) + ( 4.7 x height in inches ) - ( 4.7 x age in years )
        Men: BMR = 66 + ( 6.23 x weight in pounds ) + ( 12.7 x height in inches ) - ( 6.8 x age in year )
        '''
        ret = None
        if not self.weight and self.height and self.gender:
            logging.warning('Couldn\'t determine BMR because user profile is incomplete.')
            return None
        if self.gender == 'M':
            ret = 66 + (6.23 * self.weight) + (12.7 * self.height) - (6.8 * self.age)
        elif self.gender == 'F':
            ret = 655 + (4.35 * self.weight) + (4.7 * self.height) - (4.7 * self.age)
        else:
            raise ValueError('Unexpected gender: {}'.format(self.gender))
        return round(ret, 2)

    @property
    def hbe(self):
        ''' This is how many calories you expend per day. If you eat exactly this much
        you'll maintain your current weight. '''
        bmr = self.bmr
        if not bmr and self.activity_factor:
            logging.warning('Couldn\'t determine BMR because user profile is incomplete.')
            return None
        return int(bmr * self.activity_factor)

    @property
    def calorie_goal(self):
        '''
        There are approximately 3500 calories in a pound of stored body fat. So, if
        you create a 3500-calorie deficit through diet, exercise or a combination
        of both, you will lose one pound of body weight. (On average 75% of this is
        fat, 25% lean tissue) If you create a 7000 calorie deficit you will lose
        two pounds and so on. The calorie deficit can be achieved either by
        calorie-restriction alone, or by a combination of fewer calories in (diet)
        and more calories out (exercise). This combination of diet and exercise is
        best for lasting weight loss. Indeed, sustained weight loss is difficult or
        impossible without increased regular exercise.
        '''
        if not self.daily_weight_goal:
            logging.warning('Couldn\'t determine BMR because user profile is incomplete.')
            return None
        return self.hbe - (self.daily_weight_goal * 3500)



class CalorieEntry(models.Model):
    # entry type
    CONSUMED = 'C'
    EXPENDED = 'E'
    CALORIE_ENTRY_TYPE_CHOICES = (
        (CONSUMED, 'Consumed (Eaten)'),
        (EXPENDED, 'Expended (Exercise)'),
    )
    bogger = models.ForeignKey(Bogger, null=False, blank=False)
    entry_type = models.CharField(max_length=1, default=CONSUMED, choices=CALORIE_ENTRY_TYPE_CHOICES)
    calories = models.IntegerField()
    note = models.CharField(max_length=255)
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_occurred = models.DateTimeField(null=False, blank=False)

@receiver(pre_save, sender=CalorieEntry)
def update_daily(sender, **kwargs):
    instance = kwargs['instance']
    daily_entry, _ = DailyEntry.objects.get_or_create(date=instance.dt_occurred.date(), bogger=instance.bogger)
    if kwargs['instance'].entry_type == CalorieEntry.CONSUMED:
        daily_entry.calories_consumed += instance.calories
    elif kwargs['instance'].entry_type == CalorieEntry.EXPENDED:
        daily_entry.calories_expended += instance.calories
    daily_entry.save()



class DailyEntry(models.Model):
    bogger = models.ForeignKey(Bogger, null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    calories_consumed = models.IntegerField(default=0)
    calories_expended = models.IntegerField(default=0)
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    @property
    def net_calories(self):
        return self.calories_consumed + self.calories_expended

    class Meta:
        unique_together = ('bogger', 'date')
