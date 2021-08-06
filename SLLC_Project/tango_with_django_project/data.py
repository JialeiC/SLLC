import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Question, UserProfile
from django.contrib.auth.models import User

def populate():
    python_question=[
        {'title':'What are Literals in Python and explain about different Literals?',
        'content':'Literals in Python refer to the data that is given in a variable or constant. ',
        'likes':19,
        'views':37},
        {'title':'How to Install Python?',
        'content':'To Install Python, first go to Anaconda.org and click on “Download Anaconda”. Here, you can download the latest version of Python.',
        'likes':124,
        'views':477},
        {'title':'What are comments and how can you add comments in Python?',
        'content':'Comments in Python refer to a piece of text intended for information. It is especially relevant when more than one person works on a set of codes. '
                  'It can be used to analyse code, leave feedback, and debug it. ',
        'likes':89,
        'views':987},
        {'title': 'How long can an identifier be in Python?',
         'content': 'According to the official Python documentation, an identifier can be of any length.',
         'likes': 24,
         'views': 87},
        {'title': 'What is the pass statement in Python?',
         'content': 'There may be times in our code when we haven’t decided what to do yet, '
                    'but we must type something for it to be syntactically correct.',
         'likes': 65,
         'views': 764}
    ]

    java_question=[
        {'title':'What are constructors in Java?',
        'content':'In Java, constructor refers to a block of code which is used to initialize an object.',
        'likes':73,
        'views':743},
        {'title':'Why Java is platform independent?',
        'content':'Java is called platform independent because of its byte codes which can run on any system irrespective of its underlying operating system.',
        'likes':9,
        'views':32},
        {'title':'Why pointers are not used in Java?',
        'content':'Java doesn’t use pointers because they are unsafe and increases the complexity of the program.',
        'likes':23,
        'views':455},
        {'title': 'What is JIT compiler in Java?',
         'content': 'JIT stands for Just-In-Time compiler in Java.',
         'likes': 4,
         'views': 10},
        {'title': 'What are the main concepts of OOPs in Java?',
         'content': 'Object-Oriented Programming or OOPs is a programming style.',
         'likes': 34,
         'views': 325}
    ]

    cpp_question=[
        {'title':'What are the different data types present in C++?',
        'content':'The 4 data types in C++ are given below:',
        'likes':23,
        'views':856},
        {'title':'What are class and object in C++?',
        'content':'A class is a user-defined data type that has data members and member functions.',
        'likes':43,
        'views':677},
        {'title':'What is polymorphism in C++?',
        'content':'Polymorphism in simple means having many forms.',
        'likes':13,
        'views':78},
        {'title': 'What are the C++ access specifiers?',
         'content': 'In C++ there are the following access specifiers:',
         'likes': 15,
         'views': 98},
        {'title': 'What do you mean by abstraction in C++?',
         'content': 'Abstraction is the process of showing the essential details to the user and hiding the details '
                    'which we don’t want to show to the user or hiding the details which are irrelevant to a particular user.',
         'likes': 234,
         'views': 756}
    ]

    web_question=[
        {'title':'What is a pseudo-class?',
        'content':'It is a CSS technique that sets the style when an element changes its state. ',
        'likes':456,
        'views':1034},
        {'title':'What is CORS? Why is it important?',
        'content':'This is an important web developer interview question. ',
        'likes':13,
        'views':65},
        {'title':'What are the advantages of HTTP 2.0 over HTTP 1.1?',
        'content':'The major advantages of HTTP 2.0 over HTTP 1.1 include',
        'likes':2,
        'views':45},
        {'title': 'What are the new form elements introduced in HTML5?',
         'content': 'The new form elements introduced in HTML5',
         'likes': 34,
         'views': 457},
        {'title': 'What is the difference between null value and undefined value?',
         'content': 'Undefined means a variable has been declared '
                    'but has not yet been assigned a value. On the other hand, null is an assignment value.',
         'likes': 15,
         'views': 77}
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