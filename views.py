from curses.ascii import US
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from accounts.serializers import UserSerializer
from accounts.views import create_userprofile
from pms.models import Project, Discipline, DeliveryOwner, Counter, ProjectType, DayCountTracker, Client, DocType, BufferImages, Finance, UserType

class CreateUserPMS(APIView):
    '''
    POST Method to create a PMS User with permissions.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        post_param = request.data
        bool_values = {'true': True, 'false': False}
        if User.objects.filter(username=post_param['email']).exists():
            return Response({"error": "user already exists"},
                    status=status.HTTP_417_EXPECTATION_FAILED)
        user_details = {"username": post_param['email'], "first_name": post_param['first_name'],
            "last_name": post_param['last_name'], "email": post_param['email'], "password": post_param["password"]}
        user = get_user_model().objects.create_user(**user_details)
        org_id = None
        create_userprofile(user, org_id)
        user.save()
        user_serializer = UserSerializer(user, context={'request': request})
        is_super_admin = post_param['is_super_admin']
        is_admin = post_param['is_admin']
        is_assosciate_admin = post_param['is_assosciate_admin']
        user_type_object = UserType()
        user_type_object.user = user
        user_type_object.is_superadmin = is_super_admin
        user_type_object.is_admin = is_admin
        user_type_object.is_assosciate_admin = is_assosciate_admin
        return Response(user_serializer.data, status = status.HTTP_201_CREATED)