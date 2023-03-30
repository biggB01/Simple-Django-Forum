from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import *
from main.views import *


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.forum = Forum.objects.create(name='Test Forum', description='A test forum')
        self.thread = Thread.objects.create(forum=self.forum, title='Test Thread')
        self.post = Post.objects.create(thread=self.thread, body='Test post body')

    def test_homepage_view(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)

    def test_forum_list_view(self):
        response = self.client.get(reverse('forum_list'))
        self.assertEqual(response.status_code, 200)
        
        self.assertContains(response, self.forum.name)

    def test_thread_list_view(self):
        response = self.client.get(reverse('thread_list'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.thread.title)

    def test_post_list_view(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.body)


class LoginRequestTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.user = User.objects.create_user(
            username='testuser', email='testuser@example.com', password='testpass')
    
    def test_login_request_with_valid_credentials(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, reverse('homepage'))
        
    def test_login_request_with_invalid_credentials(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, 200) 
            


class RegisterViewTestCase(TestCase):    
    def setUp(self):
        self.client = Client()
        self.url = reverse('register')

    def test_register_view_with_valid_data(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 1)

    def test_register_view_with_invalid_data(self):
        data = {
            'username': 'testuser',
            'email': 'invalidemail',
            'password1': 'testpassword123',
            'password2': 'testpassword1234'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)


class LogoutRequestTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('logout')
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
    
    def test_logout_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('homepage'))
        self.assertFalse('_auth_user_id' in self.client.session)


class CreateForumTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.forum_user = ForumUser.objects.create(user=self.user, username='testuser')
        self.client.login(username='testuser', password='testpass')
        self.url = reverse('create_forum')
        self.form_data = {'name': 'Test Forum', 'description': 'This is a test forum'}

    def test_create_forum_view(self):
        response = self.client.post(self.url, self.form_data)
        self.assertEqual(response.status_code, 302)
        forum = Forum.objects.get(name='Test Forum')
        self.assertEqual(forum.description, 'This is a test forum')


class CreateThreadTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.forum = Forum.objects.create(name='Test Forum', description='A forum for testing')
        self.create_thread_url = reverse('create_thread', kwargs={'forum_id': self.forum.id})
        
    def test_create_thread_view_with_valid_data(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.create_thread_url, {'title': 'Test Thread'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Thread.objects.count(), 1)
        thread = Thread.objects.first()
        self.assertEqual(thread.title, 'Test Thread')
        self.assertEqual(thread.forum, self.forum)
        
    def test_create_thread_view_with_invalid_data(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.create_thread_url, {'title': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')
        self.assertEqual(Thread.objects.count(), 0)


class CreatePostViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.forum = Forum.objects.create(name='Test Forum', description='This is a test forum.')
        self.thread = Thread.objects.create(forum=self.forum, title='Test Thread')
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.url = reverse('create_post', kwargs={'thread_id': self.thread.id})

    def test_create_post_view(self):
        response = self.client.post(self.url, {'body': 'This is a test post.'})
        self.assertEqual(response.status_code, 302)  # Redirect after successful post creation
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().body, 'This is a test post.')
        self.assertEqual(Post.objects.first().thread, self.thread)
        self.assertEqual(Post.objects.first().thread.forum, self.forum)


class DeleteForumTestCase(TestCase):
    def setUp(self):
        self.forum = Forum.objects.create(name='Test Forum', description='Test description')

    def test_delete_forum(self):
        response = self.client.post(reverse('delete_forum', args=[self.forum.id]))
        self.assertEqual(response.status_code, 302)



class DeleteThreadTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.forum = Forum.objects.create(name='Test Forum')
        self.thread = Thread.objects.create(forum=self.forum, title='Test Thread')
        self.post = Post.objects.create(thread=self.thread, body='Test Post')

    def test_delete_thread_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.delete(reverse('delete_thread', args=[self.thread.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Thread.objects.filter(id=self.thread.id).exists())


class DeletePostTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.forum = Forum.objects.create(name='Test Forum')
        self.thread = Thread.objects.create(forum=self.forum, title='Test Thread')
        self.post = Post.objects.create(thread=self.thread, body='Test Body')
        self.client.login(username='testuser', password='testpass')
        
    def test_delete_post(self):
        response = self.client.post(reverse('delete_post', args=[self.thread.id, self.post.id]))
        self.assertRedirects(response, reverse('thread_list', args=[self.thread.id]))


class EditPostTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.forum = Forum.objects.create(name='Test Forum', description='A test forum.')
        self.thread = Thread.objects.create(forum=self.forum, title='Test Thread')
        self.post = Post.objects.create(thread=self.thread, body='Test post body.')
        self.url = reverse('edit_post', args=[self.thread.id, self.post.id])

    def test_edit_post(self):
        self.client.login(username='testuser', password='testpass')
        new_body = 'Edited post body.'
        response = self.client.post(self.url, {'body': new_body})
        self.assertEqual(response.status_code, 302)
        edited_post = Post.objects.get(id=self.post.id)
        self.assertEqual(edited_post.body, new_body)

    def test_edit_post_unauthenticated(self):
        new_body = 'Edited post body.'
        response = self.client.post(self.url, {'body': new_body})
        self.assertEqual(response.status_code, 302)
        edited_post = Post.objects.get(id=self.post.id)
        self.assertNotEqual(edited_post.body, new_body)

    def test_edit_post_invalid_form(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')
        edited_post = Post.objects.get(id=self.post.id)
        self.assertNotEqual(edited_post.body, '')


class FilteredThreadListTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.forum = Forum.objects.create(
            name='Test Forum', description='This is a test forum.'
        )
        self.thread1 = Thread.objects.create(
            forum=self.forum, title='Test Thread 1'
        )
        self.thread2 = Thread.objects.create(
            forum=self.forum, title='Test Thread 2'
        )
        self.thread3 = Thread.objects.create(
            forum=self.forum, title='Test Thread 3'
        )

    def test_filtered_thread_list(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('filtered_thread_list', args=[self.forum.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.thread1.title)
        self.assertContains(response, self.thread2.title)
        self.assertContains(response, self.thread3.title)
        self.assertTemplateUsed(response, 'filters/filtered_threads.html')


class FilteredPostListTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.forum = Forum.objects.create(name='Test Forum', description='A test forum')
        self.thread = Thread.objects.create(forum=self.forum, title='Test Thread')
        self.post = Post.objects.create(thread=self.thread, body='Test Post')
        
    def test_filtered_post_list_view(self):
        url = reverse('filtered_post_list', args=[self.forum.id, self.thread.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/filtered_post_list.html')
        self.assertContains(response, self.forum.name)
        self.assertContains(response, self.thread.title)
        self.assertContains(response, self.post.body)