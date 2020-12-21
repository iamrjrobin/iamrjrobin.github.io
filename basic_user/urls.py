from django.urls import path, include
from .import views 
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authtoken import views as view

schema_view = get_schema_view(
   openapi.Info(
      title="House API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('api/api-token-auth/', view.obtain_auth_token),
    path('', views.display, name='show'),
    path('logs/single_log/<int:employee_id>/',views.single_log, name = 'single_log'),
    path('logs/',views.taking_logs, name = 'logger'),
    path('<int:house_id>/', views.details, name='details'),
    path('api/display/', views.api_display),
    path('api/display/<int:house_id>', views.api_details),
    path('api/display/find/<int:house_id>', views.Emp_list_view.as_view()),
    path('api/logs', views.api_taking_logs),
    path('api/logs/single_logs/<int:employee_id>',views.api_single_log),
    path('api/show_all_emp/',  views.api_all_emp),
    path('api/api_all_emp_update/<int:employee_id>',views.api_all_emp_update),
    path('api/api_points/', views.api_points),
    # url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
    # url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]



