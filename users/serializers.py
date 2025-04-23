from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

# class UserSerializer(serializers.ModelSerializer):
#     password2 = serializers.CharField(write_only=True, required=True)  # Thêm riêng trường password2

#     class Meta:
#         model = User
#         fields = ["id", "username", "email", "phone", "password", "password2"]
#         extra_kwargs = {"password": {"write_only": True},
#                         "password2": {"write_only": True}}

#     def validate(self, data):
#         """
#         Kiểm tra mật khẩu có khớp không trước khi lưu user.
#         """
#         if data.get("password") != data.get("password2"):
#             raise serializers.ValidationError({"password": "Mật khẩu không khớp."})

#         return data

#     def create(self, validated_data):
#         """
#         Tạo user với mật khẩu được mã hóa.
#         """
#         validated_data.pop("password2")  # Xóa password2 trước khi lưu user
#         user = User.objects.create_user(
#             username=validated_data["username"],
#             email=validated_data["email"],
#             phone=validated_data.get("phone", ""),
#             password=validated_data["password"]
#         )
#         return user
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'phone', 'role']

class RegisterUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "phone", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True},
                        "password2": {"write_only": True}}

    def validate(self, data):
        if data.get("password") != data.get("password2"):
            raise serializers.ValidationError({"password": "Mật khẩu không khớp."})
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            phone=validated_data.get("phone", ""),
            password=validated_data["password"]
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'role']
