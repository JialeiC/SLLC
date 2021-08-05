import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Question, UserProfile
from django.contrib.auth.models import User

def populate():
    python_question=[
        {'title':'python_1',
        'content':'question_content_1',
        'likes':15,
        'views':77},
        {'title':'python_2',
        'content':'question_content_2',
        'likes':15,
        'views':77},
        {'title':'python_3',
        'content':'question_content_3',
        'likes':15,
        'views':77},
    ]

    java_question=[
        {'title':'java_1',
        'content':'question_content_1',
        'likes':15,
        'views':77},
        {'title':'java_2',
        'content':'question_content_2',
        'likes':15,
        'views':77},
        {'title':'java_3',
        'content':'question_content_3',
        'likes':15,
        'views':77},
    ]

    cpp_question=[
        {'title':'c++_1',
        'content':'question_content_1',
        'likes':15,
        'views':77},
        {'title':'c++_2',
        'content':'question_content_2',
        'likes':15,
        'views':77},
        {'title':'c++_3',
        'content':'question_content_3',
        'likes':15,
        'views':77},
    ]

    web_question=[
        {'title':'web_1',
        'content':'question_content_1',
        'likes':15,
        'views':77},
        {'title':'web_2',
        'content':'question_content_2',
        'likes':15,
        'views':77},
        {'title':'web_3',
        'content':'question_content_3',
        'likes':15,
        'views':77}
    ]
    
    cats = {'Python': {'questions':python_question, 'views': 128, 'likes': 64},
            'Java': {'questions':java_question, 'views': 64, 'likes': 32},
            'C++': {'questions':cpp_question, 'views': 32, 'likes': 16},
            'Web': {'questions':web_question, 'views': 16, 'likes': 8}, }

    user = User.objects.get_or_create(username='test',email='test.qq.com')[0]
    user.set_password('123456')
    user.save()

    profile = UserProfile.objects.get_or_create(user=user)[0]
    # profile.user = user
    profile.save()

    for cat, cat_data in cats.items():
        c = add_cat(cat, views=cat_data['views'], likes=cat_data['likes'])
        for q in cat_data['questions']:
            add_question(c, q['title'], q['content'], likes=q['likes'], views=q['views'])
    
    for c in Category.objects.all():
        for q in Question.objects.filter(category=c):
            print(f'- {c}: {q}')
def add_question(cat, title, content, likes, views): 
    q = Question.objects.get_or_create(category=cat, title=title, user_id=1)[0]
    # q.user_id=1
    # q.title=title
    q.content=content
    q.likes=likes
    q.views=views
    # q.date=str(time.time())
    q.save()
    return q

def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()