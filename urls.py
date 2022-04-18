from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    url(r'^create_pms_user/', views.CreateUserPMS.as_view()),
    url(r'^create_project/', views.CreateProject.as_view()),
    url(r'^update_project/', views.UpdateProject.as_view()),
    url(r'^read_projects/', views.ReadProjects.as_view()),
    url(r'^delete_project/', views.DeleteProject.as_view()),
    url(r'^create_client/', views.CreateClient.as_view()),
    url(r'^update_client/', views.UpdateClient.as_view()),
    url(r'^read_clients/', views.ReadClients.as_view()),
    url(r'^delete_client/', views.DeleteClient.as_view()),
    url(r'^create_delivery_owner/', views.CreateDeliveryOwner.as_view()),
    url(r'^update_delivery_owner/', views.UpdateDeliveryOwner.as_view()),
    url(r'^read_delivery_owners/', views.ReadDeliveryOwners.as_view()),
    url(r'^delete_delivery_owner/', views.DeleteDeliveryOwner.as_view()),
    url(r'^create_discipline/', views.CreateDiscipline.as_view()),
    url(r'^update_discipline/', views.UpdateDiscipline.as_view()),
    url(r'^read_disciplines/', views.ReadDisciplines.as_view()),
    url(r'^delete_discipline/', views.DeleteDiscipline.as_view()),
    url(r'^create_counter/', views.CreateCounter.as_view()),
    url(r'^update_counter/', views.UpdateCounter.as_view()),
    url(r'^read_counters/', views.ReadCounters.as_view()),
    url(r'^delete_counter/', views.DeleteCounter.as_view()),
    url(r'^create_day_count_tracker/', views.CreateDayCountTracker.as_view()),
    url(r'^update_day_count_tracker/', views.UpdateDayCountTracker.as_view()),
    url(r'^read_day_count_trackers/', views.ReadDayCountTrackers.as_view()),
    url(r'^delete_day_count_tracker/', views.DeleteDayCountTracker.as_view()),
    url(r'^create_buffer_images/', views.CreateBufferImages.as_view()),
    url(r'^update_buffer_images/', views.UpdateBufferImage.as_view()),
    url(r'^read_buffer_images/', views.ReadBufferImages.as_view()),
    url(r'^delete_buffer_images/', views.DeleteBufferImages.as_view()),
    url(r'^create_finance/', views.CreateFinance.as_view()),
    url(r'^update_finance/', views.UpdateFinance.as_view()),
    url(r'^read_finances/', views.ReadFinances.as_view()),
    url(r'^delete_finance/', views.DeleteFinance.as_view()),
    url(r'^projects_dropdown/', views.ReadPMSProjectsDropdown.as_view()),
]