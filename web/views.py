from django.shortcuts import render,redirect
from api.models import Posts
from django.views.generic import CreateView,FormView,TemplateView,ListView,DetailView,View
from django.urls import reverse_lazy
from web.forms import RegistrationForm,LoginForm,PostForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
# Create your views here.


def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid seesion")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

decs=[signin_required,never_cache]

class SignUpView(CreateView):
    template_name="signup.html"
    form_class=RegistrationForm
    success_url=reverse_lazy("signin")

    def form_valid(self, form):
        messages.success(self.request,"account created success fully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,"account creation failed")

        return super().form_invalid(form)


class SigninView(FormView):
    template_name="signin.html"
    form_class=LoginForm
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("home")
            else:
                messages.error(request,"invalid credentials")
                return render(request,"signin.html",{"form":form})

@method_decorator(signin_required,name="dispatch")
class HomeView(ListView):
    template_name="base.html"
    context_object_name="posts"
    model=Posts

@method_decorator(signin_required,name="dispatch")
class PostCreateView(CreateView):
    template_name="postadd.html"
    form_class=PostForm
    success_url=reverse_lazy("postlist")

    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,"post added ")
        return super().form_valid(form)    
    
@method_decorator(signin_required,name="dispatch")
class PostListView(ListView):
    model=Posts
    template_name="postlist.html"
    context_object_name="todos"
    def get_queryset(self):
        return Posts.objects.filter(user=self.request.user)    

@method_decorator(signin_required,name="dispatch")    
class PostDetailView(DetailView):
    model=Posts
    template_name="postdetail.html"  
    context_object_name="todo"
    pk_url_kwarg="id" 


@method_decorator(signin_required,name="dispatch")
class PostDeleteView(View):
    def get(self,request,*args,**kw):
        id=kw.get("id")
        Posts.objects.get(id=id).delete()
        messages.success(self.request,"post deleted")
        return redirect("postlist")        
    


@signin_required
def sign_out(request,*args,**kw):
    logout(request)
    return redirect("signin")        