from django.urls import path

from test_generator.views import TestGeneratorView

urlpatterns = [
    path('', TestGeneratorView.as_view(), name='generate-test'),
]
