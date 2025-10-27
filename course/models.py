from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(null=True, blank=True)
    linkedin = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name
    

class Course(models.Model):

    COURSE_TYPE_CHOICES=[
        ('1', 'online'),
        ('2', 'offline'),
    ]

    title = models.CharField(max_length=100)
    course_type = models.CharField(max_length=1, choices=COURSE_TYPE_CHOICES)
    price = models.PositiveIntegerField()
    description = models.TextField()
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    start_date = models.DateField()
    duration = models.DurationField()
    picture = models.ImageField(null=True, blank=True)
    files = models.FileField(null=True, blank=True)
    #for online courses:
    register_deadline = models.DateField(null=True, blank=True)  
    class_link = models.URLField(null=True,blank=True)
    #for offline courses:
    access_expiration = models.DateField(null=True, blank=True)
    offline_video = models.FileField(null=True,blank=True)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateField()
    text = models.TextField()
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} | course : {self.course.name} | comment : {self.text} | time : {self.date}'
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11, null=True,blank=True)
    email = models.EmailField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)


class Basket(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.PositiveBigIntegerField()
    discount = models.PositiveBigIntegerField(default=0)
    final_price = models.PositiveBigIntegerField()
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class BasketItem(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class OTP(models.Model):
    otp = models.IntegerField()
    phone_number = models.CharField(max_length=12)
    expire_date = models.DateTimeField(null=True, blank=True)


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.PositiveBigIntegerField()


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveBigIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    payment_code = models.CharField(max_length=20)


class Ticket(models.Model):

    STATUS_CHOICES=[
        ('1', 'open'),
        ('2', 'in progress'),
        ('3', 'closed'),
    ]

    SECTION_CHOICES=[
        ('1', 'مالی'),
        ('2', 'پشتیبانی'),
        ('3', 'آموزشی')
    ]

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    section = models.CharField(max_length=1, choices=SECTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)


class TicketMessage(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    sender = models.ForeignKey(to=User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)