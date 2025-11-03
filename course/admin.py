from django.contrib import admin
from course.models import Category, Teacher, Course,  Comment, Profile, Basket, BasketItem, Wallet, Transaction, Ticket, TicketMessage, Discount

class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'course_type', 'price']
    search_fields = ['title']
    list_filter = ['category']


class DiscountAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_type', 'value', 'is_active']
    list_filter = ['discount_type', 'is_active']


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
admin.site.register(Discount, DiscountAdmin)