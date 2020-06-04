import time
import datetime
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
    available_month = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    available_days = ['monday', 'tuesday', 'wednesday','thursday', 'friday', 'saturday', 'sunday', 'all']
    print('\n\nHello! Let\'s explore some US bikeshare data!\n')

    # gets the input of the cities
    city = input('Please enter the name of the city you want to see the data for!\n\n').lower()
    while city not in CITY_DATA.keys():
        city = input('\nPlease chose Washington, Chicago or New York City!\n\n').lower()
    print('\nGreat! You picked {}!'.format(city.title()))

    # gets the input of the month
    month = input('For which month would you like to see the data for?\n\n').lower()
    while month not in available_month:
        month = input('Please chose January, February, March, April, May, June or all!\n').lower()

    # gets the input for the day of the week
    if month == 'all':
        day = input('\nWould you like to see the Data of a certain day of the week? Please type in the name!\n\n'.format(month.title())).lower()

    else:
        day = input('\nFor which day of the week in {} would you like to see the Data?\n\n'.format(month.title())).lower()

    while day not in available_days:
        day = input('\nPlease type in all or the name of a day.\n').lower()

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
    df = pd.read_csv(CITY_DATA[city])

    # creates columns for month and day of the week in the dataframe
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filters by month if chosen by user
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
        df = df[df['month'] == month]

    # filters by day of week if chosen by user
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    # Let's the user see the first 5 lines of raw data and continues to show 5 more if wanted by user
    see_data = input('\nWould you like to see the first 5 rows of raw data? Type in Yes!\n').lower()
    i = 0
    while see_data == 'yes':
        print(df.iloc[i:i+5])
        i += 5
        see_data = input('\nWould you like to see 5 more rows? Type in Yes!\n').lower()

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # displays the most common month if dataframe contains more than one month
    month_count = df['month'].value_counts()
    row_count = len(df.index)

    if month_count.iloc[0] == row_count:
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        print('\nYou\'ve picked to only see Data of {}'.format(months[month_count.index[0]-1].title()))
    else:
        most_common_month = df['month'].mode()[0]
        month = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June'}
        print('Most bikes were rented in', month[most_common_month])

    # displays the most common day of week if dataframe contains more than one day of the week
    dow_count = df['day_of_week'].value_counts()

    if dow_count.iloc[0] == row_count:
        print('\nYou\'ve picked to only see data of {}'.format(dow_count.index[0].title()))
    else:
        most_common_dow = df['day_of_week'].mode()[0]
        print('The day of the week the most bikes got rented is', most_common_dow)

    # displays the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    hour ={0:'12am', 1:'1am', 2:'2am', 3:'3am',4:'4am', 5:'5am', 6:'6am',7:'7am', 8:'8am', 9:'9am', 10:'10am', 11:'11am', 12:'12pm', 13:'1pm', 14:'2pm', 15:'3pm', 16:'4pm', 17:'5pm', 18:'6pm', 19:'7pm', 20:'8pm', 21:'9pm', 22:'10pm', 23:'11pm'}
    most_common_hour = df['hour'].mode()[0]
    print('\nThe most rentals started beween', hour[most_common_hour], 'and', hour[(most_common_hour+1)])

    #prints time to calculate
    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # displays most commonly used start station
    most_common_sstation = df['Start Station'].mode()[0]
    print('the station where the most rentals started is', most_common_SStation)

    # displays most commonly used end station
    most_common_estation = df['End Station'].mode()[0]
    print('the station where the most rentals ended is', most_common_EStation)

    # displays most frequent combination of start station and end station trip
    df['Start & End Station'] = df['Start Station'] + ' / ' + df['End Station']
    most_common_stationcom = df['Start & End Station'].mode()[0]
    print('The most common combination of start and end station is', most_common_stationcom)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # displays total travel time
    total_travel_sec = int(df['Trip Duration'].sum())
    total_rental_time = datetime.timedelta(seconds=total_travel_sec)
    print('the total time of all rentals is', total_rental_time)
    # displays mean travel time
    mean_travel_sec = int(df['Trip Duration'].mean())
    mean_travel_time = datetime.timedelta(seconds=mean_travel_sec)
    print('the average time of a rental is', mean_travel_time)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # displays counts of user types
    user_type_counts = df['User Type'].value_counts()
    print('Here is a list of how often each user type rented a bike:\n',user_type_counts, '\n')
    # displays counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('Here is a list of how often rentals were made by males/females:\n',gender_counts, '\n')
    else:
        print('There is no data regarding the gender of the users for this city!')

    # displays earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        youngest_user = int(df['Birth Year'].max())
        oldest_user = int(df['Birth Year'].min())
        most_common_age = df['Birth Year'].value_counts()
        print('The youngest user was born in', youngest_user)
        print('The oldest user was born in', oldest_user)
        print('The most users were born in', int(most_common_age.index[0]))
    else:
        print('There is no data regarding the age of the users for this city!')


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

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
