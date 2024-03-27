from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AdSpace
from .serializers import AdSpaceSerializer


class AdSpaceList(generics.ListAPIView):
    queryset = AdSpace.objects.all()
    serializer_class = AdSpaceSerializer


class CreateAdSpace(APIView):
    def post(self, request):
        serializer = AdSpaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAdSpace(APIView):
    def get(self, request, pk):
        adspace = get_object_or_404(AdSpace, pk=pk)
        serializer = AdSpaceSerializer(adspace)
        return Response(serializer.data)


class UpdateAdSpace(APIView):
    def put(self, request, pk):
        adspace = get_object_or_404(AdSpace, pk=pk)
        serializer = AdSpaceSerializer(adspace, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAdSpace(APIView):
    def delete(self, request, pk):
        adspace = get_object_or_404(AdSpace, pk=pk)
        adspace.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
