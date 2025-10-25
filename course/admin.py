from django.contrib import admin
from course.models import Category, Teacher, Course,  Comment, Profile, Basket, BasketItem, Wallet, Transaction, Ticket, TicketMessage

class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'course_type', 'price']
    search_fields = ['title']
    list_filter = ['category']


admin.site.register(Category)
admin.site.register(Teacher)
admin.site.register(Course, CourseAdmin)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Basket)
admin.site.register(BasketItem)
admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(Ticket)
admin.site.register(TicketMessage)