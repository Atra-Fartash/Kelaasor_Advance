from course.models import Category, Teacher, Course, Comment, Profile, BasketItem, Transaction, Ticket, TicketMessage
from rest_framework.serializers import ModelSerializer


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'description']


class TeacherSerializer(ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['name', 'picture', 'linkedin']


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ['title', 'course_type', 'price', 'description', 'category',
                  'start_date', 'duration', 'picture', 'files', 'register_deadline',
                  'class_link', 'access_expiration', 'offline_video']


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['user', 'date', 'text', 'course']


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'phone_number', 'email', 'date_of_birth']


class BasketItemSerializer(ModelSerializer):
    class Meta:
        model = BasketItem
        fields = ['owner', 'course', 'basket', 'created_at']


class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['user', 'amount', 'date', 'payment_code']


class TicketSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['user', 'title', 'description', 'status', 'section', 'created_at']


class TicketMessageSerializer(ModelSerializer):
    class Meta:
        model = TicketMessage
        fields = ['ticket', 'sender', 'message', 'created_at']