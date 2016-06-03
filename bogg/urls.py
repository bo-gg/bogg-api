from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from track import views
from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'entries', views.CalorieEntryViewSet)
router.register(r'daily', views.DailyEntryViewSet)
router.register(r'goals', views.GoalViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/me/', views.BoggerView.as_view()),
    url(r'^api/create/', views.CreateBoggerView.as_view()),
]
