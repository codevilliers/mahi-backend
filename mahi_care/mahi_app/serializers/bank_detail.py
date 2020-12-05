from rest_framework import serializers

from mahi_app.models import BankDetail


class BankDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankDetail
        fields = '__all__'
