from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils.timezone import now
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail

from .serializer import UserSerializer, PasswordResetRequestSerializer, PasswordResetSerializer
from .models import CustomUser

class CreateUserView(CreateAPIView):
    """
    Signs user using the custom backed, which use email instead of username
    it requires 
    {email}
    {password}
    {username}
    """
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = UserSerializer



class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
    '''
    Authenticates user for login using the a custom login backends
    which uses email for authentication
    '''

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        

        #Authenticate user using the custom authenticate function from .backend
        authenticated_user = authenticate(request, username=email, password=password)

        if authenticated_user:
            #Login successful
            authenticated_user.last_login = now()
            authenticated_user.save()

            refresh_token = RefreshToken.for_user(authenticated_user)
            return Response({
                'refresh': str(refresh_token),
                 'access': str(refresh_token.access_token),
                 'id':authenticated_user.id
                })
        else:
            #Login gone wrong
            return Response({'msg':'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)




class PasswordResetRequestView(APIView):
    permission_classes = [IsAuthenticated]

    """
    Users Request password reset through this view.
    It generates a unique link for user to reset their password using the class:PasswordResetView:
    Combining :PasswordResetTokenGenerator: and a ('user.pk') to make unique link
    adds a layer security.
    Requires online email
    """
    
    def post(self, request, *args, **kwargs):
        #validate data passed by user i.e email

        data = request.data
        serializer = PasswordResetRequestSerializer(data=data)
        if serializer.is_valid():
            user = request.user
            """
            The password reset link consists of the host url, unique token and uid number generated from user's id
            """
            #make token for user
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            #uid for user from user's pk in db
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = 'http://localhost:8000/api/v1/user/reset-password?token=' + token + '&uid=' + uid

            #Send email to user to the provider email
            subject = 'Password Reset'
            message = f'Please follow this link to reset your password: {reset_url}'
            from_ = 'Meta Post <noreply@example.com>'
            recipient_list = [user.email]
            send_mail(
                subject=subject,
                message=message,
                from_email=from_,
                recipient_list=recipient_list,
                fail_silently=True
            )
            
            return Response(
                {
                    'msg': 'We have sent a link to reset your password.',
                     'link': reset_url
                 
                }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          


class PasswordResetView(APIView):
    permission_classes = [IsAuthenticated]
    '''
    Allows users to reset password using the link generated from --PasswordResetRequestView--
    Requires two new passwords that match
    '''

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = PasswordResetSerializer(data=data)
        if serializer.is_valid():
            #verify token and uid
            token = request.query_params.get('token')
            uid = request.query_params.get('uid')

            try:
                #decode uid into string
                pk = force_str(urlsafe_base64_decode(uid))
                user = CustomUser.objects.get(pk=pk)
                if user != request.user: #Wrong user tries to use the link
                    user = None
            except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
                user = None
            
            #Reset the password if token in link is correct
            token_generator = PasswordResetTokenGenerator()
            if user and token_generator.check_token(user, token):
                if serializer.validated_data['new_password'] == serializer.validated_data['re_password']:
                    user.set_password(serializer.validated_data['new_password'])
                    user.save()
                    return Response({'msg': 'Password has been reset successfully.'})
                else:
                    return Response({'msg': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'msg': 'Something went wrong verifying your identity'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg':'unexpected request data'}, status=status.HTTP_400_BAD_REQUEST)

            










            


