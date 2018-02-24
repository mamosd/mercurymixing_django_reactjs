from __future__ import unicode_literals, absolute_import

from collections import Counter
from StringIO import StringIO
from zipfile import ZipFile

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase

from utils import status, get_uid, create_temp_file, add_site_permission

from mixing.models import Project, Track

User = get_user_model()
admin_login_url = reverse("admin:login")

expected_zip_structure = [
    "Song 1/Group 1/track1.wav",
    "Song 1/Group 1/track2.wav",
    "Song 1/Group 2/track3.wav",
    "Song 1/Group 2/track4.wav",
    "Song 2/Group 3/track5.aif",
    "Song 2/Group 3/track6.aif",
    "Song 2/Group 4/track7.aif",
    "Song 2/Group 4/track8.aif",
]


class AdminTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.staff_data = {"username": get_uid(30), "password": "staff"}
        cls.staff = User.objects.create_user(**cls.staff_data)
        cls.staff.is_staff = True
        cls.staff.save()
        add_site_permission(cls.staff)

        cls.owner_data = {"username": get_uid(30), "password": "owner"}
        cls.owner = User.objects.create_user(**cls.owner_data)

        # Must match with the number of tracks below
        cls.owner.profile.track_credit = 8
        cls.owner.profile.save()

        cls.project = Project.objects.create(
            title="Test project",
            owner=cls.owner,
            status=Project.STATUS_IN_PROGRESS
        )

        cls.download_url = reverse(
            "admin:mixing_project_download", args=[cls.project.pk])

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # Create the Songs, Groups, and Tracks that match expected_zip_structure
        song1 = self.project.songs.create(title="Song 1")
        group1 = song1.groups.create(title="Group 1")
        group1.tracks.create(file=create_temp_file("track1.wav", "audio/x-wav"))
        group1.tracks.create(file=create_temp_file("track2.wav", "audio/x-wav"))
        group2 = song1.groups.create(title="Group 2")
        group2.tracks.create(file=create_temp_file("track3.wav", "audio/x-wav"))
        group2.tracks.create(file=create_temp_file("track4.wav", "audio/x-wav"))

        song2 = self.project.songs.create(title="Song 2")
        group3 = song2.groups.create(title="Group 3")
        group3.tracks.create(file=create_temp_file("track5.aif", "audio/x-aiff"))
        group3.tracks.create(file=create_temp_file("track6.aif", "audio/x-aiff"))
        group4 = song2.groups.create(title="Group 4")
        group4.tracks.create(file=create_temp_file("track7.aif", "audio/x-aiff"))
        group4.tracks.create(file=create_temp_file("track8.aif", "audio/x-aiff"))

    def tearDown(self):
        """
        Manually remove the Tracks, which will cause the files on disk
        to be removed by django-cleanup.
        This way running tests won't leave left-over files.
        """
        Track.objects.all().delete()

    def test_zip_download(self):
        # Anon user should be redirected to login page
        response = self.client.get(self.download_url)
        self.assertRedirects(response, admin_login_url + "?next=" + self.download_url)

        # Same for the owner of the project
        self.client.login(**self.owner_data)
        response = self.client.get(self.download_url)
        self.assertRedirects(response, admin_login_url + "?next=" + self.download_url)

        # Staff users should be allowed
        self.client.login(**self.staff_data)
        response = self.client.get(self.download_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get("Content-Type"), "application/zip")

        # Compare the contents of the resulting zip against expected_zip_structure
        # We use Counter() to compare disregarding order
        # http://stackoverflow.com/a/7829388/1330003
        z = ZipFile(StringIO(response.content), "r")
        self.assertEqual(Counter(expected_zip_structure), Counter(z.namelist()))
