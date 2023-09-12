from django.contrib.auth import authenticate, login

from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
                                   HTTP_500_INTERNAL_SERVER_ERROR)
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from user.api.serializers import (UserCreateSerializer, UserDetailSerializer,
                                  UserLoginSerializer,
                                  UserStatusUpdateSerializer,
                                  UserUpdateSerializer)
from user.models import User
from user.api.permissions import IsUserOrReadOnly


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'list':
            return UserDetailSerializer
        if self.action == 'retrieve':
            return UserDetailSerializer
        if self.action == 'create':
            return UserCreateSerializer
        if self.action == 'update':
            return UserUpdateSerializer
        if self.action == 'partial_update':
            return UserUpdateSerializer
        return UserDetailSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [IsAdminUser()]
        if self.action == 'retrieve':
            return [IsAuthenticated()]
        if self.action == 'create':
            return [AllowAny()]
        if self.action == 'partial_update':
            return [IsUserOrReadOnly()]
        if self.action == 'update':
            return [IsUserOrReadOnly()]
        if self.action == 'destroy':
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            serializer = self.serializer_class(user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserUpdateStatus(RetrieveUpdateAPIView):
    serializer_class = UserStatusUpdateSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]

    def perform_update(self, serializer):
        serializer.save()


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response(
                {'message': 'Successfully logged out.'},
                status=HTTP_200_OK)
        except Exception as error:
            return Response(
                {'error': str(error)},
                status=HTTP_500_INTERNAL_SERVER_ERROR)

