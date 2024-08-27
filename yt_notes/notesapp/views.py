from django.shortcuts import render
from notesapp.models import Note
from notesapp.serializers import noteSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Q

@api_view(["GET"])
def search_notes(request):
    query = request.query_params.get("search", "")
    if query:
        notes = Note.objects.filter(
            Q(title__icontains=query) | 
            Q(body__icontains=query) | 
            Q(category__icontains=query)
        )
    else:
        notes = Note.objects.all()
    
    serializer = noteSerializer(notes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET", "POST"])
def notes(request):
    if request.method == "GET":
        notes = Note.objects.all()
        serializer = noteSerializer(notes, many=True)
        return Response(serializer.data)
    
    if request.method == "POST":
        serializer = noteSerializer(data=request.data)
        if serializer.is_valid():  
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

@api_view(['GET',"PUT","DELETE"])
def note_detail(request,slug):
    try:
        note = Note.objects.get(slug=slug)
    except Note.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = noteSerializer(note)
        return Response(serializer.data)
    
    elif request.method == "PUT":
        serializer = noteSerializer(note,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == "DELETE":
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
