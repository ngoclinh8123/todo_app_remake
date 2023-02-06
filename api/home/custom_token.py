# from django.contrib.auth import authenticate

# from rest_framework_simplejwt.serializers import TokenRefreshSerializer
# from rest_framework_simplejwt.views import TokenRefreshView
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework import status

# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.settings import api_settings
# from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

# from .views import get_user_token
# from .models import CustomUser


# class MyTokenRefreshView(TokenRefreshView):
#     serializer_class = TokenRefreshSerializer

#     def handle_token(self, tokenAccess):
#         return tokenAccess.split(".")[-1]

#     def get_user(self, request):
#         tokenAccess = get_user_token(request)
#         tokenSignature = self.handle_token(tokenAccess)
#         user = CustomUser.objects.filter(tokenSignature=tokenSignature)
#         return user

#     def post(self, request):
#         user = self.get_user(request)
#         if not user.exists():
#             return Response("no user found", status=status.HTTP_400_BAD_REQUEST)

#         serializer = TokenRefreshSerializer(data=request.data)
#         try:
#             serializer.is_valid(raise_exception=True)
#         except TokenError as e:
#             raise InvalidToken(e.args[0])

#         newToken = serializer.validated_data["access"]
#         newTokenSignature = self.handle_token(newToken)

#         user.update(tokenSignature=newTokenSignature)

#         return Response(serializer.validated_data, status=status.HTTP_200_OK)


# khi access token hết hạn sau đó dùng refresh token để lấy token mới + cập nhật lại token signature
# # https://viblo.asia/p/refresh-token-la-gi-cach-hoat-dong-co-khac-gi-so-voi-token-khong-E375zQB2lGW
# Phường cấp cho tôi 1 cái giấy đi đường (theo tên trong giấy CMND của tôi). Hiệu lược 1 tuần. Hết 1 tuần tôi cầm CMND lên phường xin cấp lại 1 giấy đi đường khác.

# Trường hợp khác, Phường cấp cho tôi 1 cái giấy đi đường (tên tôi trong đó). Hiệu lược 1 tuần. Tôi đánh rơi, người khác nhặt được, dùng giấy đi đường của tôi, hết 1 tuần nó đem lên phường, phường nhìn cái giấy đi đường cũ hết hạn cấp lại 1 giấy mới, với tên của tôi cho thằng đó. Như vậy có ổn không?
