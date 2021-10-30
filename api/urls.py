from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

#router = routers.DefaultRouter()
#router.register(r'v1/garage',views.GarageViewSet)

urlpatterns = [
   # path('', include(router.urls)),
   path('v1/garage',views.GarageList.as_view()),
   path('v1/garage/<int:pk>/', views.GarageDetail.as_view()),
]

urlpatterns=format_suffix_patterns(urlpatterns)