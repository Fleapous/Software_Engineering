from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AdSpace, Rating
from .serializers import AdSpaceSerializer, RatingSerializer


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


# class RatingList(generics.ListAPIView):
#     queryset = Rating.objects.all()
#     serializer_class = RatingSerializer

class RatingList(APIView):
    def get(self, request):
        ratings = Rating.objects.all()
        rating_data = []

        # Group ratings by ad space ID
        ad_space_ids = set(rating.adSpace_id for rating in ratings)
        for ad_space_id in ad_space_ids:
            ad_space_ratings = ratings.filter(adSpace_id=ad_space_id)
            ad_space_data = {
                'id': ad_space_id,
                'reviews': []
            }

            # Add each review to the ad space data
            for rating in ad_space_ratings:
                review = {
                    'title': rating.title,
                    'description': rating.description,
                    'date': rating.date.strftime('%B %d, %Y'),  # Format date as desired
                    'rating': rating.rating,
                    'name': rating.client.username  # Assuming 'client' is a ForeignKey to your custom User model
                }
                ad_space_data['reviews'].append(review)

            rating_data.append(ad_space_data)

        return Response(rating_data)

class CreateRating(APIView):
    def post(self, request):
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetRating(APIView):
    def get(self, request, pk):
        rating = get_object_or_404(Rating, pk=pk)
        serializer = RatingSerializer(rating)
        return Response(serializer.data)

class UpdateRating(APIView):
    def put(self, request, pk):
        rating = get_object_or_404(Rating, pk=pk)
        serializer = RatingSerializer(rating, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteRating(APIView):
    def delete(self, request, pk):
        rating = get_object_or_404(Rating, pk=pk)
        rating.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)