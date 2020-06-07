from django.test import TestCase
from django.urls import reverse, resolve

from dashboard.views import HomeView, TopicsDashboardView
from dashboard.models import Dashboard


# Create your tests here.
class HomeTests(TestCase):
    def setUp(self):
        self.dashboard = Dashboard.objects.create(name='Django', description='Django is the best')
        url = reverse('dashboard:home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, HomeView)

    def test_home_view_contains_link_to_topics_page(self):
        dashboard_topics_url = reverse('dashboard:topics_dashboard', kwargs={'pk': self.dashboard.pk})
        self.assertContains(self.response, 'href="{0}"'.format(dashboard_topics_url))


class TopicsDashboardTests(TestCase):
    def setUp(self):
        Dashboard.objects.create(name='Django', description='Django is the best')

    def test_dashboard_topics_views_success_status_code(self):
        url = reverse('dashboard:topics_dashboard', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_dashboard_topics_views_not_found_status_code(self):
        url = reverse('dashboard:topics_dashboard', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_dashboard_topics_url_resolves_topics_dashboard_view(self):
        view = reverse('topics/1/')
        self.assertEquals(view.func, TopicsDashboardView)
