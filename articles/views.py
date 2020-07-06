from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from articles.models import MyProfile, MyPost,FollowUser,PostComment,PostLike,Contact
from django.views.generic.detail import DetailView
from django.db.models import Q
from django.views.generic.edit import UpdateView, CreateView,DeleteView
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponse
from django.contrib import messages
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from articles.templatetags import extras
   

# Create your views here
    
def home(request,slug):
    context = {
        'posts': posts,
        'comments':comments,
        'replyDict':replyDict,
        
    } 
    
    return render(request,'articles/home.html',context)

@method_decorator(login_required, name = "dispatch")
class MyPostListView(ListView):
    model =MyPost
    template_name = 'articles/home.html'
    context_object_name = 'posts'
    ordering = ['-cr_date']
    paginate_by=15

    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(*args, **kwargs)
        query = self.request.GET.get('query')
        if query == None:
            query = ""
            context['posts'] = MyPost.objects.all().order_by("-id")
        elif query == "carticles":
            context['posts'] = MyPost.objects.filter(category__icontains="articles").order_by("-id")
        elif query == "cpoetry":
            context['posts'] = MyPost.objects.filter(category__icontains="poetry").order_by("-id")
        elif query == "cstories":
            context['posts'] = MyPost.objects.filter(category__icontains="stories").order_by("-id")
        elif query == "cshayaries":
            context['posts'] = MyPost.objects.filter(category__icontains="shayaries").order_by("-id")
        elif query == "cjokes":
            context['posts'] = MyPost.objects.filter(category__icontains="jokes").order_by("-id")
        elif query == "cother":
            context['posts'] = MyPost.objects.filter(category__icontains="other").order_by("-id")                                                            
        else:    
            context['posts'] = MyPost.objects.filter(Q(title__icontains = query) | Q(content__icontains = query) | Q(category__icontains = query) | Q(author__username__icontains = query)).order_by("-id")
        context['comments'] = PostComment.objects.all()
        replies= PostComment.objects.all().exclude(parent=None)
        replyDict = {}
        for reply in replies:
            if reply.parent.id not in replyDict.keys():
                replyDict[reply.parent.id] = [reply]
            else:
                replyDict[reply.parent.id].append(reply)  
        context['replyDict'] =replyDict     
        return context




@method_decorator(login_required, name = "dispatch")
class MyPostsListView(ListView):
    model =MyPost
    ordering = ['-cr_date']
    paginate_by=10
    def get_queryset(self) :
        return MyPost.objects.filter(Q(author = self.request.user)).order_by("-id")



@method_decorator(login_required, name = "dispatch")
class UserMyPostListView(ListView):
    model =MyPost
    template_name = 'articles/user_posts.html'
    context_object_name = 'posts'
    paginate_by=10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return MyPost.objects.filter(author=user).order_by('-cr_date')
        
@method_decorator(login_required, name = "dispatch")
class MyPostDetailView(DetailView):
    model =MyPost


@method_decorator(login_required, name = "dispatch")
class MyProfileDetailView(DetailView):
    model =MyProfile
    def get_queryset(self):
        profList = MyProfile.objects.all()
        for p1 in profList:
            p1.followed = False
            ob = FollowUser.objects.filter(profile = p1, followed_by = self.request.user.myprofile)
            if ob:
                p1.followed = True
        return profList        


    

@method_decorator(login_required, name = "dispatch")
class MyPostUpdateView(UpdateView):
    model =MyPost
    fields = ['title', 'content','images']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        Mypost = self.get_object()
        if self.request.user == Mypost.author:
            return True
        return False


@method_decorator(login_required, name = "dispatch")
class MyPostDeleteView(DeleteView):
    model = MyPost   
@method_decorator(login_required, name = "dispatch")
class PostCommentDeleteView(DeleteView):
    model = PostComment   



class AboutView(TemplateView):
    template_name= "articles/About.html"

class DisclaimerView(TemplateView):
    template_name= "articles/Disclaimer.html"

class PrivacyPolicyView(TemplateView):
    template_name= "articles/PrivacyPolicy.html"
      
class TermsAndConditionsView(TemplateView):
    template_name= "articles/TermsAndConditions.html"
   
class CustomerSupportView(TemplateView):
    template_name= "articles/CustomerSupport.html"
      
def faq(request):
    context = {
        'contacts': Contact.objects.all(),     
    } 
    
    return render(request,'articles/faq.html',context)

           
@method_decorator(login_required, name="dispatch")
class MyProfileUpdateView(UpdateView):
    model = MyProfile
    fields =["name","age","address","status","gender","phone_no","description","profilepic"]

@method_decorator(login_required, name="dispatch")
class MyPostCreate(CreateView)    :
    model =MyPost
    fields = ["title","content","category","images"]
    def form_valid(self, form):
        self.object = form.save()
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

def follow(req, pk):
    user = MyProfile.objects.get(pk=pk)
    FollowUser.objects.create(profile=user, followed_by = req.user.myprofile)
    return HttpResponseRedirect(redirect_to="/articles/home/")

def like_post(request):
    user =  request.user
    if request.method=='POST':
        post_id = request.POST.get('post_id')
        post_obj = MyPost.objects.get(id=post_id)

        if user in post_obj.likes.all():
            post_obj.likes.remove(user)
        else:
            post_obj.likes.add(user)  

        like, created = PostLike.objects.get_or_create(user=user,post_id=post_id)   
        if not created:
            if like.value =="Like":
                like.value ="UnLike"
            else:
                like.value ="Like"  
        like.save()          

    return redirect('/')

def SendComment(request)  :
    if request.method =="POST":
        comment=request.POST.get("msg")
        user = request.user
        post_id = request.POST.get('post_id')
        try:
            post_obj = MyPost.objects.get(pk=post_id)
        except MyPost.DoesNotExist:
            post_obj=None
        commentid = request.POST.get("commentid")
        if commentid == "":
            comment=PostComment(msg=comment, user=user,post=post_obj)
            comment.save()
            messages.success(request, "Your comment is posted succcessfully")
        else:
            parent = PostComment.objects.get(pk= commentid)
            comment=PostComment(msg=comment, user=user,post=post_obj,parent=parent)
        comment.save()
        messages.success(request, "Your Reply is posted succcessfully")
    
    return redirect('/')


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        msg = request.POST['msg']
        contact =Contact(name=name,email=email,msg=msg )
        contact.save()
        messages.success(request, "Your message is recieved")
        
    return redirect('/')    

def postreport(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = MyPost.objects.get(id=post_id)
        postreport = request.POST['postreport']
        post_obj.flag = postreport
        post_obj.save()
        messages.success(request, "Report is recieved")
    return redirect('/')
