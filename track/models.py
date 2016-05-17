from __future__ import unicode_literals

import logging

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone

from util import formulas


logger = logging.getLogger(__name__)


class Choices:
    # gender
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    # activity factor
    SEDENTARY = 1.2
    LIGHTLY_ACTIVE = 1.375
    MODERATELY_ACTIVE = 1.55
    VERY_ACTIVE = 1.725
    EXTRA_ACTIVE = 1.9
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

    # read only fields (set by creating a new Measurement)
    current_height = models.FloatField(help_text="Height in Inches", null=True, blank=True)
    current_weight = models.FloatField(null=True, blank=True)
    current_activity_factor = models.FloatField(choices=Choices.ACTIVITY_FACTOR_CHOICES, null=True, blank=True)
    current_daily_weight_goal = models.FloatField(null=True, blank=True)

    @property
    def current_age(self):
        if not self.birthdate:
            logger.warning('Unable to calculate age because no birthdate specified.')
            return None
        today = timezone.now().date()
        return formulas.calculate_age(self.birthdate, today)

    @property
    def current_hbe(self):
        return formulas.caclulate_hbe(self.current_bmr, self.current_activity_factor)

    @property
    def current_bmr(self):
        return formulas.caclulate_bmr(self.gender, self.current_weight, self.current_height, self.current_age)

    @property
    def current_calorie_goal(self):
        return formulas.calculate_calorie_goal(self.current_hbe, self.current_daily_weight_goal)

    def __unicode__(self):
        return str(self.user)

@receiver(post_save, sender=User)
def user_creates_bogger(sender, **kwargs):
    instance = kwargs['instance']
    if not hasattr(instance, 'bogger'):
        Bogger.objects.create(user=instance)


class CalorieEntry(models.Model):
    bogger = models.ForeignKey(Bogger, null=False, blank=False)
    entry_type = models.CharField(max_length=1, default=Choices.CONSUMED, choices=Choices.CALORIE_ENTRY_TYPE_CHOICES)
    calories = models.IntegerField()
    note = models.CharField(max_length=255)
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_occurred = models.DateTimeField(null=False, blank=False)
    date = models.DateField(null=False, blank=False) # auto calculated

    def __unicode__(self):
        cals = str(self.calories)
        if self.entry_type == Choices.EXPENDED:
            cals = '-' + cals

        ret = '{}: {}'.format(str(self.bogger.user), cals)
        if self.note:
            ret += ' ' + self.note
        return ret

    def save(self, *args, **kwargs):
        self.date = self.dt_occurred.date()
        super(CalorieEntry, self).save(*args, **kwargs) # Call the "real" save() method.

    class Meta:
        get_latest_by = 'dt_occurred'
        verbose_name = 'Calorie Entry'
        verbose_name_plural = 'Calorie Entries'


@receiver(pre_save, sender=CalorieEntry)
def update_daily(sender, **kwargs):
    instance = kwargs['instance']
    daily_entry, _ = DailyEntry.objects.get_or_create(date=instance.date, bogger=instance.bogger)
    if kwargs['instance'].entry_type == Choices.CONSUMED:
        daily_entry.calories_consumed += instance.calories
    elif kwargs['instance'].entry_type == Choices.EXPENDED:
        daily_entry.calories_expended += instance.calories
    daily_entry.save()


class Goal(models.Model):
    bogger = models.ForeignKey(Bogger, null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    daily_weight_goal = models.FloatField(null=True, blank=True)
    dt_created = models.DateTimeField(auto_now_add=True)

    @property
    def calorie_goal(self):
        try:
            measurement = Measurement.get_measurement_for_date(self.bogger, self.date)
        except Measurement.DoesNotExist:
            return None
        return formulas.calculate_calorie_goal(measurement.hbe, self.daily_weight_goal)

    @classmethod
    def get_goal_for_date(cls, bogger, goal_date):
        latest_goal = cls.objects.filter(bogger=bogger, date__lte=goal_date).latest()
        return latest_goal

    def __unicode__(self):
        ret = '{}: {}'.format(str(self.bogger.user), str(self.date))
        return ret

    class Meta:
        get_latest_by = 'date'
        unique_together = ('bogger', 'date')


@receiver(post_save, sender=Goal)
def goal_updates_bogger(sender, **kwargs):
    instance = kwargs['instance']
    bogger = instance.bogger
    latest_goal = Goal.objects.filter(bogger=instance.bogger).latest()
    bogger.current_daily_weight_goal = latest_goal.daily_weight_goal
    bogger.save()



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

    height = models.FloatField(help_text="Height in Inches", null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    activity_factor = models.FloatField(choices=Choices.ACTIVITY_FACTOR_CHOICES, null=True, blank=True)

    dt_created = models.DateTimeField(auto_now_add=True)

    @property
    def age(self):
        ''' Age at the time the measurement was taken. '''
        return formulas.calculate_age(self.bogger.birthdate, self.date)

    @property
    def hbe(self):
        return formulas.caclulate_hbe(self.bmr, self.activity_factor)

    @property
    def bmr(self):
        return formulas.caclulate_bmr(self.bogger.gender, self.weight, self.height, self.age)

    @classmethod
    def get_measurement_for_date(cls, bogger, measurement_date):
        latest_measurement = cls.objects.filter(bogger=bogger, date__lte=measurement_date).latest()
        return latest_measurement

    def __unicode__(self):
        ret = '{}: {}'.format(str(self.bogger.user), str(self.date))
        return ret

    class Meta:
        get_latest_by = 'date'
        unique_together = ('bogger', 'date')


@receiver(post_save, sender=Measurement)
def measurement_updates_bogger(sender, **kwargs):
    instance = kwargs['instance']
    bogger = instance.bogger
    latest_measurement = Measurement.objects.filter(bogger=bogger).latest()
    bogger.current_height = latest_measurement.height
    bogger.current_weight = latest_measurement.weight
    bogger.current_activity_factor = latest_measurement.activity_factor


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

    def __unicode__(self):
        ret = '{}: {}'.format(str(self.bogger.user), str(self.date))
        return ret

    class Meta:
        unique_together = ('bogger', 'date')
        get_latest_by = 'date'
        verbose_name = 'Daily Entry'
        verbose_name_plural = 'Daily Entries'
