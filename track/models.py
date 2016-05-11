from __future__ import unicode_literals

import logging

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from datetime import date

from util import formulas


class Choices:
    # gender
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    # activity factor
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

    # calorie entry type
    CONSUMED = 'C'
    EXPENDED = 'E'
    CALORIE_ENTRY_TYPE_CHOICES = (
        (CONSUMED, 'Consumed (Eaten)'),
        (EXPENDED, 'Expended (Exercise)'),
    )

class Bogger(models.Model):
    ''' A bogg user '''

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=Choices.GENDER_CHOICES, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    auto_update_goal = models.BooleanField(default=True)

    # read only fields
    current_height = models.DecimalField(help_text="Height in Inches", decimal_places=2, max_digits=5, null=True, blank=True)
    current_weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    current_activity_factor = models.DecimalField(max_digits=4, decimal_places=3, choices=Choices.ACTIVITY_FACTOR_CHOICES, null=True, blank=True)

    current_daily_weight_goal = models.DecimalField(decimal_places=5, max_digits=7, null=True, blank=True)

    current_calorie_goal = models.IntegerField(null=True, blank=True)

    @property
    def current_age(self):
        if not self.birthdate:
            logger.warning('Unable to calculate age because no birthdate specified.')
            return None
        today = date.today()
        return formulas.calculate_age(self.birthdate, today)

    @property
    def current_hbe(self):
        return formulas.caclulate_hbe(self.current_bmr, self.current_activity_factor)

    @property
    def current_bmr(self):
        return formulas.caclulate_bmr(self.gender, self.current_weight, self.current_height)



class CalorieEntry(models.Model):
    bogger = models.ForeignKey(Bogger, null=False, blank=False)
    entry_type = models.CharField(max_length=1, default=Choices.CONSUMED, choices=Choices.CALORIE_ENTRY_TYPE_CHOICES)
    calories = models.IntegerField()
    note = models.CharField(max_length=255)
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_occurred = models.DateTimeField(null=False, blank=False)
    date = models.DateField(null=False, blank=False) # auto calculated

    def save(self, *args, **kwargs):
        self.date = instance.dt_occurred.date()
        super(Blog, self).save(*args, **kwargs) # Call the "real" save() method.



@receiver(pre_save, sender=CalorieEntry)
def update_daily(sender, **kwargs):
    instance = kwargs['instance']
    daily_entry, created = DailyEntry.objects.get_or_create(date=instance.date, bogger=instance.bogger)
    if created:
        # is there a DailyEntry more recent than this one which has a weight value? if so, don't enter a weight
        pass
    if kwargs['instance'].entry_type == CalorieEntry.CONSUMED:
        daily_entry.calories_consumed += instance.calories
    elif kwargs['instance'].entry_type == CalorieEntry.EXPENDED:
        daily_entry.calories_expended += instance.calories
    daily_entry.save()


class Measurement(models.Model):
    '''
    Activity Factor
    If you are sedentary (little or no exercise) : Calorie-Calculation = BMR x 1.2
    If you are lightly active (light exercise/sports 1-3 days/week) : Calorie-Calculation = BMR x 1.375
    If you are moderatetely active (moderate exercise/sports 3-5 days/week) : Calorie-Calculation = BMR x 1.55
    If you are very active (hard exercise/sports 6-7 days a week) : Calorie-Calculation = BMR x 1.725
    If you are extra active (very hard exercise/sports & physical job or 2x training) : Calorie-Calculation = BMR x 1.9`
    '''
    bogger = models.ForeignKey(Bogger, null=False, blank=False)
    date = models.DateField(null=False, blank=False)

    height = models.DecimalField(help_text="Height in Inches", decimal_places=2, max_digits=5, null=True, blank=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    activity_factor = models.DecimalField(max_digits=4, decimal_places=3, null=True, blank=True)
    bmr = models.IntegerField(help_text="BMR", null=True, blank=True)
    daily_weight_goal = models.DecimalField(decimal_places=5, max_digits=7, null=True, blank=True)

    calorie_goal = models.IntegerField(null=True, blank=True)

    dt_created = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_measurement_for_date(cls, bogger, date):
        latest_mesurement = cls.objects.filter(bogger=bogger, date__lte=date).latest('date')
        return latest_measurement


@receiver(post_save, sender=Measurement)
def update_bogger(sender, **kwargs):
    instance = kwargs['instance']
    # if this is the most recent instance
    bogger = instance.bogger
    today = date.today()
    measurement = Measurement.get_measurement_for_date(today, bogger)
    bogger.current_height = measurement.height
    bogger.current_weight = measurement.weight
    bogger.current_activity_factor = measurement.activity_factor
    bogger.current_bmr = measurement.bmr
    bogger.current_daily_weight_goal = measurement.daily_weight_goal
    bogger.current_calorie_goal = measurement.calorie_goal

    daily_entry, created = DailyEntry.objects.get_or_create(date=instance.date, bogger=instance.bogger)
    if created:
        # is there a DailyEntry more recent than this one which has a weight value? if so, don't enter a weight
        pass
    if kwargs['instance'].entry_type == CalorieEntry.CONSUMED:
        daily_entry.calories_consumed += instance.calories
    elif kwargs['instance'].entry_type == CalorieEntry.EXPENDED:
        daily_entry.calories_expended += instance.calories
    daily_entry.save()


class DailyEntry(models.Model):
    bogger = models.ForeignKey(Bogger, null=False, blank=False)
    date = models.DateField(null=False, blank=False)

    # read only
    calories_consumed = models.IntegerField(default=0)
    calories_expended = models.IntegerField(default=0)

    @property
    def net_calories(self):
        return self.calories_consumed + self.calories_expended

    @property
    def calories_remaining(self):
        return self.net_calories - self.calorie_goal

    class Meta:
        unique_together = ('bogger', 'date')

