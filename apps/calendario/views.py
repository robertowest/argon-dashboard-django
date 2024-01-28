import calendar

from datetime import timedelta, datetime, date

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.safestring import mark_safe
from django.views import generic

from apps.calendario.models import EventMember, Event
from apps.calendario.utils import Calendar
from apps.calendario.forms import EventForm, AddMemberForm


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month


class CalendarView(LoginRequiredMixin, generic.ListView):
    model = Event
    template_name = "calendario/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)
        return context


@login_required(login_url="signup")
def event_details(request, event_id):
    event = Event.objects.get(id=event_id)
    eventmember = EventMember.objects.filter(event=event)
    context = {"event": event, "eventmember": eventmember}
    return render(request, "event-details.html", context)



# class CalendarViewNew(LoginRequiredMixin, generic.View):
#     template_name = "calendario/index.html"
#     form_class = EventForm

#     def get(self, request, *args, **kwargs):
#         forms = self.form_class()
#         events = Event.objects.get_all_events(user=request.user)
#         events_month = Event.objects.get_running_events(user=request.user)
#         event_list = []
#         # start: '2020-09-16T16:00:00'
#         for event in events:
#             event_list.append(
#                 {   "id": event.id,
#                     "title": event.title,
#                     "start": event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
#                     "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
#                     "description": event.description,
#                 }
#             )
#         context = {"form": forms, "events": event_list, "events_month": events_month}
#         return render(request, self.template_name, context)

#     def post(self, request, *args, **kwargs):
#         forms = self.form_class(request.POST)
#         if forms.is_valid():
#             form = forms.save(commit=False)
#             form.user = request.user
#             form.save()
#             return redirect("calendario:calendar")
#         context = {"form": forms}
#         return render(request, self.template_name, context)



# class AllEventsListView(generic.ListView):
#     template_name = "calendario/eventos.html"
#     model = Event

#     def get_queryset(self):
#         return Event.objects.get_all_events(user=self.request.user)


# class RunningEventsListView(generic.ListView):
#     template_name = "calendario/eventos.html"
#     model = Event

#     def get_queryset(self):
#         return Event.objects.get_running_events(user=self.request.user)
    





# @login_required(login_url="signup")
# def create_event(request):
#     form = EventForm(request.POST or None)
#     if request.POST and form.is_valid():
#         title = form.cleaned_data["title"]
#         description = form.cleaned_data["description"]
#         start_time = form.cleaned_data["start_time"]
#         end_time = form.cleaned_data["end_time"]
#         Event.objects.get_or_create(
#             user=request.user,
#             title=title,
#             description=description,
#             start_time=start_time,
#             end_time=end_time,
#         )
#         return HttpResponseRedirect(reverse("calendario:calendar"))
#     return render(request, "event.html", {"form": form})


# class EventEdit(generic.UpdateView):
#     model = Event
#     fields = ["title", "description", "start_time", "end_time"]
#     template_name = "calendario/evento.html"



# def add_eventmember(request, event_id):
#     forms = AddMemberForm()
#     if request.method == "POST":
#         forms = AddMemberForm(request.POST)
#         if forms.is_valid():
#             member = EventMember.objects.filter(event=event_id)
#             event = Event.objects.get(id=event_id)
#             if member.count() <= 9:
#                 user = forms.cleaned_data["user"]
#                 EventMember.objects.create(event=event, user=user)
#                 return redirect("calendario:calendar")
#             else:
#                 print("--------------User limit exceed!-----------------")
#     context = {"form": forms}
#     return render(request, "add_member.html", context)


# class EventMemberDeleteView(generic.DeleteView):
#     model = EventMember
#     template_name = "event_delete.html"
#     success_url = reverse_lazy("calendario:calendar")


# def delete_event(request, event_id):
#     event = get_object_or_404(Event, id=event_id)
#     if request.method == 'POST':
#         event.delete()
#         return JsonResponse({'message': 'Event sucess delete.'})
#     else:
#         return JsonResponse({'message': 'Error!'}, status=400)


# def next_week(request, event_id):
#     event = get_object_or_404(Event, id=event_id)
#     if request.method == 'POST':
#         next = event
#         next.id = None
#         next.start_time += timedelta(days=7)
#         next.end_time += timedelta(days=7)
#         next.save()
#         return JsonResponse({'message': 'Sucess!'})
#     else:
#         return JsonResponse({'message': 'Error!'}, status=400)


# def next_day(request, event_id):
#     event = get_object_or_404(Event, id=event_id)
#     if request.method == 'POST':
#         next = event
#         next.id = None
#         next.start_time += timedelta(days=1)
#         next.end_time += timedelta(days=1)
#         next.save()
#         return JsonResponse({'message': 'Sucess!'})
#     else:
#         return JsonResponse({'message': 'Error!'}, status=400)
    