from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rango.models import Category, Question, Comment, UserProfile
from django.contrib.auth.models import User

def add_user():
    user = User.objects.get_or_create(username='test',email='test.gmail.com')[0]
    user.set_password('123456')
    user.save()

    profile = UserProfile.objects.get_or_create(user=user)[0]
    profile.save()

def add_category(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = abs(views)
    c.likes = abs(likes)
    c.save()
    return c

def add_question(cat, title, content, likes, views): 
    q = Question.objects.get_or_create(category=cat, title=title, user_id=1)[0]
    q.content=content
    q.likes=abs(likes)
    q.views=abs(views)
    q.save()
    return q

def addComment(question_id,content):
    c = Comment.objects.get_or_create(question_id=question_id,content=content,user_id=1)[0]
    c.save()
    return c

class CategoryMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        """
        Ensures the number of views received for a Category are positive or zero.
        """
        category = add_category('test', views=-1, likes=0)

        self.assertEqual((category.views >=0), True)
    
    def test_slug_line_creation(self):
        """
        Checks to make sure that when a category is created, an appropriate slug is created.
        Example: "Random Category String" should be "random-category-string".
        """
        category = add_category('Random Category String')
        category.save()

        self.assertEqual(category.slug, 'random-category-string')

class IndexViewTests(TestCase):
    def test_index_view_with_no_categories(self):
        """
        If no categories exist, the appropriate message should be displayed.
        """
        response = self.client.get(reverse('rango:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no categories present.')
        self.assertQuerysetEqual(response.context['categories'], [])
    
    def test_index_view_with_categories(self):
        """
        Checks whether categories are displayed correctly when present.
        """
        add_category('Python', 1, 1)
        add_category('C++', 1, 1)
        add_category('Erlang', 1, 1)

        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python')
        self.assertContains(response, 'C++')
        self.assertContains(response, 'Erlang')

        num_categories = len(response.context['categories'])
        self.assertEquals(num_categories, 3)

class QuestionAccessTests(TestCase):
    def test_Question_not_in_future(self):
        category = add_category('Django', 1, 1)
        question=add_question(cat=category, title='test_question', content='question_content', likes=-1, views=-1)
        self.assertTrue(question.date<=timezone.now())
        self.assertTrue(question.likes>=0)
        self.assertTrue(question.views>=0)
        
    
class CommentAccessTests(TestCase):
    def test_Comment_not_in_future(self):
        category = add_category('Django', 1, 1)
        question=add_question(cat=category, title='test_question', content='question_content', likes=-1, views=-1)
        comment=addComment(question_id=question.id,content='test_comment_content')
        print(comment)
        self.assertTrue(question.date<=timezone.now())
        self.assertTrue(comment.likes>=0)
