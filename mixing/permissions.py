from __future__ import unicode_literals, absolute_import

import os

from rest_framework import permissions

from utils import slugify_filename


###################
# API Permissions #
###################

class ProjectIsActive(permissions.BasePermission):
    """
    Custom permission to only allow editing and deleting on active Projects.
    This will protect PUT and DELETE.
    """

    def has_object_permission(self, request, view, obj):
        """
        Traverse the foreign keys to determine if a Project is active.
        The obj param can be a Song, Group, or Track.
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        if hasattr(obj, "group"):  # Matches a Track
            obj = obj.group
        if hasattr(obj, "song"):  # Matches a Group
            obj = obj.song
        if hasattr(obj, "project"):  # Matches a Song
            return obj.project.active
        return False


####################
# File Permissions #
####################

def private_track_path(track, filename):
    """
    Determine the upload path for Track objects.
    """
    owner_id = str(track.group.song.project.owner.id)
    return os.path.join("tracks", owner_id, slugify_filename(filename))


def private_comment_path(comment, filename):
    """
    Determine the upload path for Comment objects.
    """
    owner_id = str(comment.project.owner.id)
    return os.path.join("comments", owner_id, slugify_filename(filename))


def private_final_path(final_file, filename):
    """
    Determine the upload path for FinalFile objects.
    """
    owner_id = str(final_file.project.owner.id)
    return os.path.join("finals", owner_id, slugify_filename(filename))


def allow_owner_and_staff(private_file):
    """
    Allow access to a file only if the user is owner or staff.
    Used by django-private-storage to serve private files.
    https://github.com/edoburu/django-private-storage#defining-access-rules

    This assumes all private paths will have the following format:
    /{section}/{owner ID}/{...}
    """
    staff_only = ["tracks"]
    path_parts = private_file.relative_name.split("/")
    user = private_file.request.user

    if not user.is_authenticated():
        return False

    if user.is_staff:
        return True

    section = path_parts[0]
    owner_id = int(path_parts[1])
    if section not in staff_only and user.id == owner_id:
        return True

    return False
