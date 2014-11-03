"""Hello World API implemented using Google Cloud Endpoints.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""


import endpoints
from protorpc import messages, message_types, remote # TODO remove messages and message types when possible
from google.appengine.ext import ndb

from libs.endpoints_proto_datastore.ndb import EndpointsModel


WEB_CLIENT_ID = ""  # TODO make this secure
ANDROID_CLIENT_ID = ""  # TODO figure out android at some point
IOS_CLIENT_ID = ""  # probably not, unless I get some help
ANDROID_AUDIENCE = WEB_CLIENT_ID


class Note(EndpointsModel):
    title = ndb.StringProperty()
    content = ndb.StringProperty()
    date_created = ndb.DateTimeProperty(auto_now_add=True)
    owner = ndb.UserProperty()

'''
class NoteMessage(messages.Message):
    title = messages.StringField(1)
    content = messages.StringField(2)
    # Hotness
    hotness = messages.IntegerField(3, default=0)
    # Color
    color = messages.BytesField(4, default="#ffffff")
    # Attach
        # Due Date
    due_date = message_types.DateTimeField(5)
        # Reminder
    reminders = message_types.DateTimeField(6, repeated=True)
        # Task : is a note
        # Note
    sub_notes = messages.MessageField("Note", 7, repeated=True)
        # Image : is a file
        # File
    # A URL to a file.  The file can probably be served by the datastore.
    files = messages.BytesField(8, repeated=True)

    #dsid = messages.BytesField(12, required=True)
    #date_created = message_types.DateTimeField(9, required=True)
    #date_updated = message_types.DateTimeField(10, required=True)
    #date_accessed = message_types.DateTimeField(11, required=True)

class NoteCollectionMessage(messages.Message):
    items = messages.MessageField(Note, 1, repeated=True)


FOO_NOTES = NoteCollection(items=[
    Note(#dsid="esgihsel",
         title="my first note!",
         content="this is my very first note"),
    Note(#dsid="3f2o02hg",
         title="my second note!",
         content="i have more notes"),
    Note(#dsid="0evwhfwf",
         title="my third note!",
         content="",
         color=None,
         hotness=2),
    Note(#dsid="rkbn31ha",
         title="my first note"),
    ])
'''


@endpoints.api(name="remember", version="v1",
               allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID,
                                   endpoints.API_EXPLORER_CLIENT_ID],
               audiences=[ANDROID_AUDIENCE],
               scopes=[endpoints.EMAIL_SCOPE])
class EndpointsTestAPI(remote.Service):
    """This is a test for Endpoints, a learning experience."""

    #@endpoints.method(message_types.VoidMessage, NoteCollection,
    #                  path="notes", http_method="GET",
    #                  name="notes.list")
    #def notes_list(self, request):
    #    return FOO_NOTES

    @Note.method(user_required=True,
                 path="note", http_method="PUT", name="note.add")
    def note_add(self, note):
        note.owner = endpoints.get_current_user()
        note.put()
        return note

    @Note.query_method(user_required=True,
                       path="notes", http_method="GET", name="notes.list")
    def notes_list(self, query):
        return query.filter(Note.owner == endpoints.get_current_user())


application = endpoints.api_server([EndpointsTestAPI])
