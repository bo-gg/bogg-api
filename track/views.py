from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.http import Http404
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from track.models import Bogger, CalorieEntry
from track.serializers import UserSerializer, GroupSerializer, BoggerSerializer, CalorieEntrySerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CalorieEntryList(APIView):
    """
    List all calorie_entries, or create a new calorie_entry.
    """
    def get(self, request, format=None):
        calorie_entries = CalorieEntry.objects.all()
        serializer = CalorieEntrySerializer(calorie_entries, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CalorieEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CalorieEntryDetail(APIView):
    """
    Retrieve, update or delete a calorie_entry instance.
    """
    def get_object(self, pk):
        try:
            return CalorieEntry.objects.get(pk=pk)
        except CalorieEntry.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        calorie_entry = self.get_object(pk)
        serializer = CalorieEntrySerializer(calorie_entry)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        calorie_entry = self.get_object(pk)
        serializer = CalorieEntrySerializer(calorie_entry, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        #TODO: Active = False?
        calorie_entry = self.get_object(pk)
        calorie_entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BoggerViewSet(viewsets.ModelViewSet):
    queryset = Bogger.objects.all()
    serializer_class = BoggerSerializer
