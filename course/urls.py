from django.urls import path
from course.views import (CategoryListCreate, CategoryRetrieveUpdateDestroy, TeacherListCreate, TeacherRetrieveUpdateDestroy,
                          CourseListCreate, CourseRetrieveUpdateDestroy, CommentListCreate, CommentRetrieveUpdateDestroy, ProfileListCreate,
                          ProfileRetrieveUpdateDestroy, TicketListCreate, TicketRetrieveUpdateDestroy, TicketMessageListCreate,
                          TicketMessageRetrieveUpdateDestroy, AddBasketItem, BasketItemList, DeleteBasketItem, TransactionView,
                          GroupMemberListCreate, GroupMemberRetrieveUpdateDestroy, DiscountAPIView) 



urlpatterns = [
    path('category-list-create', CategoryListCreate.as_view()),
    path('category-retrieve-update-destroy/<str:pk>', CategoryRetrieveUpdateDestroy.as_view()),
    path('teacher-list-create', TeacherListCreate.as_view()),
    path('teacher-retrieve-update-destroy/<str:pk>', TeacherRetrieveUpdateDestroy.as_view()),
    path('course-list-create', CourseListCreate.as_view()),
    path('course-retrieve-update-destroy/<str:pk>', CourseRetrieveUpdateDestroy.as_view()),
    path('group-member-list-create', GroupMemberListCreate.as_view()),
    path('group-member-retrieve-update-destroy/<str:pk>', GroupMemberRetrieveUpdateDestroy.as_view()),
    path('comment-list-create', CommentListCreate.as_view()),
    path('comment-retrieve-update-destroy/<str:pk>', CommentRetrieveUpdateDestroy.as_view()),
    path('profile-list-create', ProfileListCreate.as_view()),
    path('profile-retrieve-update-destroy/<str:pk>', ProfileRetrieveUpdateDestroy.as_view()),
    path('Ticket-list-create', TicketListCreate.as_view()),
    path('ticket-retrieve-update-destroy/<str:pk>', TicketRetrieveUpdateDestroy.as_view()),
    path('ticket-message-list-create', TicketMessageListCreate.as_view()),
    path('ticket-message-retrieve-update-destroy/<str:pk>', TicketMessageRetrieveUpdateDestroy.as_view()),
    path('add-to-basket', AddBasketItem.as_view()),
    path('basket-item-list', BasketItemList.as_view()),
    path('basket-item-delete/<str:pk>', DeleteBasketItem.as_view()),
    path('new-transaction', TransactionView.as_view()),
    path('discount/', DiscountAPIView.as_view())
]