from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.db.models import Q
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def signup(request):
    if request.method == "POST":
        form = UserForm(data=request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']
            display_name = form.cleaned_data['display_name']
            authenticate(email=email, password=password)
            friend = User.objects.get(display_name=display_name)
            friend.friends.add(friend)
            subject = 'THANK YOU FOR SIGNING UP'
            message = f'''
            Dear {display_name},
            Thank you for registering with Social App, Now you can enjoy the benefits of the app,
            You can send and accept friend request
            '''
            sender = settings.EMAIL_HOST_USER
            recipient = [email]
            send_mail(subject=subject, message=message, from_email=sender, recipient_list=recipient, fail_silently=False)
            return redirect('thank_you')
    else:
        form = UserForm()
    context = {'form': form}
    return render(request, 'media_app/signup.html', context)


@login_required(login_url='login')
def index(request):
    posts = Post.objects.filter(author__friends=request.user).all().order_by('-created_at')
    comments = Comment.objects.all()
    groups = Group.objects.filter(user=request.user)
    grouping = Group.objects.all()
    context = {'posts': posts, 'comments': comments, 'groups': groups, 'grouping': grouping}
    if request.is_ajax():
        print('AJAX')
    return render(request, 'media_app/home.html', context)


@login_required(login_url='login')
def create_post(request):
    if request.method == "POST":
        form = PostForm(data=request.POST or None, files=request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            response = {'message': 'Your post has been posted'}
            return JsonResponse(response)
        else:
            response = JsonResponse({'error': form.errors.as_json()})
            response.status_code = 403
            return response

    else:
        form = PostForm()
    return render(request, 'media_app/create_post.html', {'form': form})


@login_required
def delete_post(request, pk):
    post = Post.objects.get(pk=pk)
    if post.author == request.user:
        post.delete()
        messages.success(request, 'Your post has been deleted')
        return redirect('home')
    else:
        messages.error(request, 'You are not authorize to delete this post')
        return redirect('home')


@login_required
def edit_post(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        form = EditPostForm(request.POST or None, instance=post)
        if form.is_valid():
            form.save()
            response = {'message': 'Your post has been edited'}
            return JsonResponse(response)
        else:
            response = JsonResponse({'error': form.errors.as_json()})
            response.status_code = 403
            return response
    else:
        form = EditPostForm(instance=post)
        return render(request, 'media_app/edit_post.html', {'form': form})


@login_required
def create_comment(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST or None)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            response = {'message': 'You have a comment here'}
            return JsonResponse(response)
        else:
            response = JsonResponse({'error': form.errors.as_json()})
            response.status_code = 403
            return response
    else:
        form = CommentForm()
    return render(request, 'media_app/comment.html', {'form': form})


@login_required
def like_post(request, pk):
    user = request.user
    post = get_object_or_404(Post, pk=pk)
    if user in post.likes.all():
        post.likes.remove(user)

    else:
        post.likes.add(user)
        sender = user.display_name
        user = user
        if sender == user:
            noti = Notification.objects.create(
                sender=sender, type='POST LIKE', text=f'You liked your post',
                user=user
            )
            post.author.notification_set.add(noti)
        else:
            noti = Notification.objects.create(
                sender=sender, type='POST LIKE', text=f'{request.user} liked your post',
                user=user
            )
            post.author.notification_set.add(noti)
    sender = settings.EMAIL_HOST_USER
    subject = 'POST LIKES'
    message = f'{request.user} liked your post'
    recipient = [post.author.email]
    send_mail(subject=subject, message=message, recipient_list=recipient, from_email=sender, fail_silently=False)
    count = Notification.objects.filter(user=user).count()
    if request.is_ajax():
        print('AJAX')
        response = {'post': post, 'total_likes': post.likes.count, 'count': count}
        html = render_to_string('media_app/like_section.html', context=response, request=request)
        return JsonResponse({'form': html})


@login_required
def search_friends(request):
    query = request.GET.get('q')
    friends = User.objects.filter(
        Q(display_name__icontains=query) | Q(email__icontains=query) | Q(location__icontains=query))
    paginator = Paginator(friends, 4)
    page = request.GET.get('page')
    try:
        results = paginator.get_page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)
    return render(request, 'media_app/search_result.html', {'results': results, 'query': query})


@login_required
def add_friend_request(request, user_profile):
    requester = User.objects.get(display_name=request.user)
    target = User.objects.get(id=user_profile)
    requester.friend_requests.add(target)
    noti = Notification.objects.create(sender=requester.display_name,
                                       text=f'{requester.display_name} sent you a friend request',
                                       type='Friend request', user=request.user)
    target.notification_set.add(noti)
    sender = settings.EMAIL_HOST_USER
    subject = 'FRIEND REQUEST'
    message = f'{requester.display_name} sent you a friend request. Log in to your account to act on it'
    recipient = [target.email]
    send_mail(subject=subject, message=message, recipient_list=recipient, from_email=sender, fail_silently=False)
    messages.success(request, f'You have sent a friend request to {target.display_name}')
    return redirect('home')


def notification(request):
    notifications = Notification.objects.filter(user=request.user)
    context = {'notifications': notifications}
    return render(request, 'media_app/notification.html', context)


def notification_detail(request, pk):
    noti = get_object_or_404(Notification, pk=pk)
    return render(request, 'media_app/detail.html', {'noti': noti})


def delete_notification(request, pk):
    noti = get_object_or_404(Notification, pk=pk)
    noti.delete()
    return redirect('home')


def accept_friend(request, user_profile, pk):
    requester = User.objects.get(display_name=request.user)
    target = User.objects.get(display_name__icontains=user_profile)
    note = get_object_or_404(Notification, pk=pk)
    requester.friends.add(target)
    requester.friends.add(requester)
    noti = Notification.objects.create(sender=requester.display_name,
                                       text=f'{requester.display_name}  accepted friend request',
                                       type='Friend Request Accepted', user=request.user)
    target.notification_set.add(noti)
    requester.friend_requests.remove(target)
    note.delete()
    sender = settings.EMAIL_HOST_USER
    subject = 'FRIEND REQUEST'
    message = f'{requester.display_name} accepted friend request. Log in to your account to see his/her profile'
    recipient = [target.email]
    send_mail(subject=subject, message=message, recipient_list=recipient, from_email=sender, fail_silently=False)
    messages.success(request, f'You accepted {target.display_name} friend request')
    return redirect('home')


@login_required
def cancel_friend_request(request, user_profile, pk):
    requester = User.objects.get(display_name=request.user)
    note = get_object_or_404(Notification, pk=pk)
    target = User.objects.get(display_name=user_profile)
    requester.friend_requests.remove(target)
    note.delete()
    messages.success(request, f'You declined {target.display_name} friend request')
    return redirect('home')


@csrf_exempt
def edit_profile(request):
    if request.method == "POST":
        form = EditUserForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            response = {'message': 'Your profile has been edited'}
            return JsonResponse(response)
        else:
            response = JsonResponse({'error': form.errors.as_json()})
            response.status_code = 403
            return response
    else:
        form = EditUserForm(instance=request.user)
    context = {'form': form}
    return render(request, 'media_app/user_edit.html', context)


def profile_details(request, user_profile):
    profile = get_object_or_404(User, display_name=user_profile)
    context = {'profile': profile}
    return render(request, 'media_app/profile_detail.html', context)


def cancel_friend_sent(request, user_profile):
    requester = User.objects.get(display_name=request.user)
    target = User.objects.get(id=user_profile)
    requester.friend_requests.remove(target)
    noti = Notification.objects.get(user=target)
    noti.delete()
    messages.success(request, f'You have cancelled the friend request to {target.display_name}')
    return redirect('home')


def create_group(request):
    if request.method == "POST":
        form = GroupForm(request.POST or None)
        if form.is_valid():
            group = form.save(commit=False)
            group.user = request.user
            group.save()
            response = {'message': 'group created'}
            group.members.add(request.user)
            sender = settings.EMAIL_HOST_USER
            subject = 'Group Created'
            message = f'This is to notify you that a group was created on your account'
            recipient = [request.user.email]
            send_mail(subject=subject, message=message, recipient_list=recipient, from_email=sender,
                      fail_silently=False)
            return JsonResponse(response)
        else:
            response = JsonResponse({'error': form.errors.as_json()})
            response.status_code = 403
            return response
    form = GroupForm()
    return render(request, 'media_app/create_group.html', {'form': form})


def group_details(request, pk):
    group = get_object_or_404(Group, pk=pk)
    posts = GroupPost.objects.filter(member=group).all()
    context = {'group': group, 'posts': posts}
    if request.is_ajax():
        pass
    # html = render_to_string('media_app/group_details.html', context=context, request=request)
    return render(request, 'media_app/group_details.html', context)


def group_form(request, pk):
    member = get_object_or_404(Group, pk=pk)
    if request.method == "POST":
        form = GroupPostForm(request.POST or None)
        if form.is_valid():
            post_form = form.save(commit=False)
            post_form.author = request.user
            post_form.member = member
            post_form.save()
            response = {'message': 'post created'}
            return JsonResponse(response)
        else:
            response = JsonResponse({'error': form.errors.as_json()})
            response.status_code = 403
            return response
    else:
        form = GroupPostForm()
    return render(request, 'media_app/group_post.html', {'form': form})


@login_required
def join_group(request, pk):
    group = get_object_or_404(Group, pk=pk)
    group.members.add(request.user)
    noti = Notification.objects.create(
        sender=request.user, type='JOINED GROUP', text=f'{request.user} joined your {group.name} group',
        user=request.user
    )
    group.user.notification_set.add(noti)
    response = {'message': 'you joined this group'}
    return JsonResponse(response)


def leave_group(request, pk):
    group = get_object_or_404(Group, pk=pk)
    group.members.remove(request.user)
    post = group.grouppost_set.filter(author=request.user)
    post.delete()
    response = {'message': 'you left the group'}
    return JsonResponse(response)


def delete_group(request, pk):
    group = get_object_or_404(Group, pk=pk)
    group.delete()
    messages.success(request, f'You deleted your {group.name}')
    return redirect('home')


def show_comments(request, pk):
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=post)
    return render(request, 'media_app/comment_post.html', {'comments': comments})
