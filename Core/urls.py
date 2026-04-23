from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views

if settings.DEBUG:
        urlpatterns=[
                path("",views.Home.as_view(),name="home_view"),
                path("signup",views.SignUpview.as_view(),name="signup_view"),
                path("signin",views.SignInView.as_view(),name="signin_view"),
                path("signout",views.SignOutView.as_view(),name="signout_view"),
                path("profile",views.ProfileView.as_view(),name="profile_view"),
                path("login",views.LoginView.as_view(),name="login_view"),
                path("profileList",views.ProfileListView.as_view(),name="proflist_view"),
                path("profileEdit/<int:id>",views.ProfileEditView.as_view(),name="profedit_view"),
                path("profileDel/<int:id>",views.ProfileDeleteView.as_view(),name="profdel_view"),
                path("profilesettings",views.SettingsView.as_view(),name="profsettings_view"),
                path("Detail/<int:id>",views.ProfileDEtailView.as_view(),name="detail_view"),
                path("PostCreate",views.PostView.as_view(),name="post_create_view"),
                path("PostList",views.PostListView.as_view(),name="post_list_view"),
                path("PostEdit/<int:id>",views.PostEditView.as_view(),name="post_edit_view"),
                path("PostDel/<int:id>",views.PostDeleteView.as_view(),name="post_del_view"),
                path("Feed/",views.FeedView.as_view(),name="feed_view"),
                path("Like/<int:id>/",views.LikePostView.as_view(),name="liked_view"),
                path("post/<int:id>",views.CommentView.as_view(),name="comment_create_view"),
                # path('follow/<str:username>/', views.follow_user, name='follow_user'),
                path('profile/<str:username>/', views.profile_view, name='profile_view'),
                path('search/', views.search_users, name='search_users'),
                path('commentlist/<int:id>', views.CommentListView.as_view(), name='comment_list'),
                path('save-post/<int:post_id>/',views.SavePostView.as_view(), name='save_post'),
                path('saved-posts/', views.SavedPostsListView.as_view(), name='saved_posts_list'),
                path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
                path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
                path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
                path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


                # path('password/reset',auth_views.PasswordResetView.as_view(template_name="password_reset_form.html"),name="password_reset"),
                # path('password/reset_done/',auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"),name="password_reset_done"),
                # path('password/reset/confirm/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"),name="password_reset_confirm"),
                # path('password/reset/complete/',auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),name="password_reset_complete"),
                # path('follow/<str:username>/', views.FollowToggleView.as_view(), name='follow_toggle'),
                # path('Follow/<str:username>/',views.AddFollowers.as_view(),name="follow_vew")

                
        ] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)