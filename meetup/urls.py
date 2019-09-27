from django.urls import path

from meetup import views

urlpatterns = [
    path('user', views.UserList.as_view(), name='user'),
    path('user/<str:pk>/', views.UserDetail.as_view(), name='userDetail'),
    path('room', views.RoomList.as_view(), name='room'),
    path('room/<str:pk>/', views.RoomDetail.as_view(), name='roomDetail'),
    path('addmember/', views.add_member_to_room, name='addMember'),
    path('userinstance/', views.UserInstanceList.as_view(), name='userInstance'),
    path('userinstance/<int:pk>', views.UserInstanceDetail.as_view(), name='userInstanceDetail')
]
