from dataclasses import dataclass
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


@dataclass
class WorkOrderRecurrence:
    id: int
    workorder_id: int
    type: str
    start_date: date
    lastraised_date: date
    interval: int
    weekdays: str
    day: int
    month: int
    month_weekday_occurrence: int

    def is_due(self):

        occurrences = list()
        d = self.start_date
        todays_date = date.today()
        type = self.type.strip().lower()

        if self.weekdays:
            weekdays = [int(wd) for wd in self.weekdays.split(";")]

        while d <= todays_date:

            date_step = timedelta(days=1)

            if type == "daily":

                if self.interval:
                    
                    occurrences.append(d)

                    date_step = timedelta(days=self.interval)

                elif self.weekdays:

                    if d.isoweekday() in weekdays:
                        occurrences.append(d)
                    
                    date_step = timedelta(days=1)

            elif type == "weekly":
                
                monday_date = d - timedelta(days=d.isoweekday()-1)

                for i in range(7):
                    week_date = monday_date + timedelta(days=i)
                    if week_date.isoweekday() in weekdays and week_date <= todays_date and week_date > self.lastraised_date:
                        occurrences.append(week_date)

                date_step = timedelta(days=7 * self.interval)

            elif type == "monthly":
                
                relative = relativedelta(d, self.start_date)

                # By day number of month interval
                if self.day and self.interval:
                    
                    if d.day == self.day and (relative.months + relative.years * 12) % self.interval == 0:
                        occurrences.append(d)
                    
                    date_step = timedelta(days=1)

                # By weekday occurrence of month interval
                elif self.month_weekday_occurrence and self.weekdays and self.interval:
                    
                    if relative.months % self.interval == 0:
                        dates = list()

                        _d = date(d.year, d.month, 1)
                        while _d.month == d.month and _d.year == d.year:

                            if _d.isoweekday() == weekdays[0]:
                                dates.append(_d)

                            _d += timedelta(days=1)

                        index = self.month_weekday_occurrence if self.month_weekday_occurrence <= 3 else -1
                        occurrences.append(dates[index])

                    next_month_mod = (d.month + 1) % 12
                    years_to_add = d.month // 12
                    next_month_date = date(d.year + years_to_add, 12 if next_month_mod == 0 else next_month_mod, 1)
                    days_to_add = next_month_date - d
                    date_step = timedelta(days=days_to_add.days)

            elif type == "yearly":
                
                if self.interval:
                    years_difference = self.start_date.year - d.year
                    if years_difference % self.interval == 0 and d.month == self.month:

                        # By day, month number
                        if self.month and self.day:

                            occurrences.append(date(d.year, self.month, self.day))
                            date_step = timedelta(days=365)

                        # By weekday occurence of month number and year interval
                        elif self.month_weekday_occurrence and self.weekdays and self.month:

                            dates = list()

                            _d = date(d.year, d.month, 1)
                            while _d.month == d.month and _d.year == d.year:

                                if _d.isoweekday() == weekdays[0]:
                                    dates.append(_d)

                                _d += timedelta(days=1)

                            index = self.month_weekday_occurrence - 1 if self.month_weekday_occurrence <= 3 else -1
                            occurrences.append(dates[index])

                            next_month_mod = (d.month + 1) % 12
                            years_to_add = d.month // 12
                            next_month_date = date(d.year + years_to_add, 12 if next_month_mod == 0 else next_month_mod, 1)
                            days_to_add = next_month_date - d
                            date_step = timedelta(days=days_to_add.days)

            d += date_step

        occurrences = sorted(list(filter(lambda o: o > self.lastraised_date and o <= todays_date, occurrences)))
        if occurrences:
            print(occurrences)
            return todays_date >= occurrences[-1]
        return False
        
    
if __name__ == "__main__":

    start_date = date(2019, 1, 1)
    last_date = date(2019, 1, 1)
    
    # DAILY
    # By day interval
    # wor1 = WorkOrderRecurrence(None, None, "daily", start_date, last_date, 3, None, None, None, None)
    # print("Is wor1 due?", wor1.is_due())


    # By weekday
    # wor2 = WorkOrderRecurrence(None, None, "daily", start_date, last_date, None, "3", None, None, None)
    # print("Is wor2 due?", wor2.is_due())

    # WEEKLY
    # wor3 = WorkOrderRecurrence(None, None, "weekly", start_date, last_date, 2, "1;3;5", None, None, None)
    # print("Is wor3 due?", wor3.is_due())

    # MONTHLY
    # By day number of month interval
    # wor4 = WorkOrderRecurrence(None, None, "monthly", start_date, last_date, 2, None, 25, None, None)
    # print("Is wor4 due?", wor4.is_due())
    
    # YEARLY
    # By day, month number
    # wor5 = WorkOrderRecurrence(None, None, "monthly", start_date, last_date, 2, "2", None, None, 4)
    # print("Is wor5 due?", wor5.is_due())

    # By weekday occurence of month number and year interval
    wor6 = WorkOrderRecurrence(None, None, "yearly", start_date, last_date, 2, "2", None, 2, 3)
    print("Is wor6 due?", wor6.is_due())

