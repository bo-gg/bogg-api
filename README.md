<p align="center">
    <a><img src="static/img/bogg-logo.png" width="66%" title="bogg logo"/></a>

    <br>

    <b>bo.gg is an open source calorie tracker for nerds</b>

    <br>

</p>

I needed a dead simple way to log my activity and my calorie
intake.

[![Build Status](https://travis-ci.org/ben174/bogg.svg?branch=master)](https://travis-ci.org/ben174/bogg)

It is meant to make tracking your daily calorie intake simple.
-----------------------------------------------------------

Entering your data should be easy and dependable.
Otherwise, you won't do it.

* I'm always in the command line, I need a very quick way to say
  `bogg 350` to log that ham sandwich I had for lunch, or `bogg --exercise 400 bicycling`
  to log my bike ride.

* A great, simple API so I can write my own little utilities to
  log my activity from my activity trackers, or track my weight
  from my connected scale.

* Sometimes I'd like my hand held. A nice interactive console app
  guide me though backfilling data.

* A nice web UI to backfill data from my weekend and visualize my
  progress. (TODO)

Get Started
-----------

Install the `bogg-cli` application and simply run:

    bogg


Follow the interactive setup and you'll be ready to log via bogg.

    Choose a username: bogger
    Enter your email: bogger@bo.gg
    Choose a password: ****
    Confirm password: ****
    How many pounds do you want to lose per week? (Usually between 1.0 and 2.0): 2

    The following questions are only used to calculate your basic metabolic 
    rate and figure out how many calories you should be eating per day.

    Activity Level (https://en.wikipedia.org/wiki/Physical_activity_level)

        1. Sedentary
        2. Lightly Active
        3. Moderately Active
        4. Very Active
        5. Extra Active

    Enter your activity level: 2
    Gender (m/f): M
    Enter your birthdate (YYYY-MM-DD): 1988-11-23
    Enter your height (in inches): 72
    Enter your weight (in pounds): 150

    User: bogger created. Your daily calorie goal is: 2142.0

    You are now ready to start logging. Simply run 'bogg' from your command line
    to start logging!

Some commands:

#### Log 350 calories eaten

    bogg 350

#### Log 350 calories exercised via bike ride

    bogg --exercise 350 "bike ride"

Or use interactive mode:

    # bogg

    1: Log calories eaten.
    2: Log calories exercised.
    3: Record a new weight measurement.
    4: Log an item from your quick-lookups.
    5: Add an item to your quick-lookups.
    6: View status for today.
    7: View a log of the past few days.
    8: Edit configuration.

    ?: This menu.
    Q: Quit.

    Command? 1

    Number of calories: 300
    What did you eat?: sandwich
    Logged 300 calories.

       - You have eaten 1200 calories.
       - You have burned off 0 calories.

    You can eat 942.0 more calories today.


Completely Open, Completely Private
-----------------------------------

Your data is *your data*, I'm happy to host it, but this is an
open source application. You can export your data at any time and
run this very simple app on your own instance. But while It's in my
possession, you can be sure it's secure.

I won't charge you anything. I built this app for myself, and am
happy to host others' data. The cost of additional users is
negligible and I'm happy to help out the community.


Uptime is Critical
-------------------

More than anything, I believe in uptime. If this goes down, I know
I'll stop using it. As a systems architect for 15+ years, I know
how to keep a site up.

API
===


## Registration [/create]

### Register a New User [POST]

You may register a new user using this action. It requires a fully
populated JSON obect with valid data, and returns your new user instance, 
complete with calculated daily calorie goals and HBE.

+ Request (application/json)

        {
            "username": "ben16",
            "email": "ben189@gmail.com",
            "password": "balls",
            "daily_weight_goal": 0.2,
            "height": 72,
            "weight": 270,
            "activity_factor": 1.2,
            "bogger": {
                "gender": "M",
                "birthdate": "1985-11-23",
                "auto_update_goal": true
            }
        }
        
+ Response 201 (application/json)


    + Body
    
                 
            {
                "username": "ben16",
                "email": "ben189@gmail.com",
                "bogger": {
                    "user": "ben16",
                    "gender": "M",
                    "birthdate": "1985-11-23",
                    "auto_update_goal": true,
                    "height": 72.0,
                    "weight": 270.0,
                    "activity_factor": 1.2,
                    "daily_weight_goal": 0.2,
                    "current_age": 30,
                    "current_hbe": 2950,
                    "current_bmr": 2458.5,
                    "current_calorie_goal": 2250.0
                }
            }
   
## Calorie Entries [/entries]

### List All Calorie Entries [GET]

+ Response 200 (application/json)
    
            
        {
            "count": 1,
            "next": null,
            "previous": null,
            "results": [
                {
                    "entry_type": "C",
                    "calories": 300,
                    "note": "Silica Gel",
                    "dt_created": "2016-06-05T03:47:59.663Z",
                    "dt_occurred": "2016-06-05T03:47:58.159761Z",
                    "date": "2016-06-04"
                }
            ]
        }

### Create a New Calorie Entry [POST]

Create a new calorie entry using this action. `entry_type` must be either
`E` (Exercise) or `C` (Consumed). A note is required.

+ Request (application/json)

        {
            "entry_type": "E",
            "calories": 300,
            "note": "Ran from Police",
            "dt_occurred": "2016-06-05T03:47:58.159761Z"
        }

+ Response 201 (application/json)


    + Body
    
            {
                "entry_type": "E",
                "calories": 300,
                "note": "Ran from Police",
                "dt_created": "2016-06-06T03:51:24.785Z",
                "dt_occurred": "2016-06-05T03:47:58.159761Z",
                "date": "2016-06-05"
            }
            

## Daily Entries [/daily]

### Retrieve Daily Status Entries [GET]

A read-only endpoint to retrieve information on daily status. This includes
aggregated calorie vlues and calories remaining.

+ Response 201 (application/json)

    + Body
    
                  
            {
                "count": 2,
                "next": null,
                "previous": null,
                "results": [
                    {
                        "date": "2016-06-04",
                        "calories_consumed": 300,
                        "calories_expended": 0,
                        "net_calories": 300,
                        "calories_remaining": null
                    },
                    {
                        "date": "2016-06-05",
                        "calories_consumed": 0,
                        "calories_expended": 300,
                        "net_calories": 300,
                        "calories_remaining": null
                    }
                ]
            }
            
## Goal Entries [/goals]

### List All Goal Entries [GET]


Goals may change over time. Daily status should reflect the goal at the time
of the status. Just because I increased my daily weight loss goal today, 
shouldn't mean I failed on my goals for all previous days.


+ Response 200 (application/json)

        {
            "count": 1,
            "next": null,
            "previous": null,
            "results": [
                {
                    "date": "2016-06-05",
                    "daily_weight_goal": 0.28,
                    "dt_created": "2016-06-06T04:05:54.978Z"
                }
            ]
        }


### Create a New Goal Entry [POST]

Create a new goal using this action. The `daily_weight_goal` is in pounds,
but usually referred to by week. To calculate the daily goal, simply
divide the weekly goal by 7.

+ Request (application/json)

            {
                "date": "2016-06-05",
                "daily_weight_goal": 0.28,
                "dt_created": "2016-06-06T04:05:54.978Z"
            }

+ Response 201 (application/json)

    + Body
    
                               
            {
                "date": "2016-06-05",
                "daily_weight_goal": 0.28,
                "dt_created": "2016-06-06T04:05:54.978Z"
            }

