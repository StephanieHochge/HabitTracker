# My Habit Tracker Project

The habit tracker can be used to monitor and manage habits by enabling the user to define habits of different types and to document their execution at any point in time. After a habit is first completed, it is also possible to display useful statistics for that habit that can help and motivate the user to complete the habit more often. By providing login and register functionalities, It is also possible to manage the habits of several users. 

## What is it?

With the habit tracker, it is possible to monitor and manage your habits. For this purpose, four different types/periodicities of habits are available for selection:
- Daily habits: habits that a user wants to perform once a day)
- Weekly habits: habits that a user wants to perform once per calendar week (from Monday to Sunday)
- Monthly habits: habits that a user wants to perform once per calendar month (from the first day of a month to the last day)
- Yearly habits: habits that a user wants to perform once per calendar year

With the application, it is possible to analyze the defined habits by answering the following questions you might have:
- What is my current streak, i.e., the number of consecutive time periods (e.g., days for daily habits) in which I completed the habit? 
- What is my best streak? 
- When did I complete the habit last? 
- What is the percentage of time periods in the last four weeks in which I completed the habit, i.e., what is my completion rate for this habit? (only available for daily and weekly habits)
- How often did I break the habit? 

It is also possible to compare these statistics for all habits:
- What is my longest streak over all habits? 
- Which habit is my best habit, i.e., the habit with the longest streak? 
- What is my lowest completion rate over all habits? 
- Which habit is my worst habit, i.e., the habit with the lowest completion rate?

## Installation

- fork and clone the repo

```shell
git clone https://github.com/yourgithubusername/habitist-streak
```

```shell
pip install -r requirements.txt
```

## Usage

Start the habit tracker:

```shell
python main.py
```

and follow instructions on screen. 

After starting the app you will first be presented with the welcome screen, where you will have the option to either login or create a new user. When first using the app, you will need to create a new user to be able to login. Once you have chosen a valid username, you are automatically logged into the system and you can start tracking your habits. However, please note down your username, since there is no possibility to retrieve it later on, if you forget it. 

_Vielleicht ein Bild vom Login-screen einbinden?_

Once logged in, you can start managing and tracking your habits by first creating new habits and then checking them off after you have completed the habits. Habit analysis is only possible after checking off at least one habit. When you don't need a habit anymore, you can simply delete its data. If you want to rename or change a habit's periodicity, just select manage habits > modify habit and follow the instructions on screen. After performing an action with the app (e.g., after analyzing a habit), you will automatically return to the action menu screen to perform other actions to your liking. If you want to close the application, you can do so by choosing "exit".  

_Vielleicht ein Bild vom Action-menu einbinden?_

## Tests

To test the app's functionalities and to see what it looks like once you have created and completed some habits, you can login to the app with one of the following dummy users:
- User 1: has defined 6 habits, etc. 

```shell
pytest .
```