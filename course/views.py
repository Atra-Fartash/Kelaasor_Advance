from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, serializers, status
from course.serializers import CategorySerializer, TeacherSerializer, CourseSerializer, CommentSerializer, ProfileSerializer, BasketItemSerializer, TransactionSerializer, TicketSerializer, TicketMessageSerializer, GroupMemberSerializer
from course.models import OTP, Basket, BasketItem, Wallet, Category, Teacher, Course, Comment, Profile, Transaction, Ticket, TicketMessage, GroupMembers, Enrollment, Discount
from rest_framework import permissions
import random
from django.core.cache import cache
from rest_framework.response import Response



def _update_basket_price(basket):
    basket.total_price = 0
    basket.save()
    i = 0
    for item in BasketItem.objects.filter(basket=basket):
        basket.total_price = basket.total_price + item.product.price
        i += 1
    basket.save()


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


class GroupMemberListCreate(ListCreateAPIView):
    queryset =  GroupMembers.objects.all()
    serializer_class = GroupMemberSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupMemberRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = GroupMembers.objects.all()
    serializer_class = GroupMemberSerializer
    permission_classes = [permissions.IsAuthenticated]


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


class AddBasketItem(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BasketItemSerializer
    queryset = BasketItem.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        course = serializer.validated_data['course']
        
        if Enrollment.objects.filter(user=user, course=course).exists():
            raise serializers.ValidationError('You have already bought this course.')
        
        basket = Basket.objects.filter(owner=user, is_paid=False)
        if not basket.exists():
            basket = Basket.objects.create(
                owner=self.request.user,
                total_price=0,
                final_price=0,
            )
        else:
            basket = basket.get()
            if basket.items.filter(course=course):
                raise serializers.ValidationError('This course is already in your basket.')
        
        serializer.save(owner=self.request.user, basket=basket)
        _update_basket_price(basket)


class BasketItemList(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BasketItemSerializer
    queryset = BasketItem.objects.all()

    def get_queryset(self):
        return BasketItem.objects.filter(owner=self.request.user)


class DeleteBasketItem(DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BasketItemSerializer
    queryset = BasketItem.objects.all()

    def get_queryset(self):
        return BasketItem.objects.filter(owner=self.request.user)
    

class GetOTP(APIView):

    def post(self, request):
        genrated_otp = random.randint(1000, 9999)
        phone_number = request.data.get("phone_number")
        # SEND OTP TO USER BY SMS
        cache.set(phone_number, genrated_otp, timeout=180)

        # otp_object = OTP.objects.create(
        #     otp = genrated_otp,
        #     phone_number = request.data.get('phone_number'),
        # )
        # SEND OTP TO USER BY SMS
        # otp_object.expire_date = now() + timedelta(seconds=180)
        # otp_object.save()
        return Response("OTP sent!")


class CheckOTP(APIView):

    def post(self, request):
        input_otp = request.data.get("otp")
        input_phone_number = request.data.get("phone_number")
        saved_otp = cache.get(input_phone_number)
        # saved_otp = OTP.objects.get(phone_number=input_phone_number)
        # if saved_otp.otp == input_otp and saved_otp.expire_date >= now():
        #     saved_otp.delete()
        #     return Response('OK')
        # else:
        #     return Response('Something is wrong!')
    

class TransactionView(CreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def perform_create(self, serializer):
        user_wallet = Wallet.objects.get(user=self.request.user)
        wallet_amount = user_wallet.amount
        serializer.save(
            user=self.request.user,
            payment_code=random.randint(1000, 9999),
            payment_type="b",
            amount=(
                serializer.validated_data["amount"]
                if serializer.validated_data["amount"] < wallet_amount
                else wallet_amount
            ),
        )


class DiscountAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        code_str = request.data.get('code')
        if not code_str:
            return Response({'detail': 'No discount code provided'}, status=400)
        
        try:
            discount = Discount.objects.get(code = code_str)
        except Discount.DoesNotExist:
            return Response({'detail' : 'Invalid discount code'}, status=400)
        
        if discount.discount_type == 'percent':
            discount_amount = Basket.total_price * (discount.value / 100)
        else:
            discount_amount = discount.value
        
        Basket.discount = discount
        Basket.final_price = max(Basket.total_price - discount_amount, 0)
        Basket.save()
        discount.usage_count += 1
        discount.save()
        return Response({
            'detail' : 'Discount code applied successfully',
            'discount' : discount.code,
            'final_price' : Basket.final_price
        }, status=200)