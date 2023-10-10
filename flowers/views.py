from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from flowers.models import Flower
from flowers.serializers import FlowerListSerializer, FlowerUploadSerializer
from utils import decrypt, get_encryption_key


class UserFlowerListView(generics.ListAPIView):
    serializer_class = FlowerListSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List all flowers uploaded by the authenticated user.",
    )
    def get_queryset(self):
        return Flower.objects.filter(user=self.request.user)


class FlowerImageView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve the image of a specific flower. Accessible only by the flower's uploader.",
    )
    def get(self, request, flower_id):
        try:
            flower = Flower.objects.get(pk=flower_id)

            if flower.user != request.user:
                return Response({"detail": "Permission denied."}, status=403)

            key = get_encryption_key()

            decrypted_data = decrypt(flower.photo, key)
            return HttpResponse(decrypted_data, content_type="image/jpeg")

        except Flower.DoesNotExist:
            return Response({"detail": "Flower not found."}, status=404)


class FlowerUploadView(views.APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Upload a flower image and set its price."
    )
    def post(self, request):
        serializer = FlowerUploadSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Flower uploaded successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
