from rest_framework import serializers

from house.models import House


class HouseSearchParamSerializer(serializers.Serializer):

    page_number = serializers.IntegerField(min_value=1, default=1)
    latitude = serializers.FloatField(min_value=-90, max_value=90)
    longitude = serializers.FloatField(min_value=-180, max_value=180)
    min_budget = serializers.IntegerField(min_value=1, required=False)
    max_budget = serializers.IntegerField(min_value=1, required=False)
    min_bedrooms = serializers.IntegerField(min_value=1, required=False)
    max_bedrooms = serializers.IntegerField(min_value=1, required=False)
    min_bathrooms = serializers.IntegerField(min_value=1, required=False)
    max_bathrooms = serializers.IntegerField(min_value=1, required=False)

    def validate(self, data):
        validated_data = super().validate(data)
        if not validated_data.get('min_budget') and not validated_data.get('max_budget'):
            raise serializers.ValidationError(
                "Either min_budget or max_budget must be present"
            )
        if not validated_data.get('min_bedrooms') and not validated_data.get('max_bedrooms'):
            raise serializers.ValidationError(
                "Either min_bedrooms or max_bedrooms must be present"
            )
        if not validated_data.get('min_bathrooms') and not validated_data.get('max_bathrooms'):
            raise serializers.ValidationError(
                "Either min_bathrooms or max_bathrooms must be present"
            )
        return validated_data
