from django.test import SimpleTestCase
from django.urls import reverse, resolve
from basic_user.views import display, details, taking_logs, single_log, api_display,api_details,api_taking_logs, api_single_log

class TestUrls(SimpleTestCase):
    
    def test_show_url_is_resolved(self):
        url = reverse('show')
        print(resolve(url))
        self.assertEquals(resolve(url).func, display)

    def test_details_url_is_resolved(self):
        url =  reverse('details',args=[1])
        print(resolve(url))
        self.assertEquals(resolve(url).func, details)
    
    def test_log_url_is_resolved(self):
        url = reverse('logger')
        print(resolve(url))
        self.assertEquals(resolve(url).func, taking_logs)

    def test_single_log_url_is_resolved(self):
        url = reverse('single_log', args = [1])
        print(resolve(url))
        self.assertEquals(resolve(url).func, single_log)

    def test_api_show_url_is_resolved(self):
        url = reverse('api_show')
        print(resolve(url))
        self.assertEquals(resolve(url).func, api_display)

    def test_api_details_url_is_resolved(self):
        url = reverse('api_details', args = [1])
        print(resolve(url))
        self.assertEquals(resolve(url).func, api_details)

    def test_api_logger_url_is_resolved(self):
        url = reverse('api_logger')
        print(resolve(url))
        self.assertEquals(resolve(url).func, api_taking_logs)
    
    def test_api_single_log_url_is_resolved(self):
        url = reverse('api_single_log', args = [1])
        print(resolve(url))
        self.assertEquals(resolve(url).func, api_single_log)