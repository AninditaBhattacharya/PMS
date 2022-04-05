from ast import expr_context
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

class CreateProject(APIView):
    '''
    POST Method to create a Project.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        post_param = request.data
        client_code = post_param['client_code']
        client_objects = Client.objects.filter(client_code = client_code)
        if len(client_objects):
            client_object = client_objects[0]
            project_name = post_param['project_name']
            client_poc = post_param['client_poc']
            client_poc_email = post_param['client_poc_email']
            delivery_owner_email = post_param['delivery_owner_email']
            delivery_owner_objects = DeliveryOwner.objects.filter(email = delivery_owner_email)
            if len(delivery_owner_objects):
                delivery_owner_object = delivery_owner_objects[0]
                project_type_is_alttext = post_param['project_type_is_alttext']
                project_type_is_remediation = post_param['project_type_is_remediation']
                project_type_object = ProjectType()
                project_type_object.is_alttext = project_type_is_alttext
                project_type_object.is_remediation = project_type_is_remediation
                project_type_object.save()
                date_booked = post_param['date_booked']
                doc_type_docx = post_param['doc_type_docx']
                doc_type_pdf = post_param['doc_type_pdf']
                doc_type_pptx = post_param['doc_type_pptx']
                doc_type_xlsx = post_param['doc_type_xlsx']
                doc_type_object = DocType()
                doc_type_object.docx = doc_type_docx
                doc_type_object.pdf = doc_type_pdf
                doc_type_object.pptx = doc_type_pptx
                doc_type_object.xlsx = doc_type_xlsx
                doc_type_object.save()
                estimated_date_of_delivery = post_param['estimated_date_of_delivery']
                image_count = post_param['image_count']
                status_project = post_param['status']
                team = post_param['team']
                image_count_authored = post_param['image_count_authored']
                date_delivered = post_param['date_delivered']
                user_object = request.user
                project_object = Project()
                project_object.client = client_object
                project_object.project_name = project_name
                project_object.client_poc = client_poc
                project_object.client_poc_email = client_poc_email
                project_object.delivery_owner = delivery_owner_object
                project_object.project_type = project_type_object
                project_object.date_booked = date_booked
                project_object.doc_type = doc_type_object
                project_object.estimated_date_of_delivery = estimated_date_of_delivery
                project_object.image_count = image_count
                project_object.status = status_project
                project_object.team = team
                project_object.image_count_authored = image_count_authored
                project_object.date_delivered = date_delivered
                project_object.created_by = user_object
                project_object.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response({"error" : "No such Delivery Owner exists."}, status = status.HTTP_417_EXPECTATION_FAILED)
        else:
            return Response({"error" : "No such Client Code exists."}, status=status.HTTP_417_EXPECTATION_FAILED)

class UpdateProject(APIView):
    '''
    POST Method to update details of a project.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        post_param = request.data
        project_id = post_param['project_id']
        project_object = Project.objects.get(pk = project_id)
        try:
            client_code = post_param['client_code']
            client_object = Client.objects.get(client_code = client_code)
            project_object.client = client_object
        except:
            pass
        try:
            project_name = post_param['project_name']
            project_object.project_name = project_name
        except:
            pass
        try:
            client_poc = post_param['client_poc']
            project_object.client_poc = client_poc
        except:
            pass
        try:
            client_poc_email = post_param['client_poc_email']
            project_object.client_poc_email = client_poc_email
        except:
            pass
        try:
            delivery_owner_email = post_param['delivery_owner_email']
            delivery_owner_object = DeliveryOwner.objects.get(email = delivery_owner_email)
            project_object.delivery_owner = delivery_owner_object
        except:
            pass
        try:
            project_type_is_alttext = post_param['project_type_isalttext']
            project_type_is_remediation = post_param['project_type_is_remediation']
            project_type_object = project_object.project_type
            project_type_object.is_alttext = project_type_is_alttext
            project_type_is_remediation = project_type_is_remediation
            project_type_object.save()
        except:
            pass
        try:
            date_booked = post_param['date_booked']
            project_object.date_booked = date_booked
        except:
            pass
        try:
            doc_type_docx = post_param['doc_type_docx']
            doc_type_pdf = post_param['doc_type_pdf']
            doc_type_pptx = post_param['doc_type_pptx']
            doc_type_xlsx = post_param['doc_type_xlsx']
            doc_type_object = project_object.doc_type
            doc_type_object.docx = doc_type_docx
            doc_type_object.pdf = doc_type_pdf
            doc_type_object.pptx = doc_type_pptx
            doc_type_object.xlsx = doc_type_xlsx
            doc_type_object.save()
        except:
            pass
        try:
            estimated_date_of_delivery = post_param['estimated_date_of_delivery']
            project_object.estimated_date_of_delivery = estimated_date_of_delivery
        except:
            pass
        try:
            image_count = post_param['image_count']
            project_object.image_count = image_count
        except:
            pass
        try:
            status_project = post_param['status']
            project_object.status = status_project
        except:
            pass
        try:
            team = post_param['team']
            project_object.team = team
        except:
            pass
        try:
            image_count_authored = post_param['image_count_authored']
            project_object.image_count_authored = image_count_authored
        except:
            pass
        try:
            date_delivered = post_param['date_delivered']
            project_object.date_delivered = date_delivered
        except:
            pass
        project_object.save()
        return Response(status=status.HTTP_200_OK)

class DeleteProject(APIView):
    '''
    POST Method to delete a project.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        post_param = request.data
        project_id = post_param['project_id']
        project_object_instances = Project.objects.filter(pk = project_id)
        if len(project_object_instances):
            project_object_instance = project_object_instances[0]
            project_object_instance.delete()
            return Response(status = status.HTTP_200_OK)
        else:
            return Response({"error" : "No project exists for given ID."}, status=status.HTTP_417_EXPECTATION_FAILED)

class ReadProjects(APIView):
    '''
    GET Method to read all projects.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        project_objects = Project.objects.all()
        response_object = []
        for project_object in project_objects:
            response_object.append(
                {
                    "project_id" : project_object.id,
                    "project_name" : project_object.project_name,
                    "client_code" : project_object.client.client_code,
                    "client_poc" : project_object.client_poc,
                    "client_poc_email" : project_object.client_poc_email,
                    "delivery_owner_email" : project_object.delivery_owner.email,
                    "project_type_is_alttext" : project_object.project_type.is_alttext,
                    "project_object_is_remediation" : project_object.project_type.is_remediation,
                    "date_booked" : project_object.date_booked,
                    "doc_type_docx" : project_object.doc_type.docx,
                    "doc_type_pdf" : project_object.doc_type.pdf,
                    "doc_type_pptx" : project_object.doc_type.pptx,
                    "doc_type_xlsx" : project_object.doc_type.xlsx,
                    "estimated_date_of_delivery" : project_object.estimated_date_of_delivery,
                    "image_count" : project_object.image_count, 
                    "status" : project_object.status,
                    "team" : project_object.team,
                    "image_count_authored" : project_object.image_count_authored,
                    "date_delivered" : project_object.date_delivered,
                    "created_by" : project_object.user.email
                }
            )
        return Response({"result" : response_object}, status=status.HTTP_200_OK)

