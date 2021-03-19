from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
from django.forms import ModelForm


class User(AbstractUser):
    pass

class Post(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_content = models.TextField(max_length=200)
    post_time = models.DateTimeField(auto_now=True)

    def serialize(self):
        return{
            "id":self.id,
            "poster":self.user_id.username,
            "content":self.post_content
        }

class Like(models.Model):
    liker_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)

    def serialize(self):
        return{
            "id":self.id,
            "liker":self.liker_id.username,
            "post":self.post_id
        }

class Follower(models.Model):
    follow_initiator = models.ForeignKey(User, related_name='initiator', on_delete=models.CASCADE)
    follow_reciever = models.ForeignKey(User, related_name='reciever', on_delete=models.CASCADE)
    
    def serialize(self):
        return{
            "id":self.id,
            "initiator":self.initiator.username,
            "reciever":self.reciever.username
        }
    
class FollowerForm(ModelForm):
    class Meta:
        model = Follower
        fields = ['follow_initiator', 'follow_reciever']