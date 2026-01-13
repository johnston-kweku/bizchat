from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.views import PasswordResetView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import UserProfile, Services, Business, Products
from .forms import RegistrationForm, ProfileForm, BusinessForm, ServiceForm, ProductForm


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # 📧 Send welcome email (HTML + text)
            subject = 'Welcome to Biz Chat App 🎉'
            from_email = settings.DEFAULT_FROM_EMAIL
            to = [user.email]

            text_content = f"""
Hi {user.first_name},

Welcome to Biz Chat App!
Your account has been created successfully.

We’re excited to have you 🚀
"""

            html_content = render_to_string(
                'user/emails/welcome.html',
                {'first_name': user.first_name}
            )

            email = EmailMultiAlternatives(
                subject,
                text_content,
                from_email,
                to
            )
            email.attach_alternative(html_content, "text/html")

            try:
                email.send()
            except:
                pass   # never block signup because of email

            login(request, user)
            return redirect('chat:chat-home')

    else:
        form = RegistrationForm()

    return render(request, 'user/sign_up.html', {'form': form})



def login_view(request):
    # Implement login view logic here
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Add authentication logic here

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'user/login.html', {'error': 'Invalid email or password'})
        
        user = authenticate(request, username=user_obj, password=password)


        if user is not None:
            login(request, user)
            return redirect('chat:chat-home')
        else:
            return render(request, 'user/login.html', {'error': 'Invalid email or password'})
        
    return render(request, 'user/login.html')


def logout_view(request):
    logout(request)
    return redirect('user:login')

# View to display all users and briefly demonstrate the use of query sets
def users_view(request):
    # Get all users in database except for the requesting user
    users = User.objects.all().exclude(id=request.user.id)
    # Pass users to the template to be rendered
    context = {
        'users':users
    }
    # Finally render template
    return render(request, 'user/users.html', context)

def get_business(user):
    profile = user.userprofile
    business, _ = Business.objects.get_or_create(user_profile=profile)
    return business


@login_required
def profile_view(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    user_profile = get_object_or_404(UserProfile, user=profile_user)
    
    return render(request, 'user/profile.html', {
        'user_profile': user_profile,
        'user': profile_user,
    })


@login_required
def edit_business(request):
    user_profile = request.user.userprofile
    business,created = Business.objects.get_or_create(user_profile=user_profile)

    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES, instance=business)
        if form.is_valid():
            form.save()
            return redirect('user:profile', user_id=request.user.id)
        
    else:
        form = BusinessForm(instance=business)


    context = {
        'form':form
    }
    return render(request, 'user/edit_business.html', context)

@login_required
def edit_profile(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    user_profile = get_object_or_404(UserProfile, user=profile_user)
    
    if profile_user == request.user:
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES, instance=user_profile)
            if form.is_valid():
                form.save()
                return redirect('user:profile', user_id=request.user.id)
        else:
            form = ProfileForm(instance=user_profile)

    context = {
            'form':form,
            'user_profile':user_profile
        }
    return render(request, 'user/edit_profile.html', context)

@login_required
def add_service(request):
    business = request.user.userprofile.business
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.business = business
            service.save()
            return redirect('user:profile', user_id=request.user.id)
        
    else:
        form = ServiceForm()

    context = {
        'form':form
    }
    return render(request, 'user/add_service.html',  context)

def edit_service(request, service_id):
    service = get_object_or_404(Services, id=service_id)

    if service.business.user_profile.user != request.user:
        return redirect('user:profile', request.user.id)
    
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('user:profile', request.user.id)
    
    else:
        form = ServiceForm(instance=service)

    context = {
        'form':form,
        'title':service.title
    }
    return render(request, 'user/edit_service.html', context)

def delete_service(request, service_id):
    service = get_object_or_404(Services, id=service_id)

    if service.business.user_profile.user == request.user:
        service.delete()

    return redirect('user:profile', request.user.id)

def add_product(request):
    business = get_business(request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.business = business
            product.save()
            return redirect('user:profile', user_id=request.user.id)

    else:
        form = ProductForm(request.FILES)

    context = {
        'form':form
    }
    return render(request, 'user/add_product.html',context)

def edit_product(request, product_id):
    product = get_object_or_404(Products, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('user:profile', request.user.id)
        
    else:
        form = ProductForm(instance=product)
    
    context= {
        'form':form
    }
    return render(request, 'user/edit_product.html', context)

def delete_product(request, product_id):
    product = get_object_or_404(Products, id=product_id)

    if product.business.user_profile.user == request.user:
        product.delete()

    return redirect('user:profile', request.user.id)

# views.py

class CustomPasswordResetView(PasswordResetView):
    template_name = 'user/password_reset.html'
    email_template_name = 'user/emails/password_reset_email.html'  # not used in default for HTML
    subject_template_name = 'user/emails/password_reset_subject.txt'
    success_url = '/user/password-reset/done/'

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Override the default send_mail to send HTML email.
        """
        # Render subject
        subject = render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())  # Remove newlines

        # Render text content
        message = render_to_string(email_template_name, context)

        # Render HTML content
        html_message = render_to_string(html_email_template_name or email_template_name, context)

        # Create email
        email = EmailMultiAlternatives(subject, message, from_email, [to_email])
        email.attach_alternative(html_message, "text/html")
        email.send()

