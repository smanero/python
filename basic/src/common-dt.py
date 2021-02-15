import datetime as dt

#----------------------------- 
# Dates produce timedeltas when subtracted.

date2 = dt.datetime(2020, 10, 7)
date1 = dt.datetime(2009, 4, 17)

diff = date2 - date1
print(date2.strftime("%c")) 
#----------------------------- 
bree = dt.datetime(1981, 6, 16, 4, 35, 25)
nat  = dt.datetime(1973, 1, 18, 3, 45, 50)

difference = bree - nat
print ("There were", difference, "minutes between Nat and Bree")
#=> There were 3071 days, 0:49:35 between Nat and Bree

weeks, days = divmod(difference.days, 7)

minutes, seconds = divmod(difference.seconds, 60)
hours, minutes = divmod(minutes, 60)

print ("%d weeks, %d days, %d:%d:%d" % (weeks, days, hours, minutes, seconds))
#=> 438 weeks, 5 days, 0:49:35

#----------------------------- 
print ("There were", difference.days, "days between Bree and Nat.")
#=> There were 3071 days between bree and nat

#----------------------------- 
# Adding to or Subtracting from a Date
# Use the rather nice datetime.timedelta objects

now = dt.date(2003, 8, 6)
difference1 = dt.timedelta(days=1)
difference2 = dt.timedelta(weeks=-2)

print ("One day in the future is:", now + difference1)
#=> One day in the future is: 2003-08-07

print ("Two weeks in the past is:", now + difference2)
#=> Two weeks in the past is: 2003-07-23

print (dt.date(2003, 8, 6) - dt.date(2000, 8, 6))
#=> 1095 days, 0:00:00

#----------------------------- 
birthtime = dt.datetime(1973, 1, 18, 3, 45, 50)   # 1973-01-18 03:45:50

interval = dt.timedelta(seconds=5, minutes=17, hours=2, days=55) 
then = birthtime + interval

print ("Then is", then.ctime())
#=> Then is Wed Mar 14 06:02:55 1973

print ("Then is", then.strftime("%A %B %d %I:%M:%S %p %Y"))
#=> Then is Wednesday March 14 06:02:55 AM 1973

#-----------------------------
when = dt.datetime(1973, 1, 18) + dt.timedelta(days=55) 
print ("Nat was 55 days old on:", when.strftime("%m/%d/%Y").lstrip("0"))
#=> Nat was 55 days old on: 3/14/1973

#----------------------------- 
# Adding to or Subtracting from a Date
# Use the rather nice dt.timedelta objects

now = dt.date(2003, 8, 6)
difference1 = dt.timedelta(days=1)
difference2 = dt.timedelta(weeks=-2)

print ("One day in the future is:", now + difference1)
#=> One day in the future is: 2003-08-07

print ("Two weeks in the past is:", now + difference2)
#=> Two weeks in the past is: 2003-07-23

print (dt.date(2003, 8, 6) - dt.date(2000, 8, 6))
#=> 1095 days, 0:00:00

#----------------------------- 
birthtime = dt.datetime(1973, 1, 18, 3, 45, 50)   # 1973-01-18 03:45:50

interval = dt.timedelta(seconds=5, minutes=17, hours=2, days=55) 
then = birthtime + interval

print ("Then is", then.ctime())
#=> Then is Wed Mar 14 06:02:55 1973

print ("Then is", then.strftime("%A %B %d %I:%M:%S %p %Y"))
#=> Then is Wednesday March 14 06:02:55 AM 1973

#-----------------------------
when = dt.datetime(1973, 1, 18) + dt.timedelta(days=55) 
print ("Nat was 55 days old on:", when.strftime("%m/%d/%Y").lstrip("0"))
#=> Nat was 55 days old on: 3/14/1973
