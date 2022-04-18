from ast import expr_context
from curses.ascii import US
from pydoc import cli
from sys import api_version
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from accounts.serializers import UserSerializer
from accounts.views import create_userprofile
from pms.models import PMSProject, Discipline, DeliveryOwner, Counter, ProjectType, DayCountTracker, Client, DocType, BufferImages, Finance, UserType
from datetime import datetime
from dateutil import parser as datetime_parser

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
                date_booked = datetime_parser.parse(post_param['date_booked'])
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
                estimated_date_of_delivery = datetime_parser.parse(post_param['estimated_date_of_delivery'])
                image_count = post_param['image_count']
                status_project = post_param['status']
                team = post_param['team']
                image_count_authored = post_param['image_count_authored']
                date_delivered = datetime_parser.parse(post_param['date_delivered'])
                user_object = request.user
                project_object = PMSProject()
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
                project_object.discipline = post_param['discipline']
                project_name.project_complexity = post_param['project_complexity']
                project_object.title_name = post_param['title_name']
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
        project_object = PMSProject.objects.get(pk = project_id)
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
        try:
            project_object.project_complexity = post_param['project_complexity']
        except:
            pass
        try:
            project_object.title_name = post_param['title_name']
        except:
            pass
        try:
            project_object.discipline = post_param['discipline']
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
        project_object_instances = PMSProject.objects.filter(pk = project_id)
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
        project_objects = PMSProject.objects.all()
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
                    "created_by" : project_object.created_by.email,
                    "discipline" : project_object.discipline,
                    "title_name" : project_object.title_name,
                    "project_complexity" : project_object.project_complexity
                }
            )
        return Response({"result" : response_object}, status=status.HTTP_200_OK)

class CreateClient(APIView):
    '''
    POST Method to create a client.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        post_param = request.data
        client_name = post_param['client_name']
        client_code = post_param['client_code']
        client_object = Client()
        client_object.client_name = client_name
        client_object.client_code = client_code
        client_object.save()
        return Response(status=status.HTTP_200_OK)

class ReadClients(APIView):
    '''
    GET Method to get all clients.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        response_object = []
        client_objects = Client.objects.all()
        for client_object in client_objects:
            response_object.append(
                {
                    "client_id" : client_object.id,
                    "client_name" : client_object.client_name, 
                    "client_code" : client_object.client_code
                }
            )
        return Response({"result" : response_object}, status = status.HTTP_200_OK)

class UpdateClient(APIView):
    '''
    POST Method to update a client information.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        post_param = request.data
        client_id = post_param['client_id']
        client_objects = Client.objects.filter(pk = client_id)
        if len(client_objects):
            client_object = client_objects[0]
            try:
                client_object.client_name = post_param['client_name']
            except:
                pass
            try:
                client_object.client_code = post_param['client_code']
            except:
                pass
            client_object.save()
            return Response(sttaus = status.HTTP_200_OK)
        else:
            return Response({"error" : "No Client exists for given client ID."}, status = status.HTTP_417_EXPECTATION_FAILED)

class DeleteClient(APIView):
    '''
    POST Method to delete a client.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        post_param = request.data
        client_id = post_param['client_id']
        client_object_instance = Client.objects.get(pk = client_id)
        client_object_instance.delete()
        return Response(status = status.HTTP_200_OK)

class CreateDeliveryOwner(APIView):
    '''
    POST Method to create a Delivery Owner.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        post_param = request.data
        name = post_param['name']
        email = post_param['email']
        delivery_owner_object = DeliveryOwner()
        delivery_owner_object.name = name
        delivery_owner_object.email = email
        delivery_owner_object.save()
        return Response(status = status.HTTP_200_OK)

class ReadDeliveryOwners(APIView):
    '''
    GET Method to read all Delivery Owners. 
    '''
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        delivery_owner_objects = DeliveryOwner.objects.all()
        response_object = []
        for delivery_owner_object in delivery_owner_objects:
            response_object.append(
                {
                    "delivery_owner_id" : delivery_owner_object.id,
                    "name" : delivery_owner_object.name,
                    "email" : delivery_owner_object.email
                }
            )
        return Response({"result" : response_object}, status = status.HTTP_200_OK)

class UpdateDeliveryOwner(APIView):
    '''
    POST Method to update a delivery owner.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        post_param = request.data
        delivery_owner_id = post_param['delivery_owner_id']
        delivery_owner_objects = DeliveryOwner.objects.filter(pk = delivery_owner_id)
        if len(delivery_owner_objects):
            delivery_owner_object = delivery_owner_objects[0]
            try:
                delivery_owner_object.name = post_param['name']
            except:
                pass
            try:
                delivery_owner_object.email = post_param['email']
            except:
                pass
            delivery_owner_object.save()
            return Response(status = status.HTTP_200_OK)
        else:
            return Response({"error" : "No such delivery owner object exist."}, status = status.HTTP_417_EXPECTATION_FAILED)

class DeleteDeliveryOwner(APIView):
    '''
    POST Method to delete a delivery owner.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        post_param = request.data
        delivery_owner_id = post_param['delivery_owner_id']
        delivery_owner_object_instance = DeliveryOwner.objects.get(pk = delivery_owner_id)
        delivery_owner_object_instance.delete()
        return Response(status = status.HTTP_200_OK)

class CreateDiscipline(APIView):
    '''
    POST Method to create a Discipline.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        post_param = request.data
        discipline_object = Discipline()
        discipline_object.discipline_name = post_param['discipline_name']
        discipline_object.discipline_code = post_param['discipline_code']
        discipline_object.save()
        return Response(status = status.HTTP_200_OK)

class ReadDisciplines(APIView):
    '''
    GET Method to read all disciplines.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        response_object = []
        discipline_objects = Discipline.objects.all()
        for discipline_object in discipline_objects:
            response_object.append(
                {
                    "discipline_id" : discipline_object.id,
                    "discipline_name" : discipline_object.discipline_name,
                    "discipline_code" : discipline_object.discipline_code
                }
            )
        return Response({"result" : response_object}, status = status.HTTP_200_OK)

class UpdateDiscipline(APIView):
    '''
    POST Method to update a discipline.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        post_param = request.data
        discipline_id = post_param['discipline_id']
        discipline_objects = Discipline.objects.filter(pk = discipline_id)
        if len(discipline_objects):
            discipline_object = discipline_objects[0]
            try:
                discipline_object.discipline_name = post_param['discipline_name']
            except:
                pass
            try:
                discipline_object.discipline_code = post_param['discipline_code']
            except:
                pass
            discipline_object.save()
            return Response(status = status.HTTP_200_OK)
        else:
            return Response({"error" : "No such discipline found."}, status = status.HTTP_417_EXPECTATION_FAILED)

class DeleteDiscipline(APIView):
    '''
    POST Method to delete a discipline.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        post_param = request.data
        discipline_id = post_param['discipline_id']
        discipline_object_instance = Discipline.objects.get(pk = discipline_id)
        discipline_object_instance.delete()
        return Response(status = status.HTTP_200_OK)

class CreateCounter(APIView):
    '''
    POST Method to create a Counter.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        post_param = request.data
        client_code = post_param['client_code']
        client_objects = Client.objects.filter(client_code = client_code)
        if len(client_objects):
            client_object = client_objects[0]
            discipline_code = post_param['discipline_code']
            discipline_objects = Discipline.objects.filter(discipline_code = discipline_code)
            if len(discipline_objects):
                discipline_object = discipline_objects[0]
                year = datetime.date.today().year
                counter = post_param['counter']
                counter_object = Counter()
                counter_object.client = client_object
                counter_object.discipline = discipline_object
                counter_object.year = year
                counter_object.counter = counter
                counter_object.save()
                return Response(status = status.HTTP_200_OK)
            else:
                return Response({"error" : "No such discipline exists for given code."}, status = status.HTTP_417_EXPECTATION_FAILED)
        else:
            return Response({"error" : "No such client exists for given Client code."}, status = status.HTTP_417_EXPECTATION_FAILED)
    
class ReadCounters(APIView):
    '''
    GET Method to read all counter objects.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        response_object = []
        counter_objects = Counter.objects.all()
        for counter_object in counter_objects:
            response_object.append(
                {
                    "counter_id" : counter_object.id,
                    "client_code" : counter_object.client.client_code,
                    "discipline_code" : counter_object.discipline.discipline_code,
                    "year" : counter_object.year,
                    "counter" : counter_object.counter
                }
            )
        return Response({"result" : response_object}, status = status.HTTP_200_OK)

class UpdateCounter(APIView):
    '''
    POST Method to update a counter object.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        post_param = request.data
        counter_id = post_param['counter_id']
        counter_object = Counter.objects.get(pk = counter_id)
        try:
            client_code = post_param['client_code']
            client_object = Client.objects.get(client_code = client_code)
            counter_object.client = client_object
        except:
            pass
        try:
            discipline_code = post_param['discipline_code']
            discipline_object = Discipline.objects.get(discipline_code = discipline_code)
            counter_object.discipline = discipline_object
        except:
            pass
        try:
            counter_object.year = post_param['year']
        except:
            pass
        try:
            counter_object.counter = post_param['counter']
        except:
            pass
        counter_object.save()
        return Response(status = status.HTTP_200_OK)

class DeleteCounter(APIView):
    '''
    POST Method to delete a counter object.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        post_param = request.data
        counter_id = post_param['counter_id']
        counter_object_instance = Counter.objects.get(pk = counter_id)
        counter_object_instance.delete()
        return Response(status = status.HTTP_200_OK)

class CreateDayCountTracker(APIView):
    '''
    POST Method to create a Day Count Tracker.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        post_param = request.data
        project_id = post_param['project_id']
        project_objects = PMSProject.objects.filter(pk = project_id)
        if len(project_objects):
            project_object = project_objects[0]
            image_count = post_param['image_count']
            image_count_authored = post_param['image_count_authored']
            day_count_tacker_object = DayCountTracker()
            day_count_tacker_object.project = project_object
            day_count_tacker_object.image_count = image_count
            day_count_tacker_object.image_count_authored = image_count_authored
            day_count_tacker_object.save()
            return Response(status = status.HTTP_200_OK)
        else:
            return Response({"error" : "No such project found for give ID."}, status = status.HTTP_417_EXPECTATION_FAILED)

class ReadDayCountTrackers(APIView):
    '''
    GET Method to read all Day Count Trackers objects.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        response_object = []
        day_count_tacker_objects = DayCountTracker.objects.all()
        for day_count_tacker_object in day_count_tacker_objects:
            response_object.append(
                {
                    "day_count_tracker_id" : day_count_tacker_object.id,
                    "project_id" : day_count_tacker_object.project.id,
                    "image_count" : day_count_tacker_object.image_count,
                    "image_count_authored" : day_count_tacker_object.image_count_authored
                }
            )
        return Response({"result" : response_object}, status = status.HTTP_200_OK)

class UpdateDayCountTracker(APIView):
    '''
    POST Method to update a Day Count Tracker.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        post_param = request.data
        day_count_tracker_id = post_param['day_count_tracker_id']
        day_count_tracker_objects = DayCountTracker.objects.filter(pk = day_count_tracker_id)
        if len(day_count_tracker_objects):
            day_count_tracker_object = day_count_tracker_objects[0]
            try:
                project_id = post_param['project_id']
                project_object = PMSProject.objects.get(pk = project_id)
                day_count_tracker_object.project = project_object
            except:
                pass
            try:
                day_count_tracker_object.image_count = post_param['image_count']
            except:
                pass
            try:
                day_count_tracker_object.image_count_authored = post_param['image_count_authored']
            except:
                pass
            day_count_tracker_object.save()
            return Response(status = status.HTTP_200_OK)
        else:
            return Response({"error" : "No such day count tracker object exists."}, status = status.HTTP_417_EXPECTATION_FAILED)

class DeleteDayCountTracker(APIView):
    '''
    POST Method to delete a Day Count Tracker.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        post_param = request.data
        day_count_tracker_id = post_param['day_count_tracker_id']
        day_count_tracker_object_instance = DayCountTracker.objects.get(pk = day_count_tracker_id)
        day_count_tracker_object_instance.delete()
        return Response(status = status.HTTP_200_OK)

class CreateBufferImages(APIView):
    '''
    POST Method to create Buffer Images.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        post_param = request.data
        parent_project_id = post_param['parent_project_id']
        parent_project_objects = PMSProject.objects.filter(pk = parent_project_id)
        if len(parent_project_objects):
            parent_project_object = parent_project_objects[0]
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
                    date_booked = datetime_parser.parse(post_param['date_booked'])
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
                    estimated_date_of_delivery = datetime_parser.parse(post_param['estimated_date_of_delivery'])
                    image_count = post_param['image_count']
                    status_project = post_param['status']
                    team = post_param['team']
                    image_count_authored = post_param['image_count_authored']
                    date_delivered = datetime_parser.parse(post_param['date_delivered'])
                    user_object = request.user
                    project_object = BufferImages()
                    project_object.parent_project = parent_project_object
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
        else:
            return Response({"error" : "No such Project exists."}, status = status.HTTP_200_OK)

class UpdateBufferImage(APIView):
    '''
    POST Method to update details of a Buffer Image Object.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        post_param = request.data
        project_id = post_param['buffer_image_id']
        project_object = BufferImages.objects.get(pk = project_id)
        try:
            parent_project_id = post_param['parent_project_id']
            parent_project_object = PMSProject.objects.get(pk = parent_project_id)
            project_object.parent_project = parent_project_object
        except:
            pass
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

class DeleteBufferImages(APIView):
    '''
    POST Method to delete a Buffer Image Object.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        post_param = request.data
        project_id = post_param['buffer_image_id']
        project_object_instances = BufferImages.objects.filter(pk = project_id)
        if len(project_object_instances):
            project_object_instance = project_object_instances[0]
            project_object_instance.delete()
            return Response(status = status.HTTP_200_OK)
        else:
            return Response({"error" : "No buffer image object exists for given ID."}, status=status.HTTP_417_EXPECTATION_FAILED)

class ReadBufferImages(APIView):
    '''
    GET Method to read all Buffer Images objects.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        project_objects = BufferImages.objects.all()
        response_object = []
        for project_object in project_objects:
            response_object.append(
                {
                    "buffer_image_id" : project_object.id,
                    "parent_project_id" : project_object.parent_project.id,
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

class CreateFinance(APIView):
    '''
    POST Method to create Finance for a Project.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        post_param = request.data
        project_id = post_param['project_id']
        project_objects = PMSProject.objects.filter(pk = project_id)
        if len(project_objects):
            project_object = project_objects[0]
            finance_object = Finance()
            finance_object.project = project_object
            finance_object.project_quote = float(post_param['project_quote'])
            finance_object.project_currency = post_param['project_currency']
            finance_object.expected_invoicing_date = datetime_parser.parse(post_param['expected_invoicing_date'])
            finance_object.po_amount = float(post_param['po_amount'])
            finance_object.po_number = post_param['po_number']
            finance_object.date_invoiced = datetime_parser.parse(post_param['date_invoiced'])
            finance_object.amount_invoiced = float(post_param['amount_invoiced'])
            finance_object.number_of_days_since_invoiced = int(post_param['number_of_days_since_invoiced'])
            finance_object.expected_money_in_date = datetime_parser.parse(post_param['expected_money_in_date'])
            finance_object.money_in = float(post_param['money_in'])
            finance_object.save()
            return Response(status = status.HTTP_200_OK)
        else:
            return Response({"error" : "No such project exists."}, status = status.HTTP_417_EXPECTATION_FAILED)

class ReadFinances(APIView):
    '''
    GET Method to read all Finances.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        response_object = []
        finance_objects = Finance.objects.all()
        for finance_object in finance_objects:
            response_object.append(
                {
                    "finance_id" : finance_object.id,
                    "project_id" : finance_object.project.id,
                    "project_quote" : finance_object.project_quote,
                    "project_currency" : finance_object.project_currency,
                    "expected_invoicing_date" : finance_object.expected_invoicing_date,
                    "po_amount" : finance_object.po_amount, 
                    "po_number" : finance_object.po_number,
                    "date_invoiced" : finance_object.date_invoiced,
                    "amount_invoiced" : finance_object.amount_invoiced,
                    "number_of_days_since_invoiced" : finance_object.number_of_days_since_invoiced,
                    "expected_money_in_date" : finance_object.expected_money_in_date,
                    "money_in" : finance_object.money_in
                }
            )
        return Response({"result" : response_object}, status = status.HTTP_200_OK)

class UpdateFinance(APIView):
    '''
    POST Method to update a finance object.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        post_param = request.data
        finance_id = post_param['finance_id']
        finance_objects = Finance.objects.filter(pk = finance_id)
        if len(finance_objects):
            finance_object = finance_objects[0]
            try:
                project_id = post_param['project_id']
                project_object = PMSProject.objects.get(pk = project_id)
                finance_object.project = project_object
            except:
                pass
            try:
                finance_object.project_quote = float(post_param['project_quote'])
            except:
                pass
            try:
                finance_object.project_currency = post_param['project_currency']
            except:
                pass
            try:
                finance_object.expected_invoicing_date = post_param['expected_invoicing_date']
            except:
                pass
            try:
                finance_object.po_amount = float(post_param['po_amount'])
            except:
                pass
            try:
                finance_object.po_number = post_param['po_number']
            except:
                pass
            try:
                finance_object.date_invoiced = post_param['date_invoiced']
            except:
                pass
            try:
                finance_object.amount_invoiced = float(post_param['amount_invoiced'])
            except:
                pass
            try:
                finance_object.number_of_days_since_invoiced = int(post_param['number_of_days_since_invoiced'])
            except:
                pass
            try:
                finance_object.expected_money_in_date = post_param['expected_money_in_date']
            except:
                pass
            try:
                finance_object.money_in = float(post_param['money_in'])
            except:
                pass
            finance_object.save()
            return Response(status = status.HTTP_200_OK)
        else:
            return Response({"error" : "No Finance sheet exists."}, status = status.HTTP_417_EXPECTATION_FAILED)

class DeleteFinance(APIView):
    '''
    POST Method to delete a finance object.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        post_param = request.data
        finance_id = post_param['finance_id']
        finance_objects = Finance.objects.filter(pk = finance_id)
        if len(finance_objects):
            finance_object = finance_objects[0]
            finance_object_instance = finance_object
            finance_object_instance.delete()
            return Response(status = status.HTTP_200_OK)
        else:
            return Response({"error" : "No such finance object exists."}, status = status.HTTP_417_EXPECTATION_FAILED)