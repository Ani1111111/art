from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from articles import views
from django.views.generic.base import RedirectView


urlpatterns =[
    path('home/', views.MyPostListView.as_view(),name='post-list'),
    path('myposts/', views.MyPostsListView.as_view()),
    path('contact', views.contact),
    path('postreport', views.postreport,name = "post-report"),
    path('post/<int:pk>/', views.MyPostDetailView.as_view(), name= 'post-detail'),
    path('myprofile/<int:pk>/', views.MyProfileDetailView.as_view(), name= 'profile-detail'),
    path('mypost/<int:pk>/update/', views.MyPostUpdateView.as_view(), name= 'post-update'),
    path('mypost/delete/<int:pk>/', views.MyPostDeleteView.as_view(success_url = "/articles/home")),
    path('like/',views.like_post,name='like-post'),
    # api to post a comment
    path('sendcomment/',views.SendComment, name='sendcomment'),
    path('postcomment/delete/<int:pk>/', views.PostCommentDeleteView.as_view(success_url = "/articles/home")),
    path('about/', views.AboutView.as_view()),
    path('faq/', views.faq,name='faq'),
    path('disclaimer/', views.DisclaimerView.as_view()),
    path('privacypolicy/', views.PrivacyPolicyView.as_view()),
    path('customersupport/', views.CustomerSupportView.as_view()),
    path('termsandconditions/', views.TermsAndConditionsView.as_view()),
    path('',RedirectView.as_view(url="home/")),
    path('profile/edit/<int:pk>', views.MyProfileUpdateView.as_view(success_url="/articles/home")),
    path('mypost/create/',views.MyPostCreate.as_view(success_url='/articles/home')),
]


