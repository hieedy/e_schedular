from django.db import models

# Create your models here.

class AdminUser(models.Model):
    first_name = models.CharField(max_length = 50, null=True, blank=True)
    last_name = models.CharField(max_length = 50, null=True, blank=True)
    email_id = models.EmailField()
    
    profile_picture = models.ImageField(upload_to = 'AdminUserImages/', blank = True, null= True )
    password = models.CharField(max_length = 20)
    gender = models.CharField(
        max_length = 1,
        choices = [('m','male'),('f','female'), ('o', 'others')],
        default = 'm'
    )
    def __str__(self):
        return self.email_id


class Event(models.Model):
    event_created_date  = models.DateField() 
    user_id = models.ForeignKey(AdminUser, on_delete=models.CASCADE)
    unique_link = models.URLField()
    event_agenda = models.CharField(max_length=100, default="Meeting")
    
    def __str__(self):
        return self.user_id.email_id

class CalendarDate(models.Model):
    Event_id = models.ForeignKey(Event, on_delete = models.CASCADE)
    date = models.DateField() 

class AvailableSlote(models.Model):
    calendardates_id = models.ForeignKey(CalendarDate, on_delete = models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.BooleanField()
    zoomlink = models.URLField()

class Participant(models.Model):
    availableslotes_id = models.ForeignKey(AvailableSlote, on_delete= models.CASCADE)
    email_id = models.EmailField()

    