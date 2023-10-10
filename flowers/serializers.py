from rest_framework import serializers

from flowers.models import Flower
from utils import encrypt, get_encryption_key


class FlowerUploadSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(write_only=True)

    class Meta:
        model = Flower
        fields = ["photo", "price", "created_at", "updated_at"]

    def create(self, validated_data):
        key = get_encryption_key()
        encrypted_data = encrypt(validated_data["photo"].read(), key)

        flower = Flower(photo=encrypted_data, price=validated_data["price"])
        flower.user = self.context["request"].user
        flower.save()
        return flower

class FlowerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flower
        fields = ["id", "photo", "price", "created_at", "updated_at"]
        ordering = ['-created_at']
