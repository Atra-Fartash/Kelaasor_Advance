from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from rest_framework import filters
from course.serializers import CategorySerializer, TeacherSerializer, CourseSerializer, CommentSerializer, ProfileSerializer, BasketItemSerializer, TransactionSerializer, TicketSerializer, TicketMessageSerializer
from course.models import OTP, Basket, BasketItem, Wallet, Category, Teacher, Course, Comment, Profile, Transaction, Ticket, TicketMessage
from rest_framework import permissions



class CategoryListCreate(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name']

    def get_permissions(self):
        if self.request.method == 'POST':
           return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]


class CategoryRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name']

    def get_permissions(self):
        if self.request.method == ['PATCH', 'PUT', 'DELETE']:
           return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
    

class TeacherListCreate(ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name']

    def get_permissions(self):
        if self.request.method == 'POST':
           return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]


class TeacherRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name']

    def get_permissions(self):
        if self.request.method == ['PATCH', 'PUT', 'DELETE']:
           return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
    

class CourseListCreate(ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    filterset_fields = ['category']
    ordering_fields = ['price', 'start_date', 'duration']

    def get_permissions(self):
        if self.request.method == 'POST':
           return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]
    

class CourseRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    filterset_fields = ['category']
    ordering_fields = ['price', 'start_date', 'duration']

    def get_permissions(self):
        if self.request.method == ['PATCH', 'PUT', 'DELETE']:
           return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
    

class CommentListCreate(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Comment.objects.all()
        return Comment.objects.filter(user=user)
    

class ProfileListCreate(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Profile.objects.all()
        return Profile.objects.filter(user=user)
    

class TicketListCreate(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['created_at']


class TicketRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['created_at']


class TicketMessageListCreate(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = TicketMessage.objects.all()
    serializer_class = TicketMessageSerializer


class TicketMessageRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = TicketMessage.objects.all()
    serializer_class = TicketMessageSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.filter(user=user)