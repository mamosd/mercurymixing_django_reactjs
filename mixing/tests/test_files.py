from __future__ import unicode_literals, absolute_import

from django.contrib.auth import get_user_model
from django.test import TestCase

from utils import status, create_temp_file, get_uid

from mixing.models import Project, Song, Group, Track, Comment, FinalFile

User = get_user_model()


def create_private_files(owner):
    project = Project.objects.create(title="Project", owner=owner)
    song = Song.objects.create(project=project, title="Song")
    group = Group.objects.create(song=song, title="Group")

    f = create_temp_file("temp-track.wav", "audio/x-wav")
    track = Track.objects.create(group=group, file=f)

    f = create_temp_file("attachment.txt", "text/plain")
    comment = Comment.objects.create(
        project=project, attachment=f, author=owner, content="Comment")

    f = create_temp_file("final.wav", "audio/x-wav")
    final = FinalFile.objects.create(project=project, attachment=f)

    return track, comment, final


class PrivateFieldTests(TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Runs once per class, not once per test method.
        Make sure all objects defined here are NOT modified in test methods.
        Django provides it's own setUpTestData, but it appears to be buggy
        when used with Postgres, raising InterfaceError: Connection already closed.
        https://groups.google.com/d/msg/django-users/MDRcg4Fur98/cGYs8cmQLAAJ
        """
        cls.staff_data = {"username": get_uid(30), "password": "staff"}
        cls.staff = User.objects.create_user(**cls.staff_data)
        cls.staff.is_staff = True
        cls.staff.save()

        cls.non_owner_data = {"username": get_uid(30), "password": "other"}
        cls.non_owner = User.objects.create_user(**cls.non_owner_data)

        cls.owner_data = {"username": get_uid(30), "password": "owner"}
        cls.owner = User.objects.create_user(**cls.owner_data)
        cls.owner.profile.track_credit = 1
        cls.owner.profile.save()

        cls.track, cls.comment, cls.final = create_private_files(owner=cls.owner)

    @classmethod
    def tearDownClass(cls):
        """
        Manually remove all models that create files, which will cause the
        files on disk to be removed by django-cleanup.
        This way running tests won't leave left-over files.
        """
        Track.objects.all().delete()
        Comment.objects.all().delete()
        FinalFile.objects.all().delete()

    def test_track_access(self):
        """
        On Track objects only staff users should be able to access the file.
        Yes, even the owner of the file can't download it because they don't need to.
        """
        # Anon user should be forbidden
        response = self.client.get(self.track.file.url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

        # Non owner should be forbidden
        self.client.login(**self.non_owner_data)
        response = self.client.get(self.track.file.url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

        # Owner should be forbidden
        self.client.login(**self.owner_data)
        response = self.client.get(self.track.file.url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

        # Staff should be allowed
        self.client.login(**self.staff_data)
        response = self.client.get(self.track.file.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_comment_access(self):
        """
        Since both staff members and the owner may create comments with attachments,
        both should have access to the files on Comments.
        """
        # Anon user should be forbidden
        response = self.client.get(self.comment.attachment.url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

        # Non owner should be forbidden
        self.client.login(**self.non_owner_data)
        response = self.client.get(self.comment.attachment.url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

        # Owner should be allowed
        self.client.login(**self.owner_data)
        response = self.client.get(self.comment.attachment.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        # Staff should be allowed
        self.client.login(**self.staff_data)
        response = self.client.get(self.comment.attachment.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_final_file_access(self):
        """
        FinalFiles should be available to the owner and staff members.
        """
        # Anon user should be forbidden
        response = self.client.get(self.final.attachment.url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

        # Non owner should be forbidden
        self.client.login(**self.non_owner_data)
        response = self.client.get(self.final.attachment.url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

        # Owner should be allowed
        self.client.login(**self.owner_data)
        response = self.client.get(self.final.attachment.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        # Staff should be allowed
        self.client.login(**self.staff_data)
        response = self.client.get(self.final.attachment.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
