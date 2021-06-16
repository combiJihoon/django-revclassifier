from django.contrib import admin
from .models import UserInput, CrawlResult
# Register your models here.
admin.site.register(UserInput)
admin.site.register(CrawlResult)
