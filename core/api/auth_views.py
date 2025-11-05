# core/api/auth_views.py
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from core.models import MasterUser
from .serializers import MasterUserSerializer

# IMPORTANT: OTP/SMS system is intentionally DISABLED per your request.
# The endpoints below exist but WILL NOT SEND ANY OTP OR EMAIL.
# They return informative messages and placeholders for future implementation.

class LoginView(APIView):
    """
    Username/password login (used for BMMU & Admin).
    CRPs may also use username/password login for now.
    Returns JWT tokens on success.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'detail':'username and password required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({'detail':'invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # Create JWT
        refresh = RefreshToken.for_user(user)
        try:
            mu = MasterUser.objects.using('master').get(username=user.username)
        except MasterUser.DoesNotExist:
            return Response({'detail': 'master user missing'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        s = MasterUserSerializer(mu)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': s.data
        })


class CRPRequestOtpView(APIView):
    """
    PLACEHOLDER: OTP REQUEST endpoint.
    NOTE: per instructions, this endpoint DOES NOT generate or send OTPs at the moment.
    When you later integrate SMS provider, implement sending here and remove the immediate return.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        # Just respond that OTP capability is disabled now.
        return Response({
            'detail': 'OTP feature currently disabled. Use username/password login. Placeholder present for future SMS/OTP integration.'
        }, status=status.HTTP_200_OK)

    # --- Example of future implementation (commented) ---
    # def post(self, request):
    #     username = request.data.get('username')
    #     # find user in master DB, validate role == 'crp_ep'
    #     # generate OTP, store in Redis or DB
    #     # send via SMS provider (Twilio/MSG91/Gupshup...)
    #     # return 200 OK
    #     pass


class CRPVerifyOtpView(APIView):
    """
    PLACEHOLDER: OTP VERIFY endpoint.
    NOTE: per instructions, this endpoint DOES NOT verify OTPs at the moment.
    When you later integrate OTP store & provider, implement verification here and issue JWTs.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        return Response({
            'detail': 'OTP verification currently disabled. Use username/password login. Placeholder present for future integration.'
        }, status=status.HTTP_200_OK)

    # --- Example future implementation (commented) ---
    # def post(self, request):
    #     # verify OTP from Redis/DB, if valid create/return JWT just like in LoginView
    #     pass
