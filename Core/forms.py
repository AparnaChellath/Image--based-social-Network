from django import forms
from django.contrib.auth.models import User
from Core.models import Profile,PostModel,Comment

class SignUpForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["username","email","password"]
        widgets={
            "username":forms.TextInput(attrs={"class":"form-control","placeholder":"Username"}),
            "email":forms.EmailInput(attrs={"class":"form-control","placeholder":"Email"}),
            "password":forms.PasswordInput(attrs={"class":"form-control","placeholder":"Password"}),
            
        }

class SignInForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["username","password"]
        widgets={
            "username":forms.TextInput(attrs={"class":"form-control","placeholder":"Username"}),
            "password":forms.PasswordInput(attrs={"class":"form-control","placeholder":"Password"})
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=["dob","gender","bio","profile_picture"]
        widgets={
            "dob":forms.DateInput(attrs={"class":"form-control","placeholder":"Dob"}),
            "gender":forms.Select(attrs={"class":"form-control","placeholder":"gender"}),
            "bio":forms.TextInput(attrs={"class":"form-control","placeholder":"bio"}),
            "profile_picture":forms.FileInput(attrs={"class":"form-control","placeholder":"File"}),
        }

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=["dob","gender","bio","profile_picture"]
        widgets={
            "dob":forms.DateInput(attrs={"class":"form-control","placeholder":"Dob"}),
            "gender":forms.Select(attrs={"class":"form-control","placeholder":"gender"}),
            "bio":forms.TextInput(attrs={"class":"form-control","placeholder":"bio"}),
            "profile_picture":forms.FileInput(attrs={"class":"form-control","placeholder":"File"}),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model=PostModel
        fields=["image","caption"]
        widgets={
            "image":forms.FileInput(attrs={"class":"form-control","placeholder":"File"}),
            "caption":forms.TextInput(attrs={"class":"form-control","placeholder":"Caption"}),
            # "hashtags":forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter hashtags separated by commas, e.g., #coding, #django'}),

        }

class PostEditForm(forms.ModelForm):
    class Meta:
        model=PostModel
        fields=["image","caption"]
        widgets={
            "image":forms.FileInput(attrs={"class":"form-control","placeholder":"File"}),
            "caption":forms.TextInput(attrs={"class":"form-control","placeholder":"Caption"})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=["content"]
        widgets={
            "content":forms.TextInput(attrs={"class":"form-control","placeholder":"Comment"})
        }