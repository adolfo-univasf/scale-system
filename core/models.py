from django.db import models
from accounts.models import fill_database as us_fill
from ministries.models import fill_database as mn_fill
from programs.models import fill_database as pg_fill
# Create your models here.

def fill_database():
    us_fill()
    mn_fill()
    pg_fill()
