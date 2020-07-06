from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db.models.deletion import CASCADE
from django.core.validators import MinValueValidator, RegexValidator
from django.urls import reverse

# Create your models here.
class MyProfile(models.Model):
    name = models.CharField(max_length = 100)
    user = models.OneToOneField(to = User, on_delete= CASCADE)
    age = models.IntegerField(default=18, validators= [MinValueValidator(10)])
    address = models.TextField(null=True, blank=True)
    status = models.CharField(max_length =20, default = "single", choices= (("single","single"),("married","married")))
    gender = models.CharField(max_length =20, default = "female", choices= (("male","male"),("female","female"),("other","other")))
    phone_no = models.CharField(validators =[RegexValidator("^0?[5-9]{1}\\d{9}$")],max_length=15,null=True, blank=True,unique =True)
    description = models.TextField(null= True, blank= True)
    profilepic= models.ImageField(default='default.jpg',upload_to='profilepics')
    def __str__(self):
        return f'{self.user.username}Profile'

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
    @property
    def profilepic_url(self):
        if self.profilepic and hasattr(self.profilepic, 'url'):
            return self.profilepic.url


class MyPost(models.Model):
    title = models.CharField(max_length=200)
    content= models.TextField(null=False ,unique =True)
    likes = models.ManyToManyField(User, default=None, blank = True,related_name="liked")
    images = models.ImageField(upload_to='images',null = True, blank=True)
    category = models.CharField(max_length=100,default="Articles",choices= (("Articles","Articles"),("Poetry","Poetry"),("Shayaries","Shayaries"),("Stories","Stories"),("Jokes","Jokes"),("Other","Other")))
    cr_date = models.DateTimeField(auto_now_add = True)
    author = models.ForeignKey(User,null=True, blank=True,  on_delete=CASCADE)
    flag = models.CharField(max_length =20, null=True, blank = True, choices= (("abusing","abusing"),("nudity","nudity"),("violence","violence"),("Harassment","Harassment"),("False News","False News"),("Terrorism","Terrorism"),("Something Else","Something Else"),("Spam","Spam")))
    def __str__(self):
        return "%s" % self.title
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    @property
    def images_url(self):
        if self.images and hasattr(self.images, 'url'):
            return self.images.url
    @property    
    def num_likes(self):
        return self.liked.all().count()

LIKE_CHOICES=(
    ('Like', 'Like'),
    ('Unlike','Unlike'),
)
class PostLike(models.Model):
    post = models.ForeignKey(to=MyPost, on_delete=CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value=models.CharField(choices=LIKE_CHOICES, default="Like", max_length=10)
    cr_date = models.DateTimeField(auto_now_add = True)   
    
    def __str__(self):
        return "%s" % self.post
    

class PostComment(models.Model):
    post = models.ForeignKey(to=MyPost, on_delete=CASCADE)
    msg= models.TextField()
    user =models.ForeignKey(User,on_delete = models.CASCADE)
    parent=models.ForeignKey('self',on_delete=CASCADE, null=True)
    cr_date = models.DateTimeField(auto_now_add = True)
    flag = models.CharField(max_length =20, null=True, blank = True, choices= (("abusing","abusing"),("racist","racist"),("Hate Speech","Hate Speech")))
    
    def __str__(self):
        return "%s" % self.msg



class FollowUser(models.Model):
    profile = models.ForeignKey(to=MyProfile, on_delete=CASCADE,related_name ="profile_by")
    followed_by = models.ForeignKey(to=MyProfile, on_delete=CASCADE, related_name="followed_by")
    def __str__(self):
        return "%s is followed_by %s" % (self.profile,self.followed_by)

class Contact(models.Model):
    sno =models.AutoField(primary_key=True)  
    name = models.CharField(max_length=225)  
    email =models.CharField(max_length=100)  
    msg =models.TextField()  
    cr_date = models.DateTimeField(auto_now_add = True) 

