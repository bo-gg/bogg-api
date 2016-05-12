from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User

from track.models import Choices, Bogger, CalorieEntry, DailyEntry, Measurement, Goal

class BoggerTest(TestCase):
    def setUp(self):
        self.today = timezone.now().date()
        self.dude = User.objects.create(username='dude')
        self.bogger_dude = Bogger.objects.create(
            user=self.dude,
            gender='M',
            birthdate=timezone.now() - timedelta(days=365.25*35),
        )
        self.dude_goal = Goal.objects.create(
            bogger=self.bogger_dude,
            date=self.today,
            daily_weight_goal=(2. / 7.),
        )
        self.dude_measurement = Measurement.objects.create(
            bogger=self.bogger_dude,
            date=self.today,
            height=(6 * 12) + 2,    # 6'2"
            weight=180,
            activity_factor=1.2,
        )

        self.chick = User.objects.create(username='chick')
        self.bogger_chick = Bogger.objects.create(
            user=self.chick,
            gender='F',
            birthdate=timezone.now() - timedelta(days=365.25*28),
        )
        self.chick_goal = Goal.objects.create(
            bogger=self.bogger_chick,
            date=self.today,
            daily_weight_goal=(1. / 7.),
        )
        self.chick_measurement = Measurement.objects.create(
            bogger=self.bogger_chick,
            date=self.today,
            height=(5 * 12) + 3,    # 5'3"
            weight=120,
            activity_factor=1.9,
        )

    def test_readonly_fields(self):
        self.assertEqual(self.bogger_dude.current_height, (6 * 12) + 2)
        self.assertEqual(self.bogger_dude.current_weight, 180)
        self.assertEqual(self.bogger_dude.current_activity_factor, 1.2)

    def test_calc_current_age(self):
        self.assertEqual(self.bogger_dude.current_age, 35)
        self.assertEqual(self.bogger_chick.current_age, 28)

    def test_calc_male_bmr(self):
        self.assertEqual(self.bogger_dude.current_bmr, 1889.2)

    def test_calc_female_bmr(self):
        self.assertEqual(self.bogger_chick.current_bmr, 1341.5)

    def test_calc_hbe(self):
        self.assertEqual(self.bogger_dude.current_hbe, 2267)
        self.assertEqual(self.bogger_chick.current_hbe, 2548)

    def test_calorie_goal(self):
        self.assertEqual(self.bogger_dude.current_calorie_goal, 1267)
        self.assertEqual(self.bogger_chick.current_calorie_goal, 2048)

class MeasurementTest(TestCase):
    def setUp(self):
        self.today = timezone.now().date()
        self.dude = User.objects.create(username='dude')
        self.bogger = Bogger.objects.create(
            user=self.dude,
            gender='M',
            birthdate=timezone.now() - timedelta(days=365.25*35),
        )
        self.old_measurement = Measurement.objects.create(
            bogger=self.bogger,
            date=self.today - timedelta(days=7),
            height=(6 * 12) + 2,    # 6'2"
            weight=180,
            activity_factor=1.2,
        )

    def test_measurement(self):
        self.assertEqual(self.bogger.current_weight, 180)

    def test_measurement_update(self):
        self.assertEqual(self.bogger.current_weight, self.old_measurement.weight)
        new_weight = 175
        new_measurement = Measurement.objects.create(
            bogger=self.bogger,
            date=self.today,
            height=(6 * 12) + 2,    # 6'2"
            weight=new_weight,
            activity_factor=1.2,
        )
        self.assertEqual(self.bogger.current_weight, new_weight)

    def test_get_measurement_for_date(self):
        new_measurement = Measurement.objects.create(
            bogger=self.bogger,
            date=self.today,
            height=(6 * 12) + 2,    # 6'2"
            weight=175,
            activity_factor=1.2,
        )
        measurement = Measurement.get_measurement_for_date(
            self.bogger,
            self.today-timedelta(days=6)
        )
        self.assertEqual(measurement.weight, 180)


class GoalTest(TestCase):
    def setUp(self):
        self.today = timezone.now().date()
        self.dude = User.objects.create(username='dude')
        self.bogger = Bogger.objects.create(
            user=self.dude,
            gender='M',
            birthdate=timezone.now() - timedelta(days=365.25*35),
        )
        self.old_measurement = Measurement.objects.create(
            bogger=self.bogger,
            date=self.today - timedelta(days=7),
            height=(6 * 12) + 2,    # 6'2"
            weight=180,
            activity_factor=1.2,
        )
        self.old_goal = Goal.objects.create(
            bogger=self.bogger,
            date=self.today - timedelta(days=7),
            daily_weight_goal=(2. / 7.),
        )

    def test_calorie_goal(self):
        self.assertEqual(self.bogger.current_calorie_goal, 1267)

    def test_goal_update(self):
        new_goal = Goal.objects.create(
            bogger=self.bogger,
            date=self.today,
            daily_weight_goal=(1. / 7.),
        )
        # should expect to eat more than before lowering goal
        self.assertTrue(self.bogger.current_calorie_goal > 1267)

    def test_old_goal(self):
        new_goal = Goal.objects.create(
            bogger=self.bogger,
            date=self.today,
            daily_weight_goal=(1. / 7.),
        )
        old_goal = Goal.get_goal_for_date(self.bogger, self.today - timedelta(days=6))
        # should expect to eat more than before lowering goal
        self.assertTrue(old_goal.calorie_goal < new_goal.calorie_goal)


class DailyEntryTest(TestCase):
    def setUp(self):
        self.dude = User.objects.create(username='dude')
        self.bogger_dude = Bogger.objects.create(user=self.dude, gender='M')
        self.snack_entry = CalorieEntry.objects.create(
            bogger=self.bogger_dude,
            calories=300,
            dt_occurred=timezone.now(),
            note='Silica gel',
            entry_type = Choices.CONSUMED
        )
        self.run_entry = CalorieEntry.objects.create(
            bogger=self.bogger_dude,
            calories=-100,
            dt_occurred=timezone.now(),
            note='Ran from police',
            entry_type = Choices.EXPENDED
        )

    def test_daily_entry_creation(self):
        daily_entry = DailyEntry.objects.get(bogger=self.bogger_dude, date=timezone.now().date())
        self.assertEqual(300, daily_entry.calories_consumed)
        self.assertEqual(-100, daily_entry.calories_expended)
        self.assertEqual(200, daily_entry.net_calories)
