# B.4. 日期時間的沿革

The SQL standard states that“Within the definition of a‘datetime literal’, the‘datetime values’are constrained by the natural rules for dates and times according to the Gregorian calendar”.PostgreSQLfollows the SQL standard's lead by counting dates exclusively in the Gregorian calendar, even for years before that calendar was in use. This rule is known as the_proleptic Gregorian calendar_.

The Julian calendar was introduced by Julius Caesar in 45 BC. It was in common use in the Western world until the year 1582, when countries started changing to the Gregorian calendar. In the Julian calendar, the tropical year is approximated as 365 1/4 days = 365.25 days. This gives an error of about 1 day in 128 years.

The accumulating calendar error prompted Pope Gregory XIII to reform the calendar in accordance with instructions from the Council of Trent. In the Gregorian calendar, the tropical year is approximated as 365 + 97 / 400 days = 365.2425 days. Thus it takes approximately 3300 years for the tropical year to shift one day with respect to the Gregorian calendar.

The approximation 365+97/400 is achieved by having 97 leap years every 400 years, using the following rules:

| Every year divisible by 4 is a leap year. |
| :--- |
| However, every year divisible by 100 is not a leap year. |
| However, every year divisible by 400 is a leap year after all. |

So, 1700, 1800, 1900, 2100, and 2200 are not leap years. But 1600, 2000, and 2400 are leap years. By contrast, in the older Julian calendar all years divisible by 4 are leap years.

The papal bull of February 1582 decreed that 10 days should be dropped from October 1582 so that 15 October should follow immediately after 4 October. This was observed in Italy, Poland, Portugal, and Spain. Other Catholic countries followed shortly after, but Protestant countries were reluctant to change, and the Greek Orthodox countries didn't change until the start of the 20th century. The reform was observed by Great Britain and its dominions \(including what is now the USA\) in 1752. Thus 2 September 1752 was followed by 14 September 1752. This is why Unix systems have the`cal`program produce the following:

```text
$ cal 9 1752

   September 1752
 S  M Tu  W Th  F  S
       1  2 14 15 16
17 18 19 20 21 22 23
24 25 26 27 28 29 30
```

But, of course, this calendar is only valid for Great Britain and dominions, not other places. Since it would be difficult and confusing to try to track the actual calendars that were in use in various places at various times,PostgreSQLdoes not try, but rather follows the Gregorian calendar rules for all dates, even though this method is not historically accurate.

Different calendars have been developed in various parts of the world, many predating the Gregorian system. For example, the beginnings of the Chinese calendar can be traced back to the 14th century BC. Legend has it that the Emperor Huangdi invented that calendar in 2637 BC. The People's Republic of China uses the Gregorian calendar for civil purposes. The Chinese calendar is used for determining festivals.

The\_Julian Date\_system is another type of calendar, unrelated to the Julian calendar though it is confusingly named similarly to that calendar. The Julian Date system was invented by the French scholar Joseph Justus Scaliger \(1540-1609\) and probably takes its name from Scaliger's father, the Italian scholar Julius Caesar Scaliger \(1484-1558\). In the Julian Date system, each day has a sequential number, starting from JD 0 \(which is sometimes called\_the\_Julian Date\). JD 0 corresponds to 1 January 4713 BC in the Julian calendar, or 24 November 4714 BC in the Gregorian calendar. Julian Date counting is most often used by astronomers for labeling their nightly observations, and therefore a date runs from noon UTC to the next noon UTC, rather than from midnight to midnight: JD 0 designates the 24 hours from noon UTC on 24 November 4714 BC to noon UTC on 25 November 4714 BC.

AlthoughPostgreSQLsupports Julian Date notation for input and output of dates \(and also uses Julian dates for some internal datetime calculations\), it does not observe the nicety of having dates run from noon to noon.PostgreSQLtreats a Julian Date as running from midnight to midnight.

* [https://www.postgresql.org/docs/10/static/datetime-units-history.html](https://www.postgresql.org/docs/10/static/datetime-units-history.html)

