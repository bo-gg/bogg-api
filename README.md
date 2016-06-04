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


