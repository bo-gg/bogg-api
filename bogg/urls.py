from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from track import views
from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'boggers', views.BoggerViewSet)
router.register(r'entries', views.CalorieEntryViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/entries/$', views.CalorieEntryList.as_view()),
    url(r'^api/entries/(?P<pk>[0-9]+)/$', views.CalorieEntryDetail.as_view()),
    url(r'^api/daily/$', views.DailyEntryList.as_view()),
    url(r'^api/daily/(?P<pk>[0-9]+)/$', views.DailyEntryDetail.as_view()),
    url(r'^api/goals/$', views.CalorieEntryList.as_view()),
    url(r'^api/goals/(?P<pk>[0-9]+)/$', views.CalorieEntryDetail.as_view()),
]
#urlpatterns = format_suffix_patterns(urlpatterns)

