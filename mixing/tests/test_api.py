from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.db import transaction

from rest_framework import status
from rest_framework.test import APITestCase

from utils import create_temp_file, get_uid
from mixing.models import Project, Song, Group, Track, Comment

User = get_user_model()


def create_temp_track():
    return create_temp_file("test-song.wav", "audio/wav")


def create_song_dependencies(instance):
    instance.owner = User.objects.create(username=get_uid(30))
    instance.non_owner = User.objects.create(username=get_uid(30))
    instance.active_project = Project.objects.create(
        title="Active Project",
        owner=instance.owner,
    )
    instance.inactive_project = Project.objects.create(
        title="Inactive Project",
        owner=instance.owner,
        active=False,
        status=Project.STATUS_COMPLETE
    )


def create_group_dependencies(instance):
    create_song_dependencies(instance)
    instance.active_song = instance.active_project.songs.create(
        title="Active song"
    )
    instance.inactive_song = instance.inactive_project.songs.create(
        title="Inactive song"
    )


def create_track_dependencies(instance):
    create_group_dependencies(instance)
    instance.active_group = instance.active_song.groups.create(
        title="Active group"
    )
    instance.inactive_group = instance.inactive_song.groups.create(
        title="Inactive group"
    )


class SongAPITests(APITestCase):
    def setUp(self):
        create_song_dependencies(self)

    def test_create_song_on_active_project(self):
        url = reverse("song-list")
        data = {"title": "Test Song", "project": self.active_project.pk}

        # User is anon
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is not owner
        self.client.force_authenticate(user=self.non_owner)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is owner
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Song.objects.count(), 1)
        self.assertEqual(Song.objects.get().title, "Test Song")

    def test_create_song_on_inactive_project(self):
        url = reverse("song-list")
        data = {"title": "Test Song", "project": self.inactive_project.pk}

        # User is anon
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is not owner
        self.client.force_authenticate(user=self.non_owner)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is owner
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # No songs should have been created
        self.assertEqual(Song.objects.count(), 0)

    def test_get_song_on_active_project(self):
        song = self.active_project.songs.create(title="Existing song")
        url = reverse("song-detail", args=[song.pk])

        # User is anon
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is not owner
        self.client.force_authenticate(user=self.non_owner)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # User is owner
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_song_on_inactive_project(self):
        song = self.inactive_project.songs.create(title="Existing song")
        url = reverse("song-detail", args=[song.pk])

        # User is anon
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is not owner
        self.client.force_authenticate(user=self.non_owner)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # User is owner
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_song_on_active_project(self):
        song = self.active_project.songs.create(title="Existing song")
        url = reverse("song-detail", args=[song.pk])
        data = {"title": "New Title", "project": self.active_project.pk}

        # User is anon
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is not owner
        self.client.force_authenticate(user=self.non_owner)
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # User is owner
        self.client.force_authenticate(user=self.owner)
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Song.objects.count(), 1)
        self.assertEqual(Song.objects.get().title, "New Title")

    def test_update_song_on_inactive_project(self):
        song = self.inactive_project.songs.create(title="Existing song")
        url = reverse("song-detail", args=[song.pk])
        data = {"title": "New Title", "project": self.inactive_project.pk}

        # User is anon
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is not owner
        self.client.force_authenticate(user=self.non_owner)
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # User is owner
        self.client.force_authenticate(user=self.owner)
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Nothing should have changed
        self.assertEqual(Song.objects.count(), 1)
        self.assertEqual(Song.objects.get().title, "Existing song")

    def test_delete_song_on_active_project(self):
        song = self.active_project.songs.create(title="Existing song")
        url = reverse("song-detail", args=[song.pk])

        # User is anon
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is not owner
        self.client.force_authenticate(user=self.non_owner)
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # User is owner
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Song.objects.count(), 0)

    def test_delete_song_on_inactive_project(self):
        song = self.inactive_project.songs.create(title="Existing song")
        url = reverse("song-detail", args=[song.pk])

        # User is anon
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is not owner
        self.client.force_authenticate(user=self.non_owner)
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # User is owner
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Nothing should have changed
        self.assertEqual(Song.objects.count(), 1)
        self.assertEqual(Song.objects.get().title, "Existing song")


class GroupAPITests(APITestCase):
    def setUp(self):
        create_group_dependencies(self)

    def test_create_group_on_active_song(self):
        url = reverse("group-list")
        data = {"title": "Test Group", "song": self.active_song.pk}

        # User is anon
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is not owner
        self.client.force_authenticate(user=self.non_owner)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is owner
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Group.objects.count(), 1)
        self.assertEqual(Group.objects.get().title, "Test Group")

    def test_create_group_on_inactive_song(self):
        url = reverse("group-list")
        data = {"title": "Test Group", "song": self.inactive_song.pk}

        # User is anon
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is not owner
        self.client.force_authenticate(user=self.non_owner)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is owner
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # No groups should have been created
        self.assertEqual(Group.objects.count(), 0)

    def test_get_group_on_active_song(self):
        group = self.active_song.groups.create(title="Existing group")
        url = reverse("group-detail", args=[group.pk])

        # User is anon
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is not owner
        self.client.force_authenticate(user=self.non_owner)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # User is owner
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_group_on_inactive_song(self):
        group = self.inactive_song.groups.create(title="Existing group")
        url = reverse("group-detail", args=[group.pk])

        # User is anon
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is not owner
        self.client.force_authenticate(user=self.non_owner)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # User is owner
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_group_on_active_song(self):
        group = self.active_song.groups.create(title="Existing group")
        url = reverse("group-detail", args=[group.pk])
        data = {"title": "New Title", "song": self.active_song.pk}

        # User is anon
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is not owner
        self.client.force_authenticate(user=self.non_owner)
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # User is owner
        self.client.force_authenticate(user=self.owner)
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Group.objects.count(), 1)
        self.assertEqual(Group.objects.get().title, "New Title")

    def test_update_group_on_inactive_song(self):
        group = self.inactive_song.groups.create(title="Existing group")
        url = reverse("group-detail", args=[group.pk])
        data = {"title": "New Title", "song": self.inactive_song.pk}

        # User is anon
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is not owner
        self.client.force_authenticate(user=self.non_owner)
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # User is owner
        self.client.force_authenticate(user=self.owner)
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Nothing should have changed
        self.assertEqual(Group.objects.count(), 1)
        self.assertEqual(Group.objects.get().title, "Existing group")

    def test_delete_group_on_active_song(self):
        group = self.active_song.groups.create(title="Existing group")
        url = reverse("group-detail", args=[group.pk])

        # User is anon
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is not owner
        self.client.force_authenticate(user=self.non_owner)
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # User is owner
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Group.objects.count(), 0)

    def test_delete_group_on_inactive_song(self):
        group = self.inactive_song.groups.create(title="Existing group")
        url = reverse("group-detail", args=[group.pk])

        # User is anon
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is not owner
        self.client.force_authenticate(user=self.non_owner)
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # User is owner
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Nothing should have changed
        self.assertEqual(Group.objects.count(), 1)
        self.assertEqual(Group.objects.get().title, "Existing group")


class TrackAPITests(APITestCase):
    def setUp(self):
        create_track_dependencies(self)
        self.owner.profile.track_credit = 1
        self.owner.profile.save()
        self.non_owner.profile.track_credit = 1
        self.non_owner.profile.save()

    def tearDown(self):
        """
        Manually remove the Tracks, which will cause the files on disk
        to be removed by django-cleanup.
        This way running tests won't leave left-over files.
        """
        Track.objects.all().delete()

    def test_create_track_on_active_group(self):
        url = reverse("track-list")

        # User is anon
        data = {"file": create_temp_track(), "group": self.active_group.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is not owner and has credit
        self.client.force_authenticate(user=self.non_owner)
        data = {"file": create_temp_track(), "group": self.active_group.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is owner and has enough credit
        self.client.force_authenticate(user=self.owner)
        data = {"file": create_temp_track(), "group": self.active_group.pk}
        with transaction.atomic():
            response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Track.objects.count(), 1)

        # User is owner, but now doesn't have credit
        self.client.force_authenticate(user=self.owner)
        data = {"file": create_temp_track(), "group": self.active_group.pk}
        with transaction.atomic():
            response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Track.objects.count(), 1)

    def test_create_track_on_inactive_group(self):
        url = reverse("track-list")

        # User is anon
        data = {"file": create_temp_track(), "group": self.inactive_group.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is not owner and has credit
        self.non_owner.profile.track_credit = 1
        self.non_owner.profile.save()
        self.client.force_authenticate(user=self.non_owner)
        data = {"file": create_temp_track(), "group": self.inactive_group.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is owner and has credit
        self.owner.profile.track_credit = 1
        self.owner.profile.save()
        self.client.force_authenticate(user=self.owner)
        data = {"file": create_temp_track(), "group": self.inactive_group.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # No tracks should have been created
        self.assertEqual(Track.objects.count(), 0)

    def test_get_track_on_active_group(self):
        track = self.active_group.tracks.create(file="file1.wav")
        url = reverse("track-detail", args=[track.pk])

        # User is anon
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is not owner
        self.client.force_authenticate(user=self.non_owner)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # User is owner
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_track_on_inactive_group(self):
        track = self.inactive_group.tracks.create(file="file1.wav")
        url = reverse("track-detail", args=[track.pk])

        # User is anon
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is not owner
        self.client.force_authenticate(user=self.non_owner)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # User is owner
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_track_on_active_group(self):
        track = self.active_group.tracks.create(file="file1.wav")
        url = reverse("track-detail", args=[track.pk])

        # User is anon
        data = {"file": create_temp_track(), "group": self.active_group.pk}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is not owner
        self.client.force_authenticate(user=self.non_owner)
        data = {"file": create_temp_track(), "group": self.active_group.pk}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # User is owner
        self.client.force_authenticate(user=self.owner)
        data = {"file": create_temp_track(), "group": self.active_group.pk}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Track.objects.count(), 1)

    def test_update_track_on_inactive_group(self):
        track = self.inactive_group.tracks.create(file="file1.wav")
        url = reverse("track-detail", args=[track.pk])

        # User is anon
        data = {"file": create_temp_track(), "group": self.inactive_group.pk}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is not owner
        self.client.force_authenticate(user=self.non_owner)
        data = {"file": create_temp_track(), "group": self.inactive_group.pk}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # User is owner
        self.client.force_authenticate(user=self.owner)
        data = {"file": create_temp_track(), "group": self.inactive_group.pk}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Nothing should have changed
        self.assertEqual(Track.objects.count(), 1)
        self.assertEqual(Track.objects.get().file.name, "file1.wav")

    def test_delete_track_on_active_group(self):
        track = self.active_group.tracks.create(file="file1.wav")
        url = reverse("track-detail", args=[track.pk])

        # User is anon
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is not owner
        self.client.force_authenticate(user=self.non_owner)
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # User is owner
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Track.objects.count(), 0)

    def test_delete_track_on_inactive_group(self):
        track = self.inactive_group.tracks.create(file="file1.wav")
        url = reverse("track-detail", args=[track.pk])

        # User is anon
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is not owner
        self.client.force_authenticate(user=self.non_owner)
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # User is owner
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Nothing should have changed
        self.assertEqual(Track.objects.count(), 1)
        self.assertEqual(Track.objects.get().file.name, "file1.wav")


class CommentAPITests(APITestCase):
    def setUp(self):
        create_song_dependencies(self)

    def tearDown(self):
        """
        Manually remove the Comments, which will cause the files on disk
        to be removed by django-cleanup.
        This way running tests won't leave left-over files.
        """
        Comment.objects.all().delete()

    def test_create_comment_on_active_project(self):
        url = reverse("comment-list")
        data = {
            "content": "Test Comment",
            "attachment": create_temp_file("test.txt", "text/plain"),
            "project": self.active_project.pk,
        }

        # User is anon
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is not owner
        data["attachment"].seek(0)
        self.client.force_authenticate(user=self.non_owner)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is owner
        data["attachment"].seek(0)
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().content, "Test Comment")
        self.assertTrue(Comment.objects.get().attachment.name.endswith("test.txt"))

    def test_create_comment_on_inactive_project(self):
        url = reverse("comment-list")
        data = {"content": "Test Comment", "project": self.inactive_project.pk}

        # User is anon
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is not owner
        self.client.force_authenticate(user=self.non_owner)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is owner
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # No comments should have been created
        self.assertEqual(Comment.objects.count(), 0)

    def test_get_comment_on_active_project(self):
        comment = self.active_project.comments.create(
            content="Existing comment",
            author=self.owner
        )
        url = reverse("comment-detail", args=[comment.pk])

        # User is anon
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is not owner
        self.client.force_authenticate(user=self.non_owner)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # User is owner
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_comment_on_inactive_project(self):
        comment = self.inactive_project.comments.create(
            content="Existing comment",
            author=self.owner
        )
        url = reverse("comment-detail", args=[comment.pk])

        # User is anon
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is not owner
        self.client.force_authenticate(user=self.non_owner)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # User is owner
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_comment_on_active_project(self):
        comment = self.active_project.comments.create(
            content="Existing comment",
            author=self.owner
        )
        url = reverse("comment-detail", args=[comment.pk])
        data = {"content": "New content", "project": self.active_project.pk}

        # User is anon
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is not owner
        self.client.force_authenticate(user=self.non_owner)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # User is owner
        self.client.force_authenticate(user=self.owner)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().content, "New content")

    def test_update_comment_on_inactive_project(self):
        comment = self.inactive_project.comments.create(
            content="Existing comment",
            author=self.owner
        )
        url = reverse("comment-detail", args=[comment.pk])
        data = {"content": "New content", "project": self.inactive_project.pk}

        # User is anon
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is not owner
        self.client.force_authenticate(user=self.non_owner)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # User is owner
        self.client.force_authenticate(user=self.owner)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Nothing should have changed
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().content, "Existing comment")

    def test_delete_comment_on_active_project(self):
        comment = self.active_project.comments.create(
            content="Existing comment",
            author=self.owner
        )
        url = reverse("comment-detail", args=[comment.pk])

        # User is anon
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is not owner
        self.client.force_authenticate(user=self.non_owner)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # User is owner
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)

    def test_delete_comment_on_inactive_project(self):
        comment = self.inactive_project.comments.create(
            content="Existing comment",
            author=self.owner
        )
        url = reverse("comment-detail", args=[comment.pk])

        # User is anon
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User is not owner
        self.client.force_authenticate(user=self.non_owner)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # User is owner
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Nothing should have changed
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().content, "Existing comment")
