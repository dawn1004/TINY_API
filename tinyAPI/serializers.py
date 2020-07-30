from rest_framework import serializers


# class TinyResponseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TinyResponse
#         fields = ['response', ]
class TinyResponseSerializer(serializers.Serializer):
    response = serializers.CharField(max_length=100)

    def create(self, TinyResponseSerializer):
        return TinyResponseSerializer.objects.create(self.response)
