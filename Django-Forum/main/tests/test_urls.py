from django.test import SimpleTestCase
from django.urls import reverse, resolve
from main.views import ForumList, ThreadList, PostList
from main import views

class TestUrls(SimpleTestCase):
    
    def test_homepage(self):
        url = reverse('homepage')
        self.assertEqual(resolve(url).func, views.homepage)
        
    def test_forum_list(self):
        url = reverse('forum_list')
        self.assertEqual(resolve(url).func.view_class, ForumList)
        
    def test_thread_list(self):
        url = reverse('thread_list')
        self.assertEqual(resolve(url).func.view_class, ThreadList)
        
    def test_post_list(self):
        url = reverse('post_list')
        self.assertEqual(resolve(url).func.view_class, PostList)
        
    def test_create_forum(self):
        url = reverse('create_forum')
        self.assertEqual(resolve(url).func, views.create_forum)
        
    def test_create_thread(self):
        url = reverse('create_thread', args=[1])
        self.assertEqual(resolve(url).func, views.create_thread)
        
    def test_create_post(self):
        url = reverse('create_post', args=[1])
        self.assertEqual(resolve(url).func, views.create_post)
        
    def test_edit_post(self):
        url = reverse('edit_post', args=[1, 1])
        self.assertEqual(resolve(url).func, views.edit_post)
        
    def test_delete_post(self):
        url = reverse('delete_post', args=[1, 1])
        self.assertEqual(resolve(url).func, views.delete_post)
        
    def test_filtered_thread_list(self):
        url = reverse('filtered_thread_list', args=[1])
        self.assertEqual(resolve(url).func, views.filtered_thread_list)
        
    def test_filtered_post_list(self):
        url = reverse('filtered_post_list', args=[1])
        self.assertEqual(resolve(url).func, views.filtered_post_list)
        
    def test_delete_forum(self):
        url = reverse('delete_forum', args=[1])
        self.assertEqual(resolve(url).func, views.delete_forum)
        
    def test_delete_thread(self):
        url = reverse('delete_thread', args=[1])
        self.assertEqual(resolve(url).func, views.delete_thread)
        