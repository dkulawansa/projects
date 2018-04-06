from __future__ import unicode_literals
from .views import EditDistanceViewSet

from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'editdistance', EditDistanceViewSet, 'editdistance')

urlpatterns = router.urls