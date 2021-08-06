from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.defaultfilters import date
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rango.models import Category, Page, Question, Comment
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm, QuestionForm
from datetime import datetime
from django.core.paginator import Paginator

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    latest_question_list = Question.objects.order_by('-date')[:5]
    most_view=Question.objects.order_by('-views')[:5]
    most_liked=Question.objects.order_by('-likes')[:5]
    
    context_dict = {}
    context_dict['most_view'] = most_view
    context_dict['most_liked'] = most_liked
    context_dict['categories'] = category_list
    context_dict['latest_question_list'] = latest_question_list
    visitor_cookie_handler(request)

    return render(request, 'rango/index.html', context=context_dict)

@login_required
def questions(request):
    category_list = Category.objects.order_by('-likes')[:5]
    question_list = Question.objects.order_by('-views')[:]

    context_dict = {}
    context_dict['categories'] = category_list
    context_dict['questions'] = question_list

    visitor_cookie_handler(request)

    return render(request, 'rango/questions.html', context=context_dict)

def about(request):
    context_dict = {}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    return render(request, 'rango/about.html', context=context_dict)

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        questions = Question.objects.filter(category=category)
        most_view = Question.objects.order_by('-views')[:5]
        most_liked = Question.objects.order_by('-likes')[:5]

        context_dict['category'] = category
        context_dict['questions'] = questions
        context_dict['most_view'] = most_view
        context_dict['most_liked'] = most_liked
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['questions'] = None
        context_dict['most_view'] = None
        context_dict['most_liked'] = None
    
    return render(request, 'rango/category.html', context=context_dict)


@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('rango:index'))
        else:
            print(form.errors)
    
    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except:
        category = None


    if category is None:
        return redirect(reverse('rango:index'))

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)  # This could be better done; for the purposes of TwD, this is fine. DM.
    
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request, 'rango/register.html', context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html')

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    
    request.session['visits'] = visits

@login_required
def homepage(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:]

    context_dict = {}
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

    visitor_cookie_handler(request)
    return render(request, 'rango/homepage.html', context=context_dict)

def add_question(request):
    form = QuestionForm()

    if request.method == 'POST':
        form = QuestionForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('rango:index'))
        else:
            print(form.errors)
    return render(request, 'rango/add_question.html', {'form': form})

'''new Question page'''
# def showComment(request,p,question):
#     CommonList= Paginator(Comment.objects.filter(question=question),per_page=5)
#     questions = QuestionList.page(p)

#     return render(request, 'rango/index.html', locals())
