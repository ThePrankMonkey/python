from datetime import date
from paydaycountdown import HolidayEZ
from paydaycountdown import HolidayHard

july_4th = HolidayEZ("July 4th", 7, 4, 2018)
def test_july_4th_date():
    assert(july_4th.date == date(2018,7,4))

def test_july_4th_name():
    assert(july_4th.name == "July 4th")

veterens_day = HolidayEZ("Veterans Day", 11, 11, 2018)
veterens_day_observed = HolidayEZ("Veterans Day", 11, 11, 2018, observed=True)
def test_veterens_day_date():
    assert(veterens_day.date == date(2018,11,11))

def test_veterens_day_name():
    assert(veterens_day.name == "Veterans Day")

def test_veterens_day_observed_date():
    assert(veterens_day_observed.date == date(2018,11,12))

def test_veterens_day_observed_name():
    assert(veterens_day_observed.name == "Veterans Day (Observed)")

thanksgiving_day = HolidayHard("Thanksgiving Day", 11, 4, 3, 2018)
def test_thanksgiving_day_date():
    assert(thanksgiving_day.date == date(2018,11,22))

def test_thanksgiving_day_name():
    assert(thanksgiving_day.name == "Thanksgiving Day")