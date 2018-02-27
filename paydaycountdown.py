"""Report how many days it is until the next pay check and make a amrked calendar."""

import calendar
import datetime
import os

# Settings
pay_day_1 = 6
pay_day_2 = 22


## Section 1: Find paydays and holidays
class HolidayEZ():
    """Creates a holiday that always occurs on a set day.
    
    :param name: A string, the name of the holiday.
    :param month: An integer, the month that the holiday occurs in (1-12).
    :param day: An integer, the day that the holiday occurs on.
    :param year: An integer, the year that the holiday occurs in (defaults to current year).
    :param observed: A boolean, dictates whether the holiday is shifted to the nearest work day.
    """
    def __init__(self, name, month, day, year=datetime.date.today().year, observed=False):
        self.name = name
        self.month = month
        self.day = day
        self.year = year
        self.observed = observed
        self.date = datetime.date(self.year, self.month, self.day)
        if observed:
            if self.date.weekday() == 5:
                self.date = self.date - datetime.timedelta(days=1)
                self.name = name + " (Observed)"
            elif self.date.weekday() == 6:
                self.date = self.date + datetime.timedelta(days=1)
                self.name = name + " (Observed)"
    
    def report(self):
        """Return a string declaring the holiday name and date."""
        print("{name} is on {date}".format(name=self.name, date=self.date))


class HolidayHard(HolidayEZ):
    """Creates a holiady that occurs on a floating date.
    
    :extends: HolidayEZ and overwrites the __init__ method.

    :param name: A string, the name of the holiday.
    :param month: An integer, the month that the holiday occurs in (1-12).
    :param weekday: An integer, the weekday that the holiday occurs on (0-6,SAT-FRI).
    :param ordinal: An integer, which occurence of the weekday the holiday occurs on.
    :param year: An integer, the year that the holiday occurs in (defaults to current year).
    """
    def __init__(self, name, month, weekday, ordinal, year=datetime.date.today().year):
        self.name = name
        self.month = month
        self.year = year
        # Checks to see if the first week has the day in question
        calendar.setfirstweekday(calendar.SUNDAY)
        if(ordinal >= 0):
            # Handle checks to see if in a week moving forward in the month
            inFirstWeek = calendar.monthcalendar(self.year, month)[0][weekday] != 0
            if inFirstWeek:
                day = calendar.monthcalendar(self.year, month)[ordinal][weekday]
            else:
                day = calendar.monthcalendar(self.year, month)[ordinal+1][weekday]
        else:
            # Handle checks to see if in a week moving backwards in the month
            inLastWeek = calendar.monthcalendar(self.year, month)[-1][weekday] != 0
            if inLastWeek:
                day = calendar.monthcalendar(self.year, month)[ordinal][weekday]
            else:
                day = calendar.monthcalendar(self.year, month)[ordinal-1][weekday]
        self.day = day
        self.date = datetime.date(self.year, self.month, self.day)


def build_holidays(year=datetime.date.today().year):
    """Find all the holidays in the year.

    :note: You may need to generate different holidays as these are what my company uses.

    :param year: An integer, the year you want to find holidays for (defaults to current year).
    :returns: Two lists, the first is of holiday objects and the second is just datetimes.
    """
    holidays = []
    holidays.append(
        HolidayEZ(name="New Year's Day",
                  month=1, day=1, year=year, observed=True)
    )
    holidays.append(
        HolidayHard(name="President's Day",
                    month=2, weekday=1, ordinal=2, year=year)
    )
    holidays.append(
        HolidayHard(name="Memorial Day",
                    month=5, weekday=1, ordinal=-1, year=year)
    )
    holidays.append(
        HolidayEZ(name="Independence Day",
                  month=7, day=4, observed=True, year=year)
    )
    holidays.append(
        HolidayHard(name="Labor Day",
                    month=9, weekday=1, ordinal=0, year=year)
    )
    holidays.append(
        HolidayEZ(name="Veterens Day",
                  month=11, day=11, observed=True, year=year)
    )
    holidays.append(
        HolidayHard(name="Thanksgiving Day",
                    month=11, weekday=4, ordinal=3, year=year)
    )
    holidays.append(
        HolidayHard(name="Day After Thanksgiving Day",
                    month=11, weekday=5, ordinal=3, year=year)
    )
    holidays.append(
        HolidayEZ(name="Christmas Day",
                  month=12, day=25, observed=True, year=year)
    )
    holidays.append(
        HolidayEZ(name="New Year's Day",
                  month=1, day=1, observed=True, year=year+1)
    )
    holidays.sort(key=lambda x: x.date)
    # Generate list that is just datetime objects
    holidates = []
    for holiday in holidays:
        holidates.append(holiday.date)
    return holidays, holidates


# Find real pay days
def get_real_pay_dates(today, offset=0):
    """Finds paydays in the provided month
    
    :param today: A datetime, it's the current day (used for year and month).
    :param offset: An integer, used for incrementing to the next month.

    :returns: Two datetimes, the actual dates for paydays in the provided month.
    """
    # Handle the offset
    if today.month + offset == 13:
        today = datetime.date(year=today.year+1, month=1, day = today.day)
    else:
        today = datetime.date(year=today.year, month=today.month+offset, day = today.day)

    dummy_days, holidates = build_holidays()

    # pay_day_1
    final_pay_day_1 = datetime.date(year=today.year, month=today.month, day=pay_day_1)
    #print("Beginning pay_day_1 is going to {date}, which is a {weekday}".format(date=final_pay_day_1, weekday=calendar.day_name[final_pay_day_1.weekday()]))
    while (final_pay_day_1 in holidates or final_pay_day_1.weekday() == 5 or final_pay_day_1.weekday() == 6):
        final_pay_day_1 = final_pay_day_1 - datetime.timedelta(days=1)
    #print("Final pay_day_1 is going to {date}, which is a {weekday}".format(date=final_pay_day_1, weekday=calendar.day_name[final_pay_day_1.weekday()]))
    # pay_day_2
    final_day_day_2 = datetime.date(year=today.year, month=today.month, day=pay_day_2)
    #print("Beginning pay_day_2 is going to {date}, which is a {weekday}".format(date=final_day_day_2, weekday=calendar.day_name[final_day_day_2.weekday()]))
    while (final_day_day_2 in holidates or final_day_day_2.weekday() == 5 or final_day_day_2.weekday() == 6):
        final_day_day_2 = final_day_day_2 - datetime.timedelta(days=1)
    #print("Final pay_day_2 is going to {date}, which is a {weekday}".format(date=final_day_day_2, weekday=calendar.day_name[final_day_day_2.weekday()]))
    return final_pay_day_1, final_day_day_2

def find_next_days():
    # Create holiday lists
    holidays, dummy_dates = build_holidays()

    # Find Next payday
    today = datetime.date.today()
    final_pay_day_1, final_day_day_2 = get_real_pay_dates(today, 0)
    if today <= final_pay_day_1:
        nextPay = final_pay_day_1
    elif today > final_pay_day_1 and today <= final_day_day_2:
        nextPay = final_day_day_2
    else:
        final_pay_day_1, final_day_day_2 = get_real_pay_dates(today, 1)
        nextPay = final_pay_day_1

    # Count down until next paycheck:
    days_until_pay = (nextPay - today).days
    if days_until_pay == 0:
        print("The next paycheck is today ({date})!!!".format(date=nextPay))
    elif days_until_pay == 1:
        print("The next paycheck is on {date} in {days} day!!".format(days=days_until_pay, date=nextPay))
    else:
        print("The next paycheck is on {date} in {days} days!!".format(days=days_until_pay, date=nextPay))

    # Find next holiday
    check = False
    for holiday in holidays:
        if today == holiday.date:
            print("Today is a holiday, {name}.".format(name=holiday.name))
        elif today < holiday.date and check == False:
            days_until_holiday = (holiday.date - today).days
            if days_until_holiday == 1:
                print("The next holiday is {name} on {date} in {days} day!!".format(name=holiday.name, date=holiday.date, days=days_until_holiday))
            else:
                print("The next holiday is {name} on {date} in {days} days!".format(name=holiday.name, date=holiday.date, days=days_until_holiday))
            check = True
        else:
            pass
            #print("Something odd happened.")


## Section 2: Make a marked calendar
def build_calendar(cal_year):
    """Creates an HTML file with a calendar marked with paydays and holidays.

    :param cal_year: An integer, the year you want the holiday to be.
    """

    # Build HTML Page of Yearly Calendar
    calendar.setfirstweekday(calendar.SUNDAY)
    final_calendar = """<style>
                    .pay{
                        background-color: lightgreen;
                        }
                        .holiday{
                            background-color: lightcoral;
                        }
                    </style>\r\n"""
    for month in range(1,13):
        final_pay_day_1, final_day_day_2 = get_real_pay_dates(datetime.date(cal_year,month,1), 0)
        month_cal = calendar.HTMLCalendar(calendar.SUNDAY)
        month_html = month_cal.formatmonth(cal_year, month)

        # Update paydays
        for payday in [final_pay_day_1, final_day_day_2]:
            string_match = "\">{day}<".format(day=payday.day)
            string_replace = " pay\"" + string_match
            month_html = month_html.replace(string_match, string_replace)
            
        # Add Holidays
        holidays, dummy_dates = build_holidays(cal_year)
        for holiday in holidays:
            if holiday.month == month and holiday.year == cal_year:
                string_match = "\">{day}<".format(day=holiday.date.day)
                string_replace = " holiday" + string_match
                month_html = month_html.replace(string_match, string_replace)

        # Update final_calendar
        final_calendar = final_calendar + month_html + "<br>"

    # Output File
    filename = "Calendar_{year}.html".format(year=cal_year)
    calendar_file = open(filename, "w+")
    calendar_file.write(final_calendar)
    print("Created a calendar for {year} at: {path}".format(year=cal_year, path=os.path.join(os.getcwd(), filename)))
    calendar_file.close()


## Section 3: Google API


## Main
if __name__ == "__main__":
    find_next_days()
    build_calendar(cal_year=2018)