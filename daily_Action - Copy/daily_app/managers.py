from django.db import models
from django.db.models import Count

class ThreadManager(models.Manager):
    def get_or_create_personal_thread(self , user1 , user2):
        try:
            print("==============inside get_or_create_personal_thread() ======== ")
            print(user1)
            print(user2)
            threads = self.get_queryset().filter(thread_type ='personal')
            print("THe threads are ")
            print(threads)
            threads = threads.filter(users__in=[user1 , user2]).distinct()
            print("++++the threads are+++")
            print(threads)
            print("----the threads are-------")
            # threads = threads.annotate(u_count = Count('users')).filter(u_count = 2)
            print("===the threads are====")
            print(threads)
            print("-+=-+=the threads are-+=-+=")

            if threads:#.exists():
            # if threads.exists():
                print("Exists ")
                return threads.first()

            else:
                print("Not exists")
                thread = self.create(thread_type = 'personal')
                thread.users.add(user1)
                thread.users.add(user2)
                return thread
        except Exception as e:
            print("=======Exception occurs===========")
            print(e)
            print("-------------Exception occurs----------")


    
    def by_user(self, user):
        return self.get_queryset().filter(users__in=[user])

