from functools import partial
from django.contrib import admin

# Register your models here.

from .models import AdminUser
from .models import Event
from .models import CalendarDate
from .models import AvailableSlote
from .models import Participant


admin.site.register(AdminUser)
admin.site.register(Event)
admin.site.register(CalendarDate)
admin.site.register(AvailableSlote)
admin.site.register(Participant)
