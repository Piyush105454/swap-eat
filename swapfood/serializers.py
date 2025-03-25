from rest_framework import serializers
from .models import FoodImage
import base64

class FoodImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True)  # Accepts image upload
    image_base64 = serializers.SerializerMethodField()  # Returns Base64 string

    class Meta:
        model = FoodImage
        fields = ['image', 'image_base64']

    def create(self, validated_data):
        image_file = validated_data.pop('image')
        image_data = image_file.read()  # Read binary data
        return FoodImage.objects.create(image_data=image_data, **validated_data)

    def get_image_base64(self, obj):
        if obj.image_data:
            return base64.b64encode(obj.image_data).decode('utf-8')  # Convert to Base64
        return None
