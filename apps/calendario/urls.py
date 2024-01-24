# -*- encoding: utf-8 -*-
from django.urls import path, re_path

from apps.calendario import views

app_name = 'calendario'


urlpatterns = [
    path('calendarios/', views.CalendarView.as_view(), name='calendarios'),
    path('calendario/', views.CalendarViewNew.as_view(), name='calendario'),

    path('eventos/', views.AllEventsListView.as_view(), name='eventos'),
    path('evento/<int:event_id>/', views.event_details, name='evento'),
    path('evento/nuevo/', views.create_event, name='evento_add'),
    path('evento/editar/<int:pk>/', views.EventEdit.as_view(), name='evento_upd'),
    path('evento/eliminar/<int:event_id>/', views.delete_event, name='evento_del'),



    
    path('next_week/<int:event_id>/', views.next_week, name='next_week'),
    path('next_day/<int:event_id>/', views.next_day, name='next_day'),
    path('add_eventmember/<int:event_id>', views.add_eventmember, name='add_eventmember'),
    path('event/<int:pk>/remove',views.EventMemberDeleteView.as_view(),name='remove_event'),
    path('running-event-list/',views.RunningEventsListView.as_view(),name='running_events'),
]
