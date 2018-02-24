from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r"songs", views.SongViewSet)
router.register(r"groups", views.GroupViewSet)
router.register(r"tracks", views.TrackViewSet)
router.register(r"comments", views.CommentViewSet)

urlpatterns = [
    url(
        r"^projects/(?P<pk>[0-9]+)/submit/$", views.ProjectSubmit.as_view(),
        name="project_submit"
    ),
    url(
        r"^projects/(?P<pk>[0-9]+)/$", views.ProjectDetail.as_view(),
        name="project_detail"
    ),
    # Wire up our API using automatic URL routing.
    url(r"^api/", include(router.urls)),
]
