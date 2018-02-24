from __future__ import unicode_literals, absolute_import

from zipfile import ZipFile, ZIP_DEFLATED
import re

from django.conf.urls import url
from django.contrib import admin
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404, HttpResponse
from django.template import Context, loader
from django.utils.html import mark_safe
from django.utils.six import b
from django.utils.timezone import now, get_default_timezone

from mezzanine.core.admin import StackedDynamicInlineAdmin, TabularDynamicInlineAdmin

from .models import Project, Track, Comment, FinalFile

TZ = get_default_timezone()


def to_folder_name(value):
    """
    Only allow alphanumeric characters, dashes, and spaces.
    """
    value = re.sub(r"[^ \w-]", "", value).strip()
    return value if len(value) else "unknown_name"


def serve_tracks_as_zipfile(request, pk):
    """
    Create a Zip archive with all the Tracks in a Project.
    The Tracks will be organized in folders according to Songs and Groups.
    Based on https://github.com/thibault/django-zipview/
    """
    project = get_object_or_404(Project, pk=pk)
    timestamp = now().astimezone(TZ).strftime("%Y-%m-%d %H-%M-%S")
    name = "%s %s.zip" % (to_folder_name(project.title), timestamp)
    temp_file = ContentFile(b(""), name=name)

    with ZipFile(temp_file, mode="w", compression=ZIP_DEFLATED) as zip_file:
        for track in Track.objects.filter(group__song__project=project):
            path = "{}/{}/{}".format(
                to_folder_name(track.group.song.title),
                to_folder_name(track.group.title),
                track.file.name.split("/")[-1]
            )
            zip_file.writestr(path, track.file.read())

    file_size = temp_file.tell()
    temp_file.seek(0)

    response = HttpResponse(temp_file, content_type="application/zip")
    response["Content-Disposition"] = "attachment; filename=\"%s\"" % name
    response["Content-Length"] = file_size
    return response


class CommentInlineAdmin(StackedDynamicInlineAdmin):
    model = Comment
    fields = ["created", "author", "content", "attachment"]
    readonly_fields = ["created", "author"]


class FinalFileInlineAdmin(TabularDynamicInlineAdmin):
    model = FinalFile
    fields = ["created", "title", "attachment"]
    readonly_fields = ["created"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [FinalFileInlineAdmin, CommentInlineAdmin]
    ordering = ["priority", "-created"]
    date_hierarchy = "created"
    list_display = ["title", "owner", "created", "status", "priority"]
    list_editable = ["priority"]
    list_filter = ["status"]
    search_fields = ["title", "owner__username"]
    readonly_fields = ["created", "updated", "track_browser"]
    fieldsets = (
        (None, {
            "fields": ["title", "owner", "created", "updated", "status", "priority"],
        }),
        ("Tracks", {
            "fields": ["track_browser"],
            "classes": ("collapse-closed",)
        }),
    )

    class Media:
        """
        Include our style and script customizations for the Project admin.
        """
        css = {
            "all": ("admin/mixing/styles.css",),
        }
        js = ("admin/mixing/scripts.js",)

    def save_formset(self, request, form, formset, change):
        """
        Populate the author field on inline Comments since it's marked as read-only.
        """
        if formset.model is Comment:
            comments = formset.save(commit=False)
            for comment in comments:
                if not comment.author_id:
                    comment.author = request.user
                comment.save()
            formset.save_m2m()
        else:
            super(ProjectAdmin, self).save_formset(request, form, formset, change)

    def get_urls(self):
        """
        Add our custom admin views.
        """
        info = self.model._meta.app_label, self.model._meta.model_name
        default_urls = super(ProjectAdmin, self).get_urls()
        urls = [
            url(
                r"^(?P<pk>[0-9]+)/download/$",
                self.admin_site.admin_view(serve_tracks_as_zipfile),
                name="%s_%s_download" % info
            ),
        ]
        return urls + default_urls

    def track_browser(self, project=None):
        """
        Generates a collapsible tree of Songs / Groups / Tracks.
        """
        template = loader.get_template("admin/mixing/includes/track_browser.html")
        context = Context({"project": project})
        output = template.render(context)
        # Remove all newlines because Django converts them into <br>
        nonewlines = re.sub(r"[\n\r\t]+", "", output)
        return mark_safe(nonewlines)
