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
    city = input('Please enter a city name : ').lower()
    # input validation
    while city not in CITY_DATA.keys():
        print('That\'s an invalid input')
        # ask for the input again
        city = input('Pleas choose from the available data \n Chicago \n New York City \n Washington \n ').lower()
        
    # get user input for month (all, january, february, ... , june)
    months = ['January', 'February', 'March', 'April', 'Mai', 'June', 'All']
    while True: 
        month = input('Please choose a month or All for all data: ')
        if month not in months: 
            print('That\'s not a valid input')
        else: 
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'All']
    while True: 
        day = input('Please choose a day or All for all data: ')
        if day not in days: 
            print('That\'s not a valid input')
        else: 
            break


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
    # read data into a data frame
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column into Date Time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and days of the week to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Days of The week'] = df['Start Time'].dt.day_name()
    
    # filter by month if applicable
    if month != 'All':
        # use the index of months list
        months = ['January', 'February', 'March', 'April', 'Mai', 'June']
        month = months.index(month) +1
        
        # filter by month to create the new dataframe
        df = df[df['Month'] == month]
        
        # filter by day if applicable
        if day != 'All': 
            # filter by day of the week to create the new dataframe
            df= df[df['Days of The week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    print('\n Calculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # The Most Commun Month
    print("The Most Commun Month is: ", df['Month'].value_counts().idxmax())    
    # The Most Commun Day of The Week
    print("The Most Commun Day of The Week is: ", df['Days of The week'].value_counts().idxmax())
    # The Most Commun Hour
    df['Hour'] = df['Start Time'].dt.hour
    print("The Most Commun Hour is: ", df['Hour'].value_counts().idxmax())
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """ Displays statistics on most popular stations and trips."""
    print('\nCalculating The Most Popular Stations and Trips...\n')
    
    start_time = time.time()
    
    # The most popular start station
    print('The Most Popular Start Station is :', df['Start Station'].value_counts().idxmax())
    
    # The most popular end station
    print('The Most Popular End Station is :', df['End Station'].value_counts().idxmax())
    
    # The most frequent combination of the start and end stations
    print('The Most Frequent Combination of Start Station and End Station Trip')
    most_common_start_and_end_stations = df.groupby(['Start Station','End Station']).size().nlargest(1)
    print(most_common_start_and_end_stations)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
 
def trip_duration_stats(df):
    """Displays Statistics on total and average trip durations""" 
    
    print('\nCalculating trip duration...\n')   
    start_time= time.time()
    
    total_duration = df['Trip Duration'].sum()/3600.00
    print('The total trip duration is : ', total_duration)
    
    average_duration = df['Trip Duration'].mean()/3600.00
    print('The average duration is :', average_duration)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def user_stats(df,city): 
    """Display Statistics on Bikeshare users"""
    
    print('\nCalculating User Statistics...\n')
    
    start_time = time.time()
    
    # Counts of user types
    user_type = df['User Type'].value_counts()
    print(user_type)
    
    # Counts of user gender
    if city != 'washington':
        user_gender = df['Gender'].value_counts()
        print(user_gender)
    
    # Displaying the earliest, most recent, most common year of birth
        earliest_year_of_birth = int(df['Birth Year'].min())
        recent_year_of_birth = int(df['Birth Year'].max())
        most_common_year_of_birth = int(df['Birth Year'].value_counts().idxmax())
    
        print('The earliest year of birth is :',earliest_year_of_birth, 
             ',The most recent year of birth is : ', recent_year_of_birth,
             ', The most common year of birth is :',most_common_year_of_birth )
    else: 
        print('There is no data for this city')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def raw_data(df):
    """Displays raw data with every press"""
    print('Press Enter to dsiplay new raw data, write no to skip')
    x = 0
    while(input()!= 'no'):
        x=x+5
        print(df.head(x))
    
    

def main():
    while True:
        city, month, day = get_filters()
        print(city, month, day)
        df = load_data(city, month, day)
        print(df.head())
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()