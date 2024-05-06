from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AdSpace, Rating, Booking, Payment
from user_management.models import User
from .serializers import AdSpaceSerializer, RatingSerializer, BookingSerializer, PaymentSerializer, NotApprovedAdSpaceSerializer


class ApprovedAdSpaceList(generics.ListAPIView):
    serializer_class = AdSpaceSerializer

    def get_queryset(self):
        return AdSpace.objects.filter(isApproved=True)

class NotApprovedAdSpaceList(generics.ListAPIView):
    serializer_class = NotApprovedAdSpaceSerializer  # Use the new serializer

    def get_queryset(self):
        # Get the queryset of AdSpace objects not approved
        queryset = AdSpace.objects.filter(isApproved=False)

        # Fetch the related owner objects separately
        owner_ids = queryset.values_list('owner', flat=True).distinct()
        owners = User.objects.filter(pk__in=owner_ids)

        # Convert owners queryset to a dictionary for efficient lookup
        owners_dict = {owner.id: owner for owner in owners}

        # Attach owner data to each AdSpace object
        for ad_space in queryset:
            ad_space.owner_data = owners_dict.get(ad_space.owner_id)

        return queryset


class CreateAdSpace(APIView):
    def post(self, request):
        request.data['isApproved'] = False

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


class BookingListView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def list(self, request, *args, **kwargs):
        bookings = self.get_queryset()
        ad_space_bookings = {}
        for booking in bookings:
            ad_space_id = booking.adSpace_id
            if ad_space_id not in ad_space_bookings:
                ad_space_bookings[ad_space_id] = []
            ad_space_bookings[ad_space_id].append(booking)

        booking_data = []
        for ad_space_id, bookings in ad_space_bookings.items():
            ad_space_data = {
                'id': ad_space_id,
                'bookings': BookingSerializer(bookings, many=True).data
            }
            booking_data.append(ad_space_data)

        return Response(booking_data)
    
    
class FetchBookings(APIView):
    def get(self, request):
        bookings = Booking.objects.all()
        booking_list = []
        for booking in bookings:
            booking_data = {
                'id': booking.id,
                'bookingDate': booking.bookingDate,
                'status': booking.status,
                'adSpace_id': booking.adSpace_id,
                'client_id': booking.client_id,
            }
            booking_list.append(booking_data)
        return Response(booking_list)


    
class BookingCreateView(APIView):
    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingDeleteView(generics.DestroyAPIView):
    queryset = Booking.objects.all()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class PaymentList(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class CreatePayment(APIView):
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetPayment(APIView):
    def get(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)


class UpdatePayment(APIView):
    def put(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        serializer = PaymentSerializer(payment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeletePayment(APIView):
    def delete(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        payment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
