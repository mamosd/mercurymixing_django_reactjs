# Mercury Mixing

This website allows users to upload and organize "tracks" (drums, guitars,
vocals, etc) and have them mixed by experienced mixing engineers. You can see
it as a file organization and exchange application.

- Mezzanine for content management
- Django REST Framework for the Mixing API
- React / Redux for the Mixing frontend

Note: The Mixing fronted has it's own README (see `mixing/frontend/README.md`).

## Projects

The Project model (`mixing.models.Project`) is the foundation for all user
interaction with the site. A Project organizes the user-uploaded Tracks in this
manner:

```
Project
  |-- Comment
  |-- FinalFile
  `-- Song
      `-- Group
          `-- Track
```

**The user-uploaded `Tracks` are organized in `Groups` and `Songs` inside a
`Project`. Both users and staff members can add `Comments` to a `Project` to
communicate and include reference attachments. Finally, staff members can add
`FinalFiles`, which are the result of the mixing process based on the original
`Tracks`. Users can then download the `FinalFiles`, which completes the
`Project`.**

### Project life cycle

A Project usually goes through the following phases (each `STATUS` is an
attribute of the `Project` model):

- User creates the project and starts uploading files (`STATUS_FILES_PENDING`)
- User finishes all uploads and mixing starts (`STATUS_IN_PROGRESS`)
- Staff members mix the files and finalize the project (`STATUS_COMPLETE`)

After this, the user has the option of requesting revisions (by writing a
Comment on the Project or contacting staff in some other way):

- File uploads can be re-enabled if needed (`STATUS_REVISION_FILES_PENDING`)
- ...or just use the previous files (`STATUS_REVISION_IN_PROGRESS`)
- After the revision, the project is complete again
  (`STATUS_REVISION_COMPLETE`)

The active flag indicates if file uploads are enabled for the users. File
uploads should only be enabled on `STATUS_FILES_PENDING` and
`STATUS_REVISION_FILES_PENDING`. See `Project.save()`.

### Project priorities

Another feature of the Projects is the priority number. This tells the staff
which Projects need to be mixed ASAP, and which ones can wait for a bit.
Priority 10 means a Project is waiting for the user or is completed, while
priority 0 means a Project needs to be mixed and delivered as soon as possible.

Whenever the project is waiting for the user's files (`STATUS_FILES_PENDING`,
`STATUS_REVISION_FILES_PENDING`) the priority is set to 10 (not important),
since the staff cannot work on the project until all files are uploaded.

When a Project is marked as `STATUS_IN_PROGRESS` or
`STATUS_REVISION_IN_PROGRESS` the priority is set to 9, and will decrease every
day. The closer a Project is to priority 0, the more urgent it is to complete
it, since it has been in the queue longer than others. TODO: Document priority
management command.

Finally, when a project is marked as `STATUS_COMPLETE` or
`STATUS_REVISION_COMPLETE` the priority is again set to 10 to remove it from
the priority queue.

## Notes

- **Running tests**: To run tests, run `python manage.py test mixing.tests
  mixing.purchases`. Trying to run `test` directly on `mixing` will result in a
  bunch of import errors.

- **Testing DB**: The project has been developed and runs on a Postgres
  database. Trying to run the test suite on SQLite will result in failing tests
  because SQLite doesn't raise `IntegrityError`, which is used in a few places
  in the code. This means that the Postgres user that runs the development
  database must also have permission to create new databases. You can achieve
  this in `psql` by running: `ALTER USER username CREATEDB;`.
