from django.test import TestCase
from django.contrib.auth.models import User
from main.models import Forum, Thread, Post, ForumUser, Subscription
from django.utils import timezone


class ForumTestCase(TestCase):
    def setUp(self):
        self.forum = Forum.objects.create(name='Test Forum', description='This is a test forum')
    
    def test_forum_str(self):
        self.assertEqual(str(self.forum), 'Test Forum')

class ThreadTestCase(TestCase):
    def setUp(self):
        self.forum = Forum.objects.create(name='Test Forum', description='This is a test forum')
        self.thread = Thread.objects.create(forum=self.forum, title='Test Thread', created_on=timezone.now())
    
    def test_thread_str(self):
        self.assertEqual(str(self.thread), 'Test Thread')

class PostTestCase(TestCase):
    def setUp(self):
        self.forum = Forum.objects.create(name='Test Forum', description='This is a test forum')
        self.thread = Thread.objects.create(forum=self.forum, title='Test Thread', created_on=timezone.now())
        self.post = Post.objects.create(thread=self.thread, body='This is a test post', created_on=timezone.now())

    def test_post_str(self):
        self.assertEqual(str(self.post), 'This is a test post...')

class ForumUserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.forum_user = ForumUser.objects.create(user=self.user, username='testuser', email='testuser@example.com')

    def test_forum_user_str(self):
        self.assertEqual(str(self.forum_user), 'testuser')

class SubscriptionTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.forum = Forum.objects.create(name='Test Forum', description='This is a test forum')
        self.forum_user = ForumUser.objects.create(user=self.user, username='testuser', email='testuser@example.com')
        self.subscription = Subscription.objects.create(user=self.forum_user, forum=self.forum, subscribed_on=timezone.now())

    def test_subscription_str(self):
        self.assertEqual(str(self.subscription), 'testuser subscribed to Test Forum')