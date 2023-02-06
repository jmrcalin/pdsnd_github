"""
    File name: bikeshare_2.py
    Author: Jose Miguel Rubio Calin
    Date created: 08/12/2022
    Date last modified: 10/30/2022
    Python Version: 3.9.7
"""

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('ENTER THE CITY: ')
    while city not in ['chicago', 'new york city', 'washington']:
    
        city = input ("CHOOSE BETWEEN chicago, new york city OR washington: ").lower()

    # get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = input('Enter the month from january to june OR Enter "all" for no month filter : ')
    while month not in months:
    
        month = input('Enter the month from january to june or Enter "all" for no month filter : ').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = input('Enter the day from monday to sunday OR Enter "all" for no day filter : ')
    while day not in days:
        day = input('Enter the day from monday to sunday OR Enter "all" for no day filter : ').lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Loading data file into a dataframe.
    if city =='new york city':
        city='new'+'_'+'york'+'_'+'city'
    df = pd.read_csv('{}.csv'.format(city))

    #convert columns od Start Time and End Time into date format yyyy-mm-dd
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # Extracting month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    # Filtering by month if applicable
    if month != "all" : 
        # Useing the index of the months list to get corresponding integer
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # Filtering by month to create new dataframe
        df = df[df['month'] == month]
    
# Filtering by day of week if applicable
    if day != 'all':
     # Useing the index of the days list to get corresponding integer
       days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
       day_of_week = days.index(day) + 0
        # Filtering by day of week to create the new dataframe
       df = df[df['day_of_week'] == day_of_week]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Converting the Start Time column to datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    common_month = df['month'].mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print('Most Popular Month:', months[common_month-1])

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday

    common_day = df['day_of_week'].mode()[0]
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    print('Most Popular Day:', days[common_day])


    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most Popular Start Station: ', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most Popular End Station: ', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print('\nMost Frequent Combination of Start and End Station Trips:\n\n',df.groupby(['Start Station', 'End Station']).size().nlargest(1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total Trip Duration in seconds:', df['Trip Duration'].sum())

    # display mean travel time
    print('Mean Trip Duration in seconds:', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types,'\n')

    # Display counts of gender
    user_gender = df['Gender'].value_counts()
    print(user_gender)

    # Display earliest, most recent, and most common year of birth

    earliest_year_of_birth = int(df['Birth Year'].min())
    most_recent_year_of_birth = int(df['Birth Year'].max())
    most_common_year_of_birth = int(df['Birth Year'].mode()[0])

    print("The earliest year of birth is:",earliest_year_of_birth,
          ", most recent one is:",most_recent_year_of_birth,
           "and the most common one is: ",most_common_year_of_birth)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
