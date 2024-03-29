from rest_framework import serializers, status
from rest_framework.response import Response
from .models import CustomUser, OtpVerification
from .utility import send_otp_mail
from django.utils import timezone
from django.contrib.auth import authenticate
from django.utils.translation import gettext as _


class OtpVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        max_length=128, style={'input_type': 'password'}, trim_whitespace=False, required=False)
    extra_kwargs = {'password': {'write_only': True}}
    username = serializers.CharField(
        max_length=100, allow_blank=True, required=False)
    otp = serializers.CharField(max_length=6, required=False)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        try:
            otp = send_otp_mail(attrs.get('email'))
            attrs['otp'] = otp
            print(f"----------------------validate-------- {attrs['otp']}")

        except Exception as e:
            raise serializers.ValidationError(
                {"message": f"Failed to send email. Reason: {str(e)}"})
        return attrs

    def create(self, validated_data):
        user = OtpVerification.objects.create_unverified_user(
            email=validated_data['email'],
            password=validated_data['password'],
            # otp is passed to validated data in the view
            otp=validated_data['otp'],
            username=validated_data['username']
        )
        print(f'----------------------create-------- {user.otp}')

        return user

    def update(self, instance, validated_data):

        # Update existing user's password and OTP

        instance.otp = validated_data['otp']
        print(f"----------------------update-------- {validated_data['otp']}")
        instance.set_password(validated_data['password'])
        instance.created_at = timezone.now()
        instance.expires_at = timezone.now()+timezone.timedelta(minutes=1)
        instance.save()
        return instance


class AuthSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):

        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password
        )

        if not user:
            msg = _('unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user

        return attrs


class CustomUserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user
