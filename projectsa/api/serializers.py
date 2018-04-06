from rest_framework import serializers


class EditDistanceSerializer(serializers.Serializer):
    """Serializer for calculating EditDistance.
    """

    first_string = serializers.CharField(
        help_text='First String to calculate edit distance',
    )
    second_string = serializers.CharField(
        help_text='Second String to calculate edit distance',
    )
