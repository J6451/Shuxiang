from django.contrib import admin
from .models import BookUser,BookBeanCredit,BookBeanCreditStatistics
# Register your models here.


admin.site.register(BookUser)
admin.site.register(BookBeanCredit)
admin.site.register(BookBeanCreditStatistics)
