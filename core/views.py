from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Profile,Post,LikePost
from django.contrib.auth.decorators import login_required

# Create your views here.

# @login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user = user_object)
    image = user_profile.profileimg
    posts = Post.objects.all()
    return render(request,'index.html',{'image':image,'posts':posts})


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'User email already exists')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username already exists')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()
                
                #Log user in and redirect to settings page

                #Create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('signup')
        else:
            messages.info(request,'Password not matching')
            return redirect('signup')
        
    else:
        return render(request,'signup.html')
    

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request, 'Credential Invalid')
            return redirect('signin')

        
        
    else:
        return render(request,'signin.html')
    
@login_required(login_url='signin')
def Logout(request):

    auth.logout(request)
    return redirect('signin')


@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user = request.user)
    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
        else:
            image = request.FILES.get('image')
        
        bio = request.POST['bio']
        location = request.POST['location']

        user_profile.profileimg = image
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()
        return redirect('settings')

    return render(request,'setting.html',{'user_profile':user_profile})

# @login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        img = request.FILES.get('uploaded_img')
        caption = request.POST['caption']
        new_post = Post.objects.create(user = user,image = img,caption = caption)
        # poster_image = new_post.img()
        # poster_obj = Profile.objects.get(user = user)
        # poster_profile = poster_obj.profileimg
        new_post.save()
    
    # return render(request,'/',{'poster_img':poster_image})
        return redirect('/')

def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(postId = post_id)
    like_filer = LikePost.objects.filter(post_id = post_id,username = username).first()

    if like_filer == None:
        new_like = LikePost.objects.create(post_id=post_id, username = username)
        new_like.save()
        post.no_of_likes += 1
        post.save()
        return redirect('/')
    else:
        like_filer.delete()
        post.no_of_likes -= 1
        post.save()
        return redirect('/')

def profile(request,pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_posts_len = len(user_posts)

    context = {
        'user_profile': user_profile,
        'user_post': user_posts,
        'user_post_len': user_posts_len
    }
    return render(request, 'profile.html', context)