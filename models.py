from django.db import models
from django.contrib.auth.models import User

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

class PMSProject(models.Model):
    '''
    DB Class to handle all the Project related information.
    '''
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=1000, blank=True, null=True)
    client_poc = models.CharField(max_length=1000, blank=False, null=False)
    client_poc_email = models.EmailField(max_length=1000, blank=False, null=False)
    delivery_owner = models.ForeignKey(DeliveryOwner, on_delete=models.CASCADE)
    project_type = models.ForeignKey(ProjectType, on_delete=models.CASCADE)
    date_booked = models.DateField()
    doc_type = models.ForeignKey(DocType, on_delete=models.CASCADE)
    estimated_date_of_delivery = models.DateField()
    image_count = models.IntegerField(default=0)
    status = models.CharField(max_length=100, blank=False, null=False)
    team = models.CharField(max_length=10000, blank=False, null=False)
    image_count_authored = models.IntegerField(default=0)
    date_delivered = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    title_name = models.CharField(max_length=1000, null=True, blank=True)
    project_complexity = models.CharField(max_length=1000, null=False, blank=False)

class Counter(models.Model):
    '''
    DB Class to handle invoice / PO number tracks for each client for a year.
    '''
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
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
    title_name = models.CharField(max_length=10000, null=False, blank=False)
    project_quote = models.FloatField(default=0.0)
    project_currency = models.CharField(max_length=100, blank=False, null=False)
    expected_invoicing_date = models.DateField()
    po_amount = models.FloatField(default=0.0)
    po_number = models.CharField(max_length=1000, blank=False, null=False)
    date_invoiced = models.DateField(blank=True, null=True)
    amount_invoiced = models.FloatField(default=0.0)
    number_of_days_since_invoiced = models.IntegerField(default=0)
    expected_money_in_date = models.DateField(blank=True, null=True)
    money_in = models.FloatField(default=0.0)
    po_file = models.CharField(max_length=1000)

class UserType(models.Model):
    '''
    DB Class to handle all User Permissions.
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_superadmin = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_assosciate_admin = models.BooleanField(default=False)

class Segregate(models.Model):
    project = models.ForeignKey(PMSProject, on_delete=models.CASCADE)
    title_name = models.CharField(max_length=1000, null=False, blank=False)
    machine_image_count_proposed = models.IntegerField(default=0)
    manual_image_count_proposed = models.IntegerField(default=0)
    machine_image_count_delivered = models.IntegerField(default = 0)
    manual_image_count_delivered = models.IntegerField(default = 0)
    machine_accuracy = models.FloatField(default=0)


