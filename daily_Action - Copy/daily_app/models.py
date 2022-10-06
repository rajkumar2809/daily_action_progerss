from ast import Break
from cgitb import text
from time import sleep
from wsgiref.simple_server import demo_app
from django.db import models

from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import jsonfield

from daily_app.managers import ThreadManager
# Create your models here.

#channels are importing here as any message get stored in ChatMessage then this socket will be used to send the message.

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import datetime


class Message_Dict:
    def __init__(self , id , sender_id , receiver_id , text): # , count):
        self.id = id
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.text = text
        

# Create your models here.
class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, first_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, first_name, password, **other_fields)

    def create_user(self, email, user_name, first_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          first_name=first_name, **other_fields)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user



class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    # about = models.TextField(_(
    #     'about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    ROLES = (
        ('LEAD', 'LEAD'),
        ('MEMBER', 'MEMBER'),
        ('ADMIN', 'ADMIN'),
    )

    role = models.CharField(_('User Role'), max_length=50, choices=ROLES)
    mobno = models.CharField(max_length=120, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    group_id = models.BinaryField(blank=True , null= True )
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name']

    def __str__(self):
        return self.user_name

    class Meta:
        db_table = "USERS"
        verbose_name = 'User'

    
class Egroup (models.Model):
    id =models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    lead_id = models.CharField(max_length=100)

    # lead_id = models.ForeignKey(to=NewUser, on_delete=models.CASCADE, default='', blank=False,
    #                            null=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "EGROUP"
        verbose_name = 'Egroup'
        verbose_name_plural = "EGROUPS"




class Project(models.Model):
    id =models.AutoField(primary_key=True)
    lead_id = models.CharField(max_length= 100 , null= True,blank=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "PROJECTS"
        verbose_name = "Project"


class Tasks (models.Model):
    id =models.AutoField(primary_key=True )
    project_id = models.CharField(max_length=40)
    goup_id = models.CharField(max_length=20 , null= True )
    user_id = models.CharField(max_length=50 , null=True)
    # project_id = models.ForeignKey(to=Project, on_delete=models.CASCADE, default='', blank=False,
    #                            null=False)
    module_name = models.CharField(max_length=100 , null= True)
    estimated_time = models.IntegerField(default=5)
    time_taken = models.CharField(max_length=50 , null=True , blank=True)
    STATUS = (
        ('STARTED', 'STARTED'),
        ('IN PROGRESS', 'IN PROGRESS'),
        ('PENDING', 'PENDING'),
        ('COMPLETED', 'COMPLETED'),
    )
    status = models.CharField(_('Status'), max_length=50, choices=STATUS , null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)


    def __str__(self):
        return self.project_id

    class Meta:
        db_table = "TASKS"
        verbose_name = "Task"
        verbose_name_plural = "TASKS"   




class ToDoList (models.Model):
    id =models.AutoField(primary_key=True )
    user_id = models.CharField(max_length=50 , null=True)
    title = models.CharField(max_length=50 , null=True , blank=True)
    STATUS = (
        ('HOLD-FOR-NOW', 'HOLD-FOR-NOW'),
        ('DONE', 'DONE'),
        ('HOLD-FOR-NOW', 'HOLD_FOR_NOW'),
    )
    status = models.CharField(_('Status'), default="HOLD_FOR_NOW" , max_length=50, choices=STATUS , null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)



    def __str__(self):
        return self.title

    class Meta:
        db_table = "TODOLISTS"
        verbose_name = "ToDoList"
        verbose_name_plural = "TODOLISTS"  


class TrackingModel(models.Model):

    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True


class Thread(TrackingModel):

    THREAD_TYPE = (
        ('personal' , 'Personal'),
        ('group' , 'Group'),
    )
    name = models.CharField(max_length = 50 , null=True , blank=True)
    thread_type = models.CharField(max_length =15 , choices= THREAD_TYPE , default = 'group' )
    users = models.ManyToManyField(NewUser)
    # users = models.ManyToManyField('auth.User')

    objects = ThreadManager()

    def __str__(self) -> str:
        if self.thread_type == 'personal' and self.users.count() == 2:
            return f'{self.users.first()} and {self.users.last() }'

        return f'{self.name}'



class Message(TrackingModel):
    thread = models.ForeignKey(Thread , on_delete= models.CASCADE)
    sender = models.ForeignKey(NewUser , on_delete= models.CASCADE)
    text = models.TextField(blank=False , null= False)

    def __str__(self) -> str:
        return f'From <Other - {self.thread}>'

    
class ChatMessage (models.Model):
    id =models.AutoField(primary_key=True )
    sender_id = models.CharField(max_length=50 , null=True)
    receiver_id = models.CharField(max_length=50 , null=True)
    text = models.TextField(blank=False , null= False)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now = True)
    is_seen = models.BooleanField(default = False)



    def __str__(self):
        return str(self.id )+ " " + self.text

    # create a method that will override the save method , this method will be called when a data saved in this model.

    def save(self , *args , **kwargs):
        print("ChatMessage Saved ")
        print(self.sender_id)
        print(self.receiver_id)
        print(self.text)

        super(ChatMessage , self).save(*args , **kwargs)

        # data = {}
        channel_layer = get_channel_layer()
        chat_message_count = ChatMessage.objects.filter(sender_id = self.sender_id , receiver_id = self.receiver_id).count()

        # chat_message_obj = ChatMessage.objects.filter(sender_id = self.sender_id , receiver_id = self.receiver_id)

        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        chat_message_obj = ChatMessage.objects.filter( receiver_id = self.receiver_id, created_at__gte=today, created_at__lt=tomorrow)

        # print("The length of the chat_message_object is" , len(chat_message_obj))

        test_list = []
        for c in chat_message_obj:
            # print(c.id)
            # print(c.sender_id)
            sndr_usr_name = NewUser.objects.filter(id = c.sender_id)
            for u in sndr_usr_name:
                uname = u.user_name
            # print(c.receiver_id)
            # print(c.text)
            # test_list.append(c.text)
        created_time = self.created_at


        data = {'sender_name':uname , 'created_time': str(created_time), 'receiver_id':self.receiver_id , 'currrent_message':self.text}

        # data = {'chat_message_obj':test_list}
        # data = {'sender_id':self.sender_id , 'receiver_id':self.receiver_id, 'currrent_message':self.text}

        async_to_sync(channel_layer.group_send)(
            'broadcast',
            {
                "type":"websocket.message",
                "value":json.dumps(data)
            }
        )






    class Meta:
        db_table = "CHAT_MESSAGES"
        verbose_name = "ChatMessage"
        verbose_name_plural = "CHAT_MESSAGES"         