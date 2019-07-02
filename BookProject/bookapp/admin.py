from django.contrib import admin
from .models import Books,BorrowBook,UserBookComment,BookClasses

# Register your models here.



admin.site.register(Books)
admin.site.register(BorrowBook)
admin.site.register(UserBookComment)
admin.site.register(BookClasses)

