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
    path('profile/<str:username>/', views.ProfileView.as_view(), name='profile'),
    # path('profile/<str:pk>/<str:post_id>', views.ProfilePostView.as_view(), name='profile_post'),
    path('edit-post/<str:post_id>/', views.EditPost.as_view(), name='edit-post'),
    path('like-post', views.LikePost.as_view(), name='like-post'),
    path('delete-post', views.DeletePost.as_view(), name='delete-post'),
    path('disable-post-comments', views.DisablePostComments.as_view(), name='disable-post-comments'),
    path('enable-post-comments', views.EnablePostComments.as_view(), name='enable-post-comments'),
    # path('edit-post', views.Likepost.as_view(), name='like-post'),
    path('add-comment', views.AddComment.as_view(), name='add-comment'),
    path('like-comment', views.Likecomment.as_view(), name='like-comment'),
    # < a href = "/like-post?post_id={{post.id}}" class ="flex items-center space-x-2" >
    # < a href = "/like-comment?comment_id={{post.id}}" class ="flex items-center space-x-2" >
    # path('follow', views.Follow.as_view(), name='follow'),
    path('search', views.Search.as_view(), name='search'),
    path('dialogs/', views.DialogsView.as_view(), name='dialogs'),
    path('dialogs/create/<int:user_id>/', views.CreateDialogView.as_view(), name='create_dialog'),
    path('dialogs/<int:chat_id>', views.MessagesView.as_view(), name='messages'),
]