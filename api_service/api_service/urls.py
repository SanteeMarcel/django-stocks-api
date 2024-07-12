# encoding: utf-8

from django.contrib import admin
from django.urls import path

from api import views as api_views
from rest_framework_simplejwt import views as jwt_views

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('stock', api_views.StockView.as_view(), name='stock-view'),
    path('history', api_views.HistoryView.as_view(), name='history-view'),
    path('stats', api_views.StatsView.as_view(), name='stats-view'),
    path('admin', admin.site.urls),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
