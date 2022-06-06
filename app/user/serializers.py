from django.db import transaction
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer

from core.models import CustomUser
# from core.models import GENDER_SELECTION, CustomUser


class CustomRegisterSerializer(RegisterSerializer):
    # gender = serializers.ChoiceField(choices=GENDER_SELECTION)
    phone_number = serializers.CharField(max_length=30)
    ahjin_coin = serializers.FloatField(default=0)
    user_hash = serializers.CharField(max_length=255, required=False)


    # Define transaction.atomic to rollback the save operation in case of error
    @transaction.atomic
    def save(self, request):
        print(f"request is: {request.data}")
        user = super().save(request)
        # user.gender = self.data.get('gender')
        user.phone_number = self.data.get('phone_number')
        user.ahjin_coin = self.data.get('ahjin_coin')
        user.user_hash = self.data.get('user_hash')
        user.save()
        return user


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    
    # profile = CustomRegisterSerializer(source='CustomUser')

    class Meta:
        model = CustomUser
        fields = (
            'pk',
            'email',
            'phone_number',
            # 'gender',
            'ahjin_coin',
            'user_hash'
        )
        read_only_fields = ('pk', 'email', )
    
    # def update(self, instance, validated_data):
    #     """
    #     Update a user
    #     """

    #     customuser_serializer = self.fields['profile']
    #     customuser_instance = instance.customuser
    #     print(f"Instance is: {instance}")
    #     print(f"Validated data is : {validated_data}")
    #     customuser_data = validated_data.pop('customuser', {})

    #     phone_number = customuser_data.get('phone_number')
    #     ahjin_coin = customuser_data.get('ahjin_coin')
    #     user_hash = customuser_data.get('user_hash')

    #     if phone_number:
    #         customuser_serializer.update(customuser_instance, )

