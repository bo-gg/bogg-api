import datetime

from django.test import TestCase
from django.contrib.auth.models import User

from track.models import Bogger, CalorieEntry, DailyEntry, Measurement

class BoggerTest(TestCase):
    def setUp(self):
        self.today = datetime.datetime.today()
        self.dude = User.objects.create(username='dude')
        self.bogger_dude = Bogger.objects.create(
            user=self.dude,
            gender='M',
            birthdate=datetime.datetime.now() - datetime.timedelta(days=365.25*35),
        )
        self.dude_measurement = Measurement.objects.create(
            bogger=self.bogger_dude,
            height=(6 * 12) + 2,    # 6'2"
            weight=180,
            activity_factor=1.2,
            daily_weight_goal=(2. / 7.),
            date=self.today,
        )

        self.chick = User.objects.create(username='chick')
        self.bogger_chick = Bogger.objects.create(
            user=self.chick,
            gender='F',
            birthdate=datetime.datetime.now() - datetime.timedelta(days=365.25*28),
        )
        self.chick_measurement = Measurement.objects.create(
            bogger=self.bogger_chick,
            height=(5 * 12) + 3,    # 5'3"
            weight=120,
            activity_factor=1.9,
            daily_weight_goal=(1. / 7.),
            date=self.today,
        )

    def test_readonly_fields(self):
        self.assertEqual(current_height, 72)
        self.assertEqual(current_weight, 180)
        self.assertEqual(current_activity_factor, 1.2)

    def test_calc_current_age(self):
        self.assertEqual(self.bogger_dude.current_age, 35)
        self.assertEqual(self.bogger_chick.current_age, 28)

    def test_calc_male_bmr(self):
        self.assertEqual(self.bogger_dude.current_bmr, 1889.2)

    def test_calc_female_bmr(self):
        self.assertEqual(self.bogger_chick.current_bmr, 1341.5)

    def test_calc_hbe(self):
        self.assertEqual(self.bogger_dude.hbe, 2267)
        self.assertEqual(self.bogger_chick.hbe, 2548)

    def test_calorie_goal(self):
        self.assertEqual(self.bogger_dude.calorie_goal, 1267)
        self.assertEqual(self.bogger_chick.calorie_goal, 2048)


class DailyEntryTest(TestCase):
    def setUp(self):
        self.dude = User.objects.create(username='dude')
        self.bogger_dude = Bogger.objects.create(user=self.dude, gender='M')
        self.bogger_dude.height = (6 * 12) + 2    # 6'2"
        self.bogger_dude.weight = 180
        self.bogger_dude.birthdate = datetime.datetime.now() - datetime.timedelta(days=365.25*35)
        self.bogger_dude.activity_factor = 1.2
        self.bogger_dude.daily_weight_goal = (2. / 7.)
        self.today = datetime.datetime.today()
        self.now = datetime.datetime.now()
        self.snack_entry = CalorieEntry.objects.create(
            bogger=self.bogger_dude,
            calories=300,
            dt_occurred=self.now,
            note='Silica gel',
            entry_type = CalorieEntry.CONSUMED
        )
        self.run_entry = CalorieEntry.objects.create(
            bogger=self.bogger_dude,
            calories=-100,
            dt_occurred=self.now,
            note='Ran from police',
            entry_type = CalorieEntry.EXPENDED
        )

    def test_daily_entry_creation(self):
        daily_entry = DailyEntry.objects.get(bogger=self.bogger_dude, date=self.today)
        self.assertEqual(300, daily_entry.calories_consumed)
        self.assertEqual(-100, daily_entry.calories_expended)
        self.assertEqual(200, daily_entry.net_calories)

