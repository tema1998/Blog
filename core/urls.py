from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('signup', views.Signup.as_view(), name='signup'),
    path('signin', views.Signin.as_view(), name='signin'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('settings', views.Settings.as_view(), name='settings'),
    path('user/follow/<int:user_id>/', views.ProfileFollowingCreateView.as_view(), name='follow'),
    # path('profile/<str:pk>', views.profile, name='profile'),
    path('profile/<str:username>/', views.ProfileView.as_view(), name='profile'),
    path('add-remove-favorites/<str:post_id>/', views.AddRemoveFavoritePost.as_view(), name='add-remove-favorites'),
    path('favorites-posts', views.FavoritesPosts.as_view(), name='favorites-posts'),
    path('followers', views.FollowersList.as_view(), name='followers'),
    path('following', views.FollowingList.as_view(), name='following'),
    # path('profile/<str:pk>/<str:post_id>', views.ProfilePostView.as_view(), name='profile_post'),
    path('add-post', views.AddPost.as_view(), name='add-post'),
    path('edit-post/<str:post_id>/', views.EditPost.as_view(), name='edit-post'),
    path('like-post', views.LikePost.as_view(), name='like-post'),
    path('delete-post', views.DeletePost.as_view(), name='delete-post'),
    path('disable-post-comments', views.DisablePostComments.as_view(), name='disable-post-comments'),
    path('enable-post-comments', views.EnablePostComments.as_view(), name='enable-post-comments'),
    # path('edit-post', views.Likepost.as_view(), name='like-post'),
    path('add-comment', views.AddComment.as_view(), name='add-comment'),
    path('like-comment', views.Likecomment.as_view(), name='like-comment'),
    # path('follow', views.Follow.as_view(), name='follow'),
    path('search', views.Search.as_view(), name='search'),
]