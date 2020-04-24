from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.index, name='home'),
    path('signup', views.signup, name='signup'),
    path('success', TemplateView.as_view(template_name='thank_you.html'), name='thank_you'),
    path('logged_out', TemplateView.as_view(template_name='check_again.html'), name='logged_out'),
    path('create', views.create_post, name='create'),
    path('delete/<int:pk>/', views.delete_post, name='delete'),
    path('edit/<int:pk>/', views.edit_post, name='edit'),
    path('comment/<int:pk>/', views.create_comment, name='comment'),
    path('like/<int:pk>/', views.like_post, name='likes'),
    path('search/', views.search_friends, name='search'),
    path('send_request/<user_profile>/', views.add_friend_request, name='add_friend'),
    path('cancel_request/<user_profile>/<int:pk>/', views.cancel_friend_request, name='cancel_friend'),
    path('notifications', views.notification, name='notification'),
    path('notifications/detail/<int:pk>/', views.notification_detail, name='detail'),
    path('accept_friend/<user_profile>/<int:pk>/', views.accept_friend, name='accept'),
    path('del_note/<int:pk>/', views.delete_notification, name='del_note'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('profile_detail/<user_profile>/', views.profile_details, name='profile_detail'),
    path('canceled_request/<user_profile>/', views.cancel_friend_sent, name='canceled_request'),
    path('create_group', views.create_group, name='group'),
    path('group_details/<int:pk>/', views.group_details, name='group_detail'),
    path('create_group_post/<int:pk>/', views.group_form, name='group_post'),
    path('join_group/<int:pk>/', views.join_group, name='join_group'),
    path('leave_group/<int:pk>/', views.leave_group, name='leave_group'),
    path('delete_group/<int:pk>/', views.delete_group, name='delete_group'),
    path('comment_post/<int:pk>/', views.show_comments, name='comment_post'),
    path('people', views.people_you_know, name='people')

]
