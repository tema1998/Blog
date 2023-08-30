from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('signup', views.Signup.as_view(), name='signup'),
    path('signin', views.Signin.as_view(), name='signin'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('settings', views.Settings.as_view(), name='settings'),
    path('upload', views.Upload.as_view(), name='upload'),
    path('user/follow/<str:user_id>/', views.ProfileFollowingCreateView.as_view(), name='follow'),
    # path('profile/<str:pk>', views.profile, name='profile'),
    path('profile/<str:pk>/', views.ProfileView.as_view(), name='profile'),
    path('like-post', views.Likepost.as_view(), name='like-post'),
    path('like-comment', views.Likecomment.as_view(), name='like-comment'),
    # < a href = "/like-post?post_id={{post.id}}" class ="flex items-center space-x-2" >
    # < a href = "/like-comment?comment_id={{post.id}}" class ="flex items-center space-x-2" >
    # path('follow', views.Follow.as_view(), name='follow'),
    path('search', views.Search.as_view(), name='search'),
    path('dialogs/', views.DialogsView.as_view(), name='dialogs'),
    path('dialogs/create/<int:user_id>/', views.CreateDialogView.as_view(), name='create_dialog'),
    path('dialogs/<int:chat_id>', views.MessagesView.as_view(), name='messages'),
]