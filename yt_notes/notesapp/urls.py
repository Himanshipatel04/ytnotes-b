from django.urls import path
from . import views 

urlpatterns = [
    path("notes/",views.notes,name  = "notes"),
    path("notes/<slug:slug>/",views.note_detail,name  = "note_detail"),
    path("notes-search/",views.search_notes,name = "notes-search"),
]


#endpoints
#get all nodes and create new node : http://127.0.0.1:8000/notes/
#get single node : http://127.0.0.1:8000/notes/note-slug