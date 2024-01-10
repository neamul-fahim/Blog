from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, OtpVerification
from .serializers import OtpVerificationSerializer, AuthSerializer, CustomUserModelSerializer
from .utility import send_email, get_token_from_request, country_code, designations
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from rest_framework import generics


class LoginView(View):
    # def get(self, request):
    #     return render(request, 'user_management/signup.html')

    def get(self, request):
        # print(f"---------------GET--------CreateTokenView------------")
        return render(request, 'user_management/login.html')


class SignupView(View):
    def get(self, request):
        # print("-----------------SighupView")
        return render(request, 'user_management/signup.html')


class OTPView(View):
    def get(self, request, *args, **kwargs):
        # print(f"-------------------Get------------------UserAccountView--------")
        email = request.GET.get('email')
        # print(f"------Get------UserAccountView-------- {email}")

        # email = kwargs.get('email')

        # print(f"------Get------UserAccountView-------- {email}")

        if email:
            return render(request, 'user_management/otp_verification.html', {'email': email})
        else:
            return HttpResponse("Email not found in query parameters", status=400)


class HomeView(View):
    def get(self, request, *args, **kwargs):

        try:
            # print(f"---------------GET--------Home------------")
            token = request.headers.get(
                'Authorization', '').replace('Bearer ', '')
            # print(f"---------------GET--------Home------------{token}")

            return render(request, 'user_management/home_page.html')
        except Exception as e:
            # Log the exception for debugging
            print(f"Exception: {e}")
            # Return a generic error response
            return HttpResponse("Internal Server Error", status=500)


class UserProfileView(View):
    def get(self, request, *args, **kwargs):
        # print(f"---------------GET--------Home------------")

        return render(request, 'user_management/user_profile.html')


class SignupAPIView(APIView):

    def post(self, request, *args, **kwargs):  # username,email,password
        # print(f"----------------------OtpVerificationView--------")
        # raw_user_data = request.POST
        raw_user_data = request.data
        try:
            # checking if user has already registered
            user = CustomUser.objects.get(email=raw_user_data['email'])

            return Response("User already exists", status=status.HTTP_400_BAD_REQUEST)
        except:
            try:
                instance = OtpVerification.objects.get(
                    email=raw_user_data['email'])
                serializer = OtpVerificationSerializer(
                    instance=instance, data=raw_user_data)
            except:
                serializer = OtpVerificationSerializer(data=raw_user_data)

            serializer.is_valid(raise_exception=True)
            serializer.save()
            # return redirect('user_account', email=raw_user_data['email'])
            return Response('otp sent', status=status.HTTP_200_OK)


class UserAccountView(APIView):

    # def get(self, request, *args, **kwargs):
    #     print(f"-------------------Get------------------UserAccountView--------")
    #     # email = request.GET.get('email')
    #     email = kwargs.get('email')

    #     print(f"------Get------UserAccountView-------- {email}")

    #     if email:
    #         return render(request, 'user_management/otp_verification.html', {'email': email})
    #     else:
    #         return HttpResponse("Email not found in query parameters", status=400)

    def post(self, request, *args, **kwargs):  # email,otp
        # print(f"-----------------post---------------------UserAccountView--------")

        # raw_user_data = request.POST
        raw_user_data = request.data

        try:
            instance = OtpVerification.objects.get(
                email=raw_user_data['email'])
            if instance.otp == raw_user_data['otp']:
                instance = CustomUser.objects.model(
                    email=instance.email,
                    password=instance.password,
                    username=instance.username
                )
                instance.save()
                author_group = Group.objects.get(name='Author')
                instance.groups.add(author_group)
                message = 'You have signed up to ipsita'
                send_email(instance.email, message)
                return Response("Account Created", status=status.HTTP_200_OK)
            else:
                return Response("Otp didn't match", status=status.HTTP_400_BAD_REQUEST)

        except OtpVerification.DoesNotExist:
            return Response("Otp verification is not complete", status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request):  # email,password
        token = get_token_from_request(request)
        raw_user_data = request.data

        if token is None:
            return Response('Invalid token', status=status.HTTP_401_UNAUTHORIZED)
        try:
            user = Token.objects.get(key=token).user
            # print(f"---------------user 1---------------{user}")
        except Token.DoesNotExist:
            return Response('Invalid Token', status=status.HTTP_401_UNAUTHORIZED)

        try:
            CustomUser.objects.get(email=raw_user_data['email'])
            return Response('User already exists', status=status.HTTP_400_BAD_REQUEST)
        except:
            serializer = CustomUserModelSerializer(
                instance=user, data=raw_user_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response('Login info updated', status=status.HTTP_200_OK)


class UserView(APIView):
    # Add Bearer token authentication
    # authentication_classes = [TokenAuthentication,]
    # permission_classes = [IsAuthenticated,]

    def get(self, request):  # token
        """get the user by token"""
        token = get_token_from_request(request)
        # print(f"-------------------GET-----------User------------{token}")
        # print(
        #     f'-----UserView-----{request.data}----{request.META["HTTP_AUTHORIZATION"]}')

        if token is None:
            return Response('Invalid token', status=status.HTTP_401_UNAUTHORIZED)
        try:
            user = Token.objects.get(key=token).user
            # print(f"---------------user 1---------------{user}")
        except Token.DoesNotExist:
            return Response('Invalid Token', status=status.HTTP_401_UNAUTHORIZED)

        # user_data = {
        #     'email': user.email,
        #     'username': user.username
        # }
        serializer = CustomUserModelSerializer(user)
        # print(
        #     f"--------------------------{user.username}----------------")
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)


class CreateTokenAPIView(APIView):
    """create and get token on user login"""

    # def get(self, request):
    #     print(f"---------------GET--------CreateTokenView------------")
    #     return render(request, 'user_management/login.html')

    def post(self, request, *args, **kwargs):  # email,password
        # print(
        #     f"---------------POST--------CreateTokenView------------{request.data}")

        serializer = AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        # ********************************************************************************
        current_user = user
        Token.objects.filter(user=user).delete()

        # Create a new token
        token = Token.objects.create(user=user)
        print(f"token--------------{token}")
        request.session['token'] = token.key
        return Response({'token': token.key}, status=status.HTTP_200_OK)


# class CreateArticleAPIView(APIView):
#     # def get(self, request, *args, **kwargs):
#     #     print('-------------------Article--------Get----')
#     #     form = ArticleForm()
#     #     return render(request, 'user_management/post.html', {'form': form})

#     def post(self, request, *args, **kwargs):
#         token = request.headers.get('Authorization', '').replace('Bearer ', '')

#         # print(
#         #     f'-----Article--------Post=================={token}')
#         # print(
#         #     f'-----Article========post================{request.META.get("HTTP_AUTHORIZATION","")}')
#         form = ArticleForm(request.POST)
#         """get the user by token"""
#         token = get_token_from_request(request)
#         # print(
#         #     f"-------------------Article GET-----------token------------{token}")

#         if token is None:
#             # return Response('Invalid token', status=status.HTTP_401_UNAUTHORIZED)
#             # return render(request, 'user_management/post.html', {'form': form})
#             return Response('Invalid token', status=status.HTTP_401_UNAUTHORIZED)

#         try:
#             user = Token.objects.get(key=token).user
#             # print(f"---------------Article user---------------{user}")
#         except Token.DoesNotExist:
#             # return Response('Invalid Token', status=status.HTTP_401_UNAUTHORIZED)
#             # return render(request, 'user_management/post.html', {'form': form})
#             return Response('Invalid token', status=status.HTTP_401_UNAUTHORIZED)

#         if form.is_valid:
#             article = form.save(commit=False)
#             # print(f'------------article------{article}-----------------')
#             article.author = user  # Set the author to the currently logged-in user
#             article.save()
#             return Response('Article Posted', status=status.HTTP_200_OK)
#         else:
#             # return Response("no success", status=status.HTTP_400_BAD_REQUEST)
#             # form = ArticleForm()
#             # return render(request, 'user_management/post.html', {'form': form})
#             return Response("There was a problem posting the article", status=status.HTTP_400_BAD_REQUEST)

#             # return render(request, 'user_management/post.html', {'form': form})
#             # return redirect('home')
