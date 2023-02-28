import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

City_Names = ["chicago", "washington", "new york"]

def align_months(month_number):
    
    months_names = {1:'January', 2:'February', 3:'March', 
             4:'April', 5:'May', 6:'June', 7:'July',
             8:'August', 9:'September', 10:'October',
             11:'November', 12:'December'}
    
    return months_names[month_number]

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

    x= 0
    while x != -1:
        city = input('Which city you want to select?  Chicago, Washington, or New York ')
        city = city.lower()
        if city in City_Names:
            #print("\nThe city is: ",city)
            x = -1
        else:
            print("Please check you spelling, rewrite the city name [Chicago, Washington, or New York]  ")

    # get user input for month (all, january, february, ... , june)

    month = input('All right! now it\'s time to provide us a month name or just say \'all\' to apply no month filter. \n(e.g. all, january, february, march, april, may, june) \n> ')

    # get user input for day of week (all, monday, tuesday, ... sunday)

    day = input('One last thing. Could you type one of the week day you want to analyze?'\
                   ' You can type \'all\' again to apply no day filter. \n(e.g. all, monday, sunday) \n> ')

    print('-'*40)
    return city, month, day

# this function is used to load dataset, and adding a three new cloumns Month, Day, and Hour
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
    
    # converting start time object to data_time, for reading the month, week, and days from data rows
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # Modify the name of the months
    df["month"] = df.month.apply(align_months)
    
    if month != 'all':
        df = df[ df['month'].str.lower() == month ]
    
    if day != 'all':   
        df = df[ df['day_of_week'].str.lower() == day ]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['Start Time'].dt.month
    counts_month = common_month.value_counts().sort_values(ascending =True)
    month_num = counts_month.index[-1]
    
    months_names = ['January', 'February', 'March', 
             'April', 'May', 'June','July',
             'August','September','October',
             'November','December']

    month = months_names[month_num - 1]
    renting_total_month = max(counts_month)
    print(f"The most common month of travel is: \"{month}\", with {renting_total_month} count record.")


    # display the most common day of week
    common_day = df['Start Time'].dt.day_name()
    counts_days = common_day.value_counts().sort_values(ascending =True)
    days_num=counts_days.index[-1]
    
    day = days_num
    renting_total_day = max(counts_days)
    
    print(f"The most common day of travel is: \"{day}\", with {renting_total_day} count record.")


    # display the most common start hour
    common_hour = df['Start Time'].dt.hour
    counts_hours = common_hour.value_counts().sort_values(ascending =True)
    hours_num=counts_hours.index[-1]
    hour = hours_num
    renting_total_hour = max(counts_hours)
    
    if hour < 12:
        print(f"The most common hour of travel is: {hour} AM in the morning, with {renting_total_hour} count record.")

    elif hour > 12 & hour < 24:
        print(f"The most common hour of travel is:  {hour - 12} PM in the evening, with {renting_total_hour} count record.")
        
    elif hour == 24:
        print(f"The most common hour of travel is: {hour - 12} AM in the morning , with {renting_total_hour} count record.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].value_counts().sort_values(ascending = False)
    start_station_name = start_station.index[0]
    print(f"The most used start station: {start_station_name}, with {start_station[start_station_name]} count record." )
    

    # display most commonly used end station
    end_station = df['End Station'].value_counts().sort_values(ascending = False)
    end_station_name = end_station.index[0]
    print(f"The most used End station: {end_station_name}, with {end_station[end_station_name]} count record." )


    # display most frequent combination of start station and end station trip
    start_end_station = df[['Start Station', 'End Station']].mode().loc[0]
    print(f"The most used combination between start and end station are : {start_end_station[1]}, {start_end_station[0]} count record." )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_mean = df['Trip Duration'].mean()
    print("The mean travel time is: {:0.2f}".format(travel_mean))

    # display mean travel time
    travel_maximum = df['Trip Duration'].max()
    print("The maximum travel time is: ", travel_maximum)
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_counts = df['User Type'].value_counts()
    print(f"The total user counts is: \n {user_counts}")

    # Display counts of gender (only available for NYC and Chicago)
    if city == 'new york' or city == 'chicago':
        if 'Gender' in df.columns:
            gender_counts = df['Gender'].value_counts()
            print(f"The total counts of gender: \n {gender_counts}")
    else:
        print('Count of Gender could not be displayed, the dataset does not contain information for Gender\n')


    # Display earliest, most recent, and most common year of birth
    #earliest, most recent, most common year of birth (only available for NYC and Chicago)
    if city == 'new york' or city == 'chicago':
        
        # the most common birth year
        
        birth_year = df['Birth Year'].value_counts().sort_values(ascending = False)
        common_year = birth_year.index[0]
        #common_year = birth_year.value_counts().idxmax()
        print("\nThe most common birth year:", int(common_year))
        # the most recent birth year
        recent_birth_year = df['Birth Year'].max()
        print("The most recent birth year:",int(recent_birth_year))
        # the most earliest birth year
        early_birth_year = df['Birth Year'].min()
        print("The most earliest birth year:", int(early_birth_year))
        
    else:
         print('The Birth Year could not be displayed, the dataset does not contain information for Birth Year\n')

        
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def show_five_rows_data(df):
    
    i = 0 #intalize value with 0 (row)
    while True:
        view_raw_data = input('\nWould you like to see the rows of the first five row data? Enter yes or no.\n')
        
        while view_raw_data.lower() != "yes" and view_raw_data.lower() != "no":
            view_raw_data = input('\n You answer is not correct, Would you like to see the rows of the first five row data? Enter yes or no.\n')  
        
        if view_raw_data.lower() == 'yes':
            i = i + 5 # 5 rows
            print(df.loc[ i:i+5, : ])
        elif view_raw_data.lower() == 'no':
            break
        

def main():
    while True:
        city, month, day = get_filters()
        print(f"The city is: {city} and the month {month}, {day} ")
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        
        show_five_rows_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        
        while restart.lower() != "yes" and restart.lower() != "no":
            restart = input('\nYou answer is not correct, Would you like to restart? Enter yes or no.\n')

        if restart.lower() != 'yes':
            break

            


if __name__ == "__main__":
	main()
