from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField


class Client(models.Model):
    '''
    DB Class to handle all Client information.
    '''
    client_name = models.CharField(max_length=1000, blank=False, null=False)
    client_code = models.CharField(max_length=100, blank=False, null=False)

class DeliveryOwner(models.Model):
    '''
    DB Class to handle all the delivery owner's information.
    '''
    name = models.CharField(max_length=1000, blank=False, null=False)
    email = models.EmailField(max_length=1000, blank=False, null=False)

class ProjectType(models.Model):
    '''
    DB Class to handle Project Type information.
    '''
    is_alttext = models.BooleanField(default=False)
    is_remediation = models.BooleanField(default = False)

class DocType(models.Model):
    '''
    DB Class to handle document types information.
    '''
    docx = models.BooleanField(default = False)
    pdf = models.BooleanField(default = False)
    pptx = models.BooleanField(default = False)
    xlsx = models.BooleanField(default = False)

class Discipline(models.Model):
    '''
    DB Class to handle all the disciplines.
    '''
    discipline_name = models.CharField(max_length=100, blank=False, null=False)
    discipline_code = models.CharField(max_length=100, blank=False, null=False)

class ClientOrganization(models.Model):
    client_organization_name = models.CharField(max_length=1000, null=False, blank=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

class Storing_Invoice(models.Model):
    Project_Number=models.ForeignKey(PMSProject,on_delete=models.CASCADE, null=True)
    Invoice_File=models.URLField(max_length=500)
    Invoice_Number=models.CharField(max_length=1000, blank=True, null=True)

class PMSProject(models.Model):
    '''
    DB Class to handle all the Project related information.
    '''
    parent_project_name = models.CharField(max_length=1000, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    project_name = models.CharField(max_length=1000, blank=True, null=True)
    client_poc = models.CharField(max_length=1000, blank=True, null=True)
    client_poc_email = models.EmailField(max_length=1000, blank=True, null=True)
    delivery_owner = models.ForeignKey(DeliveryOwner, on_delete=models.CASCADE, null=True)
    project_type = models.ForeignKey(ProjectType, on_delete=models.CASCADE, null=True)
    date_booked = models.DateField()
    doc_type = models.ForeignKey(DocType, on_delete=models.CASCADE,null=True)
    #doc_type = models.CharField(max_length=100, blank=False, null=False)
    estimated_date_of_delivery = JSONField(blank=True, null=True)
    image_count = models.IntegerField(default=0)
    status = models.CharField(max_length=100, blank=True, null=True)
    team = JSONField(blank=True, null=True)
    image_count_authored = models.IntegerField(default=0)
    date_delivered = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, null=True)
    title_name = models.CharField(max_length=1000, null=True, blank=True)
    project_complexity = models.CharField(max_length=1000, null=True, blank=True)
    client_organization = models.ForeignKey(ClientOrganization, on_delete=models.CASCADE, null=True)

class Counter(models.Model):
    '''
    DB Class to handle invoice / PO number tracks for each client for a year.
    '''
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    year = models.IntegerField(blank=False, null=False)
    counter = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CAS.CADE,null=True)

class InvoiceCounter(models.Model):
    '''
    DB Class to handle invoice / PO number tracks for each client for a year.
    '''
    project = models.ForeignKey(PMSProject, on_delete=models.CASCADE, null=True)
    counter = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)

class TrackingCounter(models.Model):
    '''
    DB Class to handle invoice / PO number tracks for each client for a year.
    '''
    year = models.IntegerField(blank=False, null=False)
    counter = models.IntegerField(default=0)

class DayCountTracker(models.Model):
    '''
    DB Class to handle Daily count trackers.
    '''
    project = models.ForeignKey(PMSProject, on_delete=models.CASCADE)
    image_count = models.IntegerField(default=0)
    image_count_authored = models.IntegerField(default=0)
    #email
    #date

class BufferImages(models.Model):
    '''
    DB Class to handle Buffer / Extra Images for a Project.
    '''
    parent_project = models.ForeignKey(PMSProject, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=100, blank=False, null=False)
    client_poc = models.CharField(max_length=1000, blank=False, null=False)
    client_poc_email = models.EmailField(max_length=1000, blank=False, null=False)
    delivery_owner = models.ForeignKey(DeliveryOwner, on_delete=models.CASCADE)
    project_type = models.ForeignKey(ProjectType, on_delete=models.CASCADE)
    date_booked = models.DateField()
    doc_type = models.ForeignKey(DocType, on_delete=models.CASCADE)
    estimated_date_of_delivery = models.DateField()
    image_count = models.IntegerField(default=0)
    status = models.CharField(max_length=100, blank=False, null=False)
    team = models.CharField(max_length=100, blank=False, null=False)
    image_count_authored = models.IntegerField(default=0)
    date_delivered = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class Finance(models.Model):
    '''
    DB Class to handle all the Project Finances.
    '''
    project = models.ForeignKey(PMSProject, on_delete=models.CASCADE)
    title_name = models.CharField(max_length=10000, null=True, blank=True)
    project_quote = models.FloatField(default=0.0)
    project_currency = models.CharField(max_length=100, blank=True, null=True)
    expected_invoicing_date = models.DateField(blank=True, null=True)
    po_amount = models.FloatField(default=0.0)
    po_number = models.CharField(max_length=1000, blank=True, null=True)
    date_invoiced = models.DateField(blank=True, null=True)
    amount_invoiced = models.FloatField(default=0.0)
    number_of_days_since_invoiced = models.IntegerField(default=0)
    expected_money_in_date = models.DateField(blank=True, null=True)
    money_in = models.FloatField(default=0.0)
    po_file = models.CharField(max_length=1000, blank=True, null=True)

class UserType(models.Model):
    '''
    DB Class to handle all User Permissions.
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_superadmin = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_assosciate_admin = models.BooleanField(default=False)
    contact_number = models.CharField(max_length=12, blank=True, null=True)
    discipline_expertise = models.TextField(blank=True, null=True)
    work_expertise = models.TextField(blank=True, null=True)
    employee_type = models.TextField(blank=True, null=True)
    disp_expertise = models.ForeignKey(Discipline, on_delete=models.CASCADE, null=True)

class Segregate(models.Model):
    project = models.ForeignKey(PMSProject, on_delete=models.CASCADE)
    title_name = models.CharField(max_length=1000, null=False, blank=False)
    machine_image_count_proposed = models.IntegerField(default=0)
    manual_image_count_proposed = models.IntegerField(default=0)
    machine_image_count_delivered = models.IntegerField(default = 0)
    manual_image_count_delivered = models.IntegerField(default = 0)
    machine_accuracy = models.FloatField(default=0)

class DailyImageTracker(models.Model):
    project = models.ForeignKey(PMSProject, on_delete=models.CASCADE)
    title_name = models.CharField(max_length=1000, null=False, blank=False)
    expected_count = models.IntegerField(default=0)
    delivered_count = models.IntegerField(default=0)
    delivery_info = JSONField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    estimated_hours = models.IntegerField(default=0)
    worked_hours = models.IntegerField(default=0)
    work_type = models.CharField(max_length=1000, blank=False, null=False)
    employee_type = models.CharField(max_length=1000, blank=False, null=False)
    team_member = models.CharField(max_length=1000, blank=False, null=False)
    status = models.CharField(max_length=1000, blank=False, null=False)
    delivery_owner = models.ForeignKey(DeliveryOwner, on_delete=models.CASCADE, null=True)
    image_type = models.CharField(max_length=1000, blank=False, null=True)
    team_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class TeamMember(models.Model):
    email = models.EmailField(max_length = 254)
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)

class SaveInvoide(models.Model):
    Project_name=models.CharField(max_length=70)
    Invoice_Number=models.CharField(max_length=70)
    Invoice_File=models.CharField(max_length=70)

class POInvoice(models.Model):
    input_file_link = models.CharField(max_length=1000, blank=False, null=False)
    output_file_link = models.CharField(max_length=1000, blank=False, null=False)
    created_at = models.DateField(auto_now=True)
