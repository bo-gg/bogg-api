def caclulate_bmr(gender, weight, height, age):
    '''
    BMR Formula
    Women: BMR = 655 + ( 4.35 x weight in pounds ) + ( 4.7 x height in inches ) - ( 4.7 x age in years )
    Men: BMR = 66 + ( 6.23 x weight in pounds ) + ( 12.7 x height in inches ) - ( 6.8 x age in year )
    '''
    ret = None
    if not weight and height and gender:
        logging.warning('Couldn\'t determine BMR because user profile is incomplete.')
        return None
    if gender == 'M':
        ret = 66 + (6.23 * weight) + (12.7 * height) - (6.8 * age)
    elif gender == 'F':
        ret = 655 + (4.35 * weight) + (4.7 * height) - (4.7 * age)
    else:
        raise ValueError('Unexpected gender: {}'.format(gender))
    return round(ret, 2)

def caclulate_hbe(bmr, activity_factor):
    ''' This is how many calories you expend per day. If you eat exactly this much
    you'll maintain your current weight. '''
    return int(bmr * activity_factor)

def calculate_calorie_goal(hbe, daily_weight_goal):
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
    return round(hbe - (daily_weight_goal * 3500))

def calculate_age(birthdate, date):
    return date.year - birthdate.year - ((date.month, date.day) < (birthdate.month, birthdate.day))
