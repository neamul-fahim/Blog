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
from django.contrib.auth import get_user_model

from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from rest_framework import generics
from django.conf import settings
User = get_user_model()


class LoginView(View):
    # def get(self, request):
    #     return render(request, 'user_management/signup.html')

    def get(self, request):
        context = {
        }
        # print(f"---------------GET--------CreateTokenView------------")
        return render(request, 'user_management/login.html', context)


class SignupView(View):
    def get(self, request):
        context = {
        }
        # print("-----------------SighupView")
        return render(request, 'user_management/signup.html', context)


class OTPView(View):
    def get(self, request, *args, **kwargs):
        # print(f"-------------------Get------------------UserAccountView--------")
        email = request.GET.get('email')

        if email:
            context = {
                'email': email,
            }
            return render(request, 'user_management/otp_verification.html', context)
        else:
            return HttpResponse("Email not found in query parameters", status=400)


class HomeView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'user_management/home_page.html', context)


class UserProfileView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'user_management/user_profile.html', context)


class BlockedUsersPage(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'user_management/blocked_users_page.html', context)


class ModeratorUsersPage(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'user_management/moderator_page.html', context)


class UserProfileAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        print(user)
        user = {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'is_moderator': user.groups.filter(name='Moderator').exists(),
            'is_superuser': user.is_superuser,
        }
        print(user)

        return Response({'user': user})


class AllUserProfileAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.is_superuser:
            return Response('Unauthoried', status=status.HTTP_401_UNAUTHORIZED)

        users = CustomUser.objects.all()
        user_data = []

        for user in users:
            user_info = {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'is_moderator': user.groups.filter(name='Moderator').exists(),
                'is_superuser': user.is_superuser,
            }
            user_data.append(user_info)

        return Response({'users': user_data}, status=status.HTTP_200_OK)


class SignupAPIView(APIView):

    def post(self, request, *args, **kwargs):  # username,email,password
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


# class UserView(APIView):

#     def get(self, request):  # token
#         """get the user by token"""
#         token = get_token_from_request(request)

#         if token is None:
#             return Response('Invalid token', status=status.HTTP_401_UNAUTHORIZED)
#         try:
#             user = Token.objects.get(key=token).user
#         except Token.DoesNotExist:
#             return Response('Invalid Token', status=status.HTTP_401_UNAUTHORIZED)
#         serializer = CustomUserModelSerializer(user)

#         return Response({"user": serializer.data}, status=status.HTTP_200_OK)


class CreateTokenAPIView(APIView):
    """create and get token on user login"""

    def post(self, request, *args, **kwargs):  # email,password
        serializer = AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        current_user = user
        Token.objects.filter(user=user).delete()

        # Create a new token
        token = Token.objects.create(user=user)
        print(f"token--------------{token}")
        request.session['token'] = token.key
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class BlockedUsersAPIView(APIView):
    def get(self, request):
        try:
            # Get the 'Moderator' group
            moderator_group = Group.objects.get(name='Author')

            # Filter users who are not in the 'Moderator' group
            non_moderator_users = User.objects.exclude(groups=moderator_group)

            # Serialize the users or extract relevant data
            user_data = [{'id': user.id, 'username': user.username,
                          'email': user.email} for user in non_moderator_users if not user.is_superuser]

            return Response({'users': user_data}, status=status.HTTP_200_OK)

        except Group.DoesNotExist:
            return Response({'error': 'Moderator group not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UnblockUserAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            # Check if the authenticated user is in the 'Moderator' group
            if not request.user.has_perm('article.unban_author'):
                return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

            # Retrieve the user to be unblocked
            user_to_unblock = CustomUser.objects.get(id=user_id)

            # Add the user to the 'Author' group
            author_group, created = Group.objects.get_or_create(name='Author')
            user_to_unblock.groups.add(author_group)

            return Response({'message': 'User unblocked and added to Author group'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ToggleModeratorAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            # Get the user model
            # Retrieve the user
            user = CustomUser.objects.get(id=user_id)

            # Toggle moderator status
            if user.groups.filter(name='Moderator').exists():
                user.groups.remove(Group.objects.get(name='Moderator'))
                message = f'{user.username} removed from Moderator group'
            else:
                user.groups.add(Group.objects.get(name='Moderator'))
                message = f'{user.username} added to Moderator group'

            return Response({'message': message})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
