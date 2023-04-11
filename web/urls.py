from django.urls import path
from web import views

urlpatterns = [
    path("register",views.SignUpView.as_view(),name="register"),
    path("login",views.SigninView.as_view(),name="signin"),
    path("",views.HomeView.as_view(),name="home"),
    path("post/add",views.PostCreateView.as_view(),name="postadd"),
    path("post/all",views.PostListView.as_view(),name="postlist"),
    path("post/<int:id>",views.PostDetailView.as_view(),name="postdetail"),
    path("post/<int:id>/remove",views.PostDeleteView.as_view(),name="postdelete"),
    path("logout",views.sign_out,name="signout")
    
]





 