from django.shortcuts import render,redirect
from django.views.generic import TemplateView,CreateView,ListView,UpdateView,DetailView,FormView
from Core.forms import SignUpForm,SignInForm,ProfileForm,ProfileEditForm,PostForm,PostEditForm,CommentForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views import View
from Core.models import Profile,PostModel,Comment,SavedPost
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.decorators import method_decorator
# Create your views here.

class Home(TemplateView):
    template_name="index.html"

class SignUpview(CreateView):
    form_class=SignUpForm
    template_name='signup.html'
    model=User
    # success_url=reverse_lazy('signin_view')

    def form_valid(self,form):
        print(form.cleaned_data)
        User.objects.create_user(**form.cleaned_data)
        messages.success(self.request,"registration successfull")
        return redirect('signin_view')
    def form_invalid(self,form):
        messages.warning(self.request,"invalid input")
        return super().form_invalid(form)
    

class SignInView(View):
    def get(self,request):
        form=SignInForm()
        return render(request,'signin.html',{"form":form})
    def post(self,request):
         uname=request.POST.get("username")
         psw=request.POST.get("password")
         user=authenticate(request,username=uname,password=psw)
         if user:
              login(request,user)
              return redirect('profile_view')      
         else:
              messages.warning(request,"invalid username or password")
              return redirect('signin_view')
         
class SignOutView(View):
     def get(self,request):
          logout(request)
          return redirect('signin_view')
         
class LoginView(TemplateView):
     template_name="login.html"


     
class ProfileView(CreateView):
     form_class=ProfileForm
     template_name="profile.html"

     def form_valid(self, form):
            profile = form.save(commit=False)
            profile.user = self.request.user  
            profile.save()
            return redirect("login_view")
     
class ProfileListView(ListView):
     template_name="Home.html"
     model=Profile
     context_object_name="profile"

     def get_queryset(self):
          return Profile.objects.filter(user=self.request.user)
     
     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = PostModel.objects.filter(user=self.request.user)
        return context

     
class ProfileEditView(UpdateView):
     form_class=ProfileEditForm
     template_name='profile_edit.html'
     model=Profile
     pk_url_kwarg="id"
     success_url=reverse_lazy('proflist_view')

class ProfileDeleteView(View):
     def get(self,request,*args,**kwargs):
          profile=Profile.objects.get(id=kwargs.get("id"))
          profile.delete()
          return redirect('profile_view')
     
class SettingsView(TemplateView):
     template_name="settings.html"
     model=Profile
     context_object_name="profile"
     pk_url_kwarg="id"

class ProfileDEtailView(DetailView):
     template_name="profile_view.html"
     model=Profile
     pk_url_kwarg="id"
     context_object_name="profile"


class PostView(CreateView):
     form_class=PostForm
     template_name="post_create.html"

     def form_valid(self, form):
            post = form.save(commit=False)
            post.user = self.request.user  
            post.save()
            return redirect("home_view")
     
class PostListView(ListView):
    template_name = "Home.html"
    model = PostModel
    context_object_name = "posts"

    def get_queryset(self):
        return PostModel.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.filter(user=self.request.user)
        return context
    
    

class PostEditView(UpdateView):
     form_class=PostEditForm
     template_name='post_edit.html'
     model=PostModel
     pk_url_kwarg="id"
     success_url=reverse_lazy('post_list_view')

class PostDeleteView(View):
     def get(self,request,*args,**kwargs):
          profile=PostModel.objects.get(id=kwargs.get("id"))
          profile.delete()
          return redirect('post_list_view')
     
class FeedView(ListView):
     template_name='Feed.html'
     model=PostModel
     context_object_name="posts"

     def get_queryset(self):
          return PostModel.objects.all()

#like
class LikePostView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(PostModel, id=kwargs.get("id"))

        if request.user in post.like.all():  
            post.like.remove(request.user)
        else:
            post.like.add(request.user)

        return redirect('feed_view')


class FeedView(View):
    def get(self, request, *args, **kwargs):
        posts = PostModel.objects.all()
        for post in posts:
            post.like_count = post.like.count()  
        return render(request, 'feed.html', {'posts': posts})
    
#comment

class CommentView(View):
    def get(self, request, *args, **kwargs):
        form = CommentForm()
        return render(request, 'comment_create.html', {"form": form})

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(PostModel, id=kwargs.get("id"))
        if not request.user.is_authenticated:
            return redirect("login")
        if not hasattr(request.user, "profile"):
            raise ValueError("User does not have an associated profile.")

        profile = request.user.profile 
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data.get("content")
            Comment.objects.create(user=profile, post=post, content=content)
            return redirect("feed_view")

        return render(request, 'comment_create.html', {"form": form})




class CommentListView(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get("id")
        post = get_object_or_404(PostModel, id=id)
        comments = Comment.objects.filter(post=post)
        return render(request, 'comment_list.html', {'comments': comments})

     
    




#search

def profile_view(request, username):
    user = get_object_or_404(User, username=username) 
    return render(request, 'profile_view.html', {'user': user})


@login_required
def search_users(request):
    query = request.GET.get('q', '')
    results = User.objects.filter(
        Q(username__icontains=query) | Q(profile__bio__icontains=query)
    ).exclude(username=request.user.username) 
    return render(request, 'search.html', {'results': results, 'query': query})


#save

class SavePostView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(PostModel, id=post_id)
        saved_post, created = SavedPost.objects.get_or_create(user=request.user.profile, post=post)

        if created:
            messages.success(request, "Post saved successfully!")
        else:
            messages.info(request, "You have already saved this post.")
        return redirect('saved_posts_list') 
    

class SavedPostsListView(LoginRequiredMixin, ListView):
    model = SavedPost
    template_name = 'saved_posts_list.html'
    context_object_name = 'saved_posts'

    def get_queryset(self):
        return SavedPost.objects.filter(user=self.request.user.profile)
    









