from __future__ import unicode_literals, absolute_import

import os

from private_storage.views import PrivateStorageView


class PrivateAttachment(PrivateStorageView):
    """
    Modifies the PrivateStorageView to return the response as an attachment.
    """

    def serve_file(self, private_file):
        filename = os.path.basename(private_file.full_path)
        response = super(PrivateAttachment, self).serve_file(private_file)
        response["Content-Disposition"] = "attachment; filename=\"%s\"" % filename
        return response
