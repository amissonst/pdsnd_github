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
    print('Hi there! Welcome to the bikeshare analysis. Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities_list = ['chicago','new york city','washington']
    while(True):
        city = input('\nPlease enter the name of the city you want to explore: Data is available for Chicago, New York City and Washington:\n')
        if city.lower() in cities_list:
            print('Good choice! Let\'s explore {}\'s data'.format(city.title()))
            break
        else:
            print('\nSorry! Data is only available for Chicago, New York City and Washington. Please select one of those and try again.')

    # TO DO: get user input for month (all, january, february, ... , june)
    months_list = ['january','february','march','april','may','june']
    print('\nWhich month would you like to analyze? Data is available for January, February, March, April, May, or June. If you would like to review all months please enter all.\n.')
    while(True):
        month = input('Enter the name of the month you wish to start: ')
        if month.lower() in months_list or month.lower() == 'all':
            print('\nYou have chosen to analyze {}\'s data'.format(month.title()))
            break
        else:
            print('\nSorry, you have chosen an invalid month. Please enter a month between January and June.')
                     
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days_list = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    print('\nPlease enter a day of the week you would like to analyze. If you would like to review all days please enter all.')
    while(True):
        day = input('\nType the full name of the day you would like to analyze (All, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday or Saturday):\n')
        if day.lower() in days_list or day.lower() == 'all':
            print('\nYou have chosen to analyze data for {}'.format(day.title()))
            break
        else:
            print('\nSorry, you have chosen an invalid day. Please enter the full name of one of the days of the week or All to analyze all days.')

    print('-'*40)
    return city.lower(), month.lower(), day.lower()


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
    df = pd.read_csv(CITY_DATA[city])
    #df = df.drop(df.columns[0],axis = 1)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    #df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # slices the data by month
    if month.lower() != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # slices data by month
        df = df[df['Month'] == month]

    # day of the week filter
    if day.lower() != 'all':

        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['Month'].mode()[0]
    print('The most common month is: {}'.format(most_common_month))

    # TO DO: display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('The most common day is: {}'.format(most_common_day))

    # TO DO: display the most common start hour
    most_common_hour = df['Start Time'].dt.hour.mode()[0]
    print('The most common start hour is: {}'.format(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is: ' + most_common_start_station)


    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is: ' + most_common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    most_frequent_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('The most commonly used trip is from: {} to {}'.format(*most_frequent_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is: {} seconds'.format(total_travel_time))

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time is: {} seconds'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('Counts by User Types')
    print(df.groupby('User Type').count())

    
    # TO DO: Display counts of gender 
    """Washington data is missing birth year and gender -- needs error handling for those issues"""
    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        print("Gender:\n",gender,"\n")

    # TO DO: Display earliest, most recent, and most common year of birth
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print('\nThe earliest birth year is {}, most recent is: {} and the most common is: {}'.format(earliest_year,most_recent_year,most_common_year))
    else:
            print("No Gender or Birth Year data available for this city")
    """Display total time"""
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
        """Gives the user the option to restart the program again to run an alternate analysis"""
        restart = input('\nWould you like to restart the program? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
