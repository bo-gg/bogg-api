from django.shortcuts import render, get_object_or_404

from django.contrib.auth.models import User, Group
from django.http import Http404
from rest_framework import viewsets, permissions, status, renderers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import detail_route


from track.models import Bogger, CalorieEntry, DailyEntry, Goal
from track.serializers import UserSerializer, GroupSerializer, BoggerSerializer, \
                              CalorieEntrySerializer, DailyEntrySerializer, GoalSerializer
from track.permissions import IsOwnerOrStaff




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



class CalorieEntryViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = CalorieEntry.objects.all()
    serializer_class = CalorieEntrySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(bogger=self.request.user.bogger)


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


class DailyEntryList(APIView):
    """
    List all daily_entries, or create a new daily_entry.
    """
    def get(self, request, format=None):
        daily_entries = DailyEntry.objects.all()
        serializer = DailyEntrySerializer(daily_entries, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DailyEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DailyEntryDetail(APIView):
    """
    Retrieve, update or delete a daily_entry instance.
    """
    def get_object(self, pk):
        try:
            return DailyEntry.objects.get(pk=pk)
        except DailyEntry.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        daily_entry = self.get_object(pk)
        serializer = DailyEntrySerializer(daily_entry)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        daily_entry = self.get_object(pk)
        serializer = DailyEntrySerializer(daily_entry, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        #TODO: Active = False?
        daily_entry = self.get_object(pk)
        daily_entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BoggerViewSet(viewsets.ModelViewSet):
    queryset = Bogger.objects.all()
    serializer_class = BoggerSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsOwnerOrStaff,)

    @detail_route(renderer_classes=(renderers.StaticHTMLRenderer,))
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(bogger=self.request.user.bogger)

    def retrieve(self, request, pk=None):
        queryset = Bogger.objects.all()
        bogger = get_object_or_404(queryset, pk=pk)
        serializer = BoggerSerializer(request.user.bogger)
        return Response(serializer.data)
