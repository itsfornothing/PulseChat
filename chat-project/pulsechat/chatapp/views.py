from django.shortcuts import get_object_or_404, redirect, render
from .models import PulseChatUsers, Messages, Chat, Group, GroupMessages
from .form import UserForm, CreateGroupForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_backends
from django.contrib import messages



def user_login(request):
    error_message = ''
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email and password:
            user_instance = User.objects.filter(email=email).first()

            if not user_instance:
                messages.error(request, "User doesn't exist!")
                return redirect('login')

            user = authenticate(request, username=user_instance.username, password=password)

            if user is not None:
                login(request, user)
                return redirect('chat_home')

            else:
                messages.error(request, 'Invalid Credential!')
                return redirect('login')

        else:
            error_message = "Please provide both email and password."

    return render(request, 'login.html', {'error_message': error_message})


def register(request):
    error_message = ''
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            full_name = form.cleaned_data.get('full_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            bio = form.cleaned_data.get('bio')

            if User.objects.filter(username=username).exists():
                message = 'Username is already taken, please choose another one.'
                return render(request, 'register.html', {'form': form, 'message': message})

            if User.objects.filter(email=email).exists():
                error_message = 'You already have an account, please login instead!'
                return render(request, 'register.html', {'form': form, 'error_message': error_message})

            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                newuser = PulseChatUsers(username=username, full_name=full_name, email=email, password=user.password,
                                         bio=bio)
                newuser.save()

                backend = get_backends()[0]
                user.backend = f"{backend.__module__}.{backend.__class__.__name__}"

                login(request, user)
                return redirect('chat_home')
    else:
        form = UserForm()

    return render(request, 'register.html', {'form': form})


def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    

def create_grp_view(request):
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')

            if Group.objects.filter(name=name).exists():
                error_message = 'There is a Group with This Name!'
                return render(request, 'create_group.html', {'form': form, 'error_message': error_message})
            
            newgroup = Group(name=name, description=description, owner=request.user)
            newgroup.save()

            newgroup.members.set([request.user])

            return redirect('chat_home')
        
    else:
        form = CreateGroupForm()

    return render(request, 'create_group.html', {'form': form})


def home_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('login')

    chat_users = PulseChatUsers.objects.all().exclude(email=request.user.email)
    
    return render(request, 'homepage.html', {'users': chat_users})


freind_email = ''
def chat_view(request, user_id, *args, **kwargs):
    freind_email = PulseChatUsers.objects.filter(id=user_id).first().email
    print(freind_email)
    chat_users = PulseChatUsers.objects.all().exclude(email=request.user.email)
    messages = None 

    if request.method == 'POST' and freind_email:
        chat_user1 = get_object_or_404(PulseChatUsers, email=request.user.email)
        chat_user2 = get_object_or_404(PulseChatUsers, email=freind_email)
        chat_names = [f'{chat_user1.username}_{chat_user2.username}', f'{chat_user2.username}_{chat_user1.username}']

        chat = Chat.objects.filter(name__in=chat_names).distinct().first()  
        if chat:
            messages = Messages.objects.filter(chat=chat).order_by('id')
     
        else:
            chat = Chat.objects.create(name=f'{chat_user1.username}_{chat_user2.username}')
            chat.save()

    return render(request, 'chat_messages.html', {'messages': messages, 'users': chat_users, 'freind_email': freind_email})

    

def group_view(request, g_name, *args, **kwargs):
    all_groups = Group.objects.all()
    if request.method == 'POST':
        if g_name != 'g_name':
            selected_grp = Group.objects.filter(name=g_name).first() 

            if request.user in selected_grp.members.all():
                print("user is member!")
                messages = GroupMessages.objects.filter(group=selected_grp)

            else:
                selected_grp.members.set([request.user])
                messages = GroupMessages.objects.filter(group=selected_grp)

            return render(request, 'grp_messages.html', {'messages': messages, 'all_groups': all_groups, 'g_name': g_name})

          
    return render(request, 'groups_view.html', {'all_groups': all_groups})



def profile_page(request):
    you = PulseChatUsers.objects.filter(email=request.user.email).first()

    return render(request, 'profile.html', {'profile_data': you})