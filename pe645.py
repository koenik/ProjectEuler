"""
This file solves the ProjectEuler No 645

Source: 2018-12-05 https://projecteuler.net/problem=645

"
On planet J, a year lasts for D days. Holidays are defined by the two following rules.

At the beginning of the reign of the current Emperor, his birthday is declared a holiday from that year onwards.
If both the day before and after a day d are holidays, then d also becomes a holiday.
Initially there are no holidays.
Let E(D) be the expected number of Emperors to reign before all the days of the year are holidays,
assuming that their birthdays are independent and uniformly distributed throughout the D days of the year.

You are given E(2)=1, E(5)=31/6, E(365)≈1174.3501.

Find E(10000). Give your answer rounded to 4 digits after the decimal point.
"

code (c) 2018 koenik.******@gmail.com

"""

import numpy as np
from matplotlib import pyplot as plt
plt.style.use('ggplot')


class Calendar:
    """
    Calendar is a class that is basically a trivial, linear database.
    For every day in a year there is a slot in a numpy-array.
    The number in this slot is 0 if this particular day is no holiday and
    if it is a holiday, the number is >0.
    """
    def __init__(self, D):
        self.D = D  # number of days in a year
        self.calendar = np.zeros(self.D)  # initially no holidays
        self.numberOfEmperors = 0  # no emperor in the beginning

    def print_calendar(self):
        print(self.calendar)

    def everyday_is_a_holiday(self):
        """
        :return: check if every day of the calendar is a holiday
        """
        return np.count_nonzero(self.calendar) == len(self.calendar)

    def add_holiday(self, new_holiday):
        self.calendar[new_holiday] += 1

    def add_birthday(self, new_birthday, resolve_bridge_day=1, verbose=0):
        """
        A new emperor is born and it's birthday will be added to the calendar subsequently.
        Then the adjacent days will be checked whether they are to be declared as a holiday as well.
        :param new_birthday: int: 0 <= new_birthday <= self.D
        :param resolve_bridge_day: flag: if 1 then check neighbours of birth day and resolve
        :param verbose: debugging purpose
        :return:
        """
        self.numberOfEmperors += 1
        self.add_holiday(new_birthday)

        if verbose > 0:
            print("Emperor #", self.numberOfEmperors, "has birthday on: ", new_birthday)

        if resolve_bridge_day > 0:
            for neighbour_day in [new_birthday-1, new_birthday+1]:
                if neighbour_day > self.D - 1:  # workaround: avoid calendar-cut-off
                    neighbour_day = 0
                if self.is_bridge_day(neighbour_day):
                    if verbose > 0:
                        print("Found a bridge day:", neighbour_day)
                        self.print_calendar()
                    self.add_holiday(neighbour_day)

    # function is deprecated, i.e. not used.
    # Same functionality is implemented in add_birthday eventually
    # with lower computational cost.
    def is_bridge_day(self, day):
        """
        Definition of bridge day, see file description.
        Interpretation: if calendar[0] is checked. see calendar[-1] and calender[1].
        :param day: int: 0 <= new_birthday <= self.D
        :return: int: 1 if day is bridge day
        """
        if self.calendar[day] < 1:
            successing_day = day+1
            if successing_day > self.D-1:  # workaround: avoid calendar-cut-off
                successing_day = 0
            if (self.calendar[day-1] > 0) and (self.calendar[successing_day] > 0):
                return 1
        else:
            return 0

    def resolve_bridge_days(self, verbose=0):
        """
        Function goes through calendar, if a bridge-day is detected, this will be turned into a holiday
        :param verbose: debugging purpose
        :return: -
        """
        for i in range(0, self.D):
            if self.is_bridge_day(i):
                if verbose > 0:
                    print("Found a bridge day:", i)
                    self.print_calendar()
                self.add_holiday(i)  # should be 1 afterwards in every case


def create_random_birthday(D, verbose=0):
    """
    creates a birthday, is uniformly distributed.
    :param D: numbers of days in the year
    :param verbose: int: debugging purpose
    :return: random birthday
    """
    bd = np.random.randint(D)
    if verbose > 0:
        print("New birthday: ", bd)
    return bd


def make_line_of_emperors(D, verbose=0):
    myCalendar = Calendar(D)
    while not myCalendar.everyday_is_a_holiday():
        new_birthday = create_random_birthday(D)
        myCalendar.add_birthday(new_birthday, resolve_bridge_day=1, verbose=verbose)

        # deprecated: myCalendar.resolve_bridge_days(verbose=verbose)

        if verbose > 0:
            myCalendar.print_calendar()
    return myCalendar.numberOfEmperors


if __name__ == "__main__":
    print("Project Euler 645")

    # init variables
    J = "Planet J"
    D = 10000 # Number of days in a year
    maxPlay = 250  # number of execution cycles
    NumberOfEmperorsPerPlay = np.zeros(maxPlay)
    MeanOfEmperors = np.zeros(maxPlay)  # accumulated mean

    # welcome
    print("We're on planet", J, ".")
    print("A year consists of", D, "days.")

    # plotting preparation
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    ax.axis([0, maxPlay, 0, 1400])
    plt.title("Sliding mean")
    plt.grid("on")
    x = list()
    y = list()
    ym = list()
    line1, = ax.plot(x, y, 'k.')
    line_mean, = ax.plot(x, ym, 'r-')
    #line2, = ax.plot([0, maxPlay], [31/6, 31/6], 'r--')
    #line2, = ax.plot([0, maxPlay], [1174.3501, 1174.3501], 'r--')
    ax.legend(['# Emperors', 'Mean'], loc='upper left')
    plt.xlabel('Trial')
    plt.ylabel('Number of Emperors')
    mytext = plt.text(3, 7, 'Current Mean')

    # main loop
    np.random.seed(seed=121212)

    for i in range(0, maxPlay):
        NumberOfEmperorsPerPlay[i] = make_line_of_emperors(D, verbose=0)
        # print("# ", i, "- We had ", NumberOfEmperorsPerPlay[i], "emperors until the calendar was full.")
        MeanOfEmperors[i] = np.mean(NumberOfEmperorsPerPlay[NumberOfEmperorsPerPlay != 0])
        # print("In the meantime the mean is: ", MeanSoFar[i])

        # save
        x.append(i)
        y.append(NumberOfEmperorsPerPlay[i])
        ym.append(MeanOfEmperors[i])

        # update plot
        line1.set_xdata(x)
        line1.set_ydata(y)
        line_mean.set_xdata(x)
        line_mean.set_ydata(ym)
        ax.axis([0, maxPlay, 0, MeanOfEmperors[0]*2])
        mytext.set_text(["Current Mean: ", MeanOfEmperors[i]])
        mytext.set_position([maxPlay/2.0,  MeanOfEmperors[0] * 1.9])

        fig.canvas.draw()
        plt.pause(0.02)

    print("E( ", D, ") = ", np.mean(NumberOfEmperorsPerPlay))
    # Compare with description
    # print("E(2)=1, E(5)=31/6=5.16666, E(365)≈1174.3501.")

    plt.show()
