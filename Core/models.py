from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob=models.DateField()
    choice = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
    ]

    gender = models.CharField(max_length=1, choices=choice, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='media', blank=True, null=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)

    def __str__(self):
        return self.user.username
    
    def followers_count(self):
        return self.followers.all().count()
    


    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)

    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.profile.save()



class PostModel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to="media")
    caption=models.CharField(max_length=100)
    date=models.DateField(auto_now_add=True)
    like=models.ManyToManyField(User,related_name="like")
    hashtags = models.ManyToManyField('Hashtag', blank=True)

class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
      

class Comment(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.user.username} on {self.post.id}"


class SavedPost(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='saved_posts')
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.user.username} saved {self.post.id}"

