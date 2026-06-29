from django.urls import path, include

urlpatterns = [
    path('accounts/', include('apps.shared.accounts.urls')),
    path('', include('apps.shared.core.urls')),
    path('suggestions/', include('apps.shared.suggestions.urls')),
]
