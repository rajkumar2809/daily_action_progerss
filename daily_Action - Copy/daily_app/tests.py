import datetime
import time

x = datetime.datetime.now()
print(x)
time.sleep(2.4)


time.sleep(12)

y = datetime.datetime.now()
# y = '2022-10-01 22:29:11.447366'
# # y = datetime('2022-10-01 22:29:11.447366')
# date_time_obj = datetime.datetime.strptime(y, '%Y-%m-%d %H:%M:%S.%f')
# print(date_time_obj)

date_diff = y - x
print(date_diff)
secs = date_diff.total_seconds() / 3600
print(secs)
h = date_diff.total_seconds()//3600
m = (date_diff.total_seconds()%3600) // 60
sec =(date_diff.total_seconds()%3600)%60


print ("%d:%d:%d" %(h,m,sec))

# a = [8, 7, 6, 5]
# b = [2 , 1]

# for (i in a )and (j in b) :
#     # for j in b:
#         # print(j)
#     print(i , j)
# # if(x in a ):
# #     print(x)

# import datetime
# duration = datetime.timedelta(days = 2, hours = 4, minutes = 15)
# # Once we got a timedelta object:

# totsec = duration.total_seconds()
# h = totsec//3600
# m = (totsec%3600) // 60
# sec =(totsec%3600)%60 #just for reference
# print ("%d:%d" %(h,m))