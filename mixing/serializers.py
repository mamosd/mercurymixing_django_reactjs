from __future__ import unicode_literals, absolute_import

from rest_framework import serializers

from utils import get_user_display

from .models import Project, Song, Group, Track, Comment


##########
# Fields #
##########

class FileMetaDataField(serializers.FileField):
    """
    A FileField with a dictionary representation of its metadata.
    """
    def to_representation(self, value=None):
        try:
            return {
                "name": value.name.split("/")[-1],
                "size": value.size,
                "url": getattr(value, "url", None),
            }
        except (OSError, AttributeError, ValueError):
            return {}


###############
# Serializers #
###############

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("title", "active", "id")
        read_only_fields = fields


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ("project", "title", "id")
        read_only_fields = ("id",)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("song", "title", "id")
        read_only_fields = ("id",)


class TrackSerializer(serializers.ModelSerializer):
    file = FileMetaDataField()

    class Meta:
        model = Track
        fields = ("group", "file", "id")
        read_only_fields = ("id",)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    attachment = FileMetaDataField(required=False)

    class Meta:
        model = Comment
        fields = ("id", "project", "author", "content", "attachment", "created")
        read_only_fields = ("id", "author", "created")

    def get_author(self, comment):
        return get_user_display(comment.author)
