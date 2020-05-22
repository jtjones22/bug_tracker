from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from account.forms import LoginForm, AddTicketForm
from account.models import Ticket, Account
# Create your views here.


@login_required
def index(request):
    item = Ticket.objects.all()
    item = item.order_by('-time')
    new_tickets = item.filter(status='New')
    in_progress_tickets = item.filter(status='In Progress')
    done_tickets = item.filter(status='Done')
    html = 'index.html'
    context = {
        'tickets': item,
        'new_tickets': new_tickets,
        'in_progress_tickets': in_progress_tickets,
        'done_tickets': done_tickets}
    return render(request, html, context)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request,
                username=data['username'],
                password=data['password']
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get('next', reverse('homepage'))
                )
    form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


@login_required
def add_ticket_view(request):
    html = 'add_ticket.html'
    if request.method == 'POST':
        form = AddTicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            item = Ticket.objects.create(
                title=data['title'],
                description=data['description'],
                submitted_by=request.user
            )
            item.save()
            return HttpResponseRedirect(reverse('ticket_detail', args=(item.id,)))
    form = AddTicketForm()
    context = {'form': form}
    return render(request, html, context)


@login_required
def ticket_view(request, item_id):
    html = 'ticket_detail.html'
    item = Ticket.objects.get(id=item_id)
    context = {'item': item}
    return render(request, html, context)


@login_required
def user_view(request, item_id):
    user = Account.objects.get(username=item_id)
    submitted_tickets = Ticket.objects.filter(submitted_by=user)
    assigned_tickets = Ticket.objects.filter(assigned_user=user)
    completed_tickets = Ticket.objects.filter(completed_by=user)

    html = 'user_profile.html'
    context = {
        'user': user,
        'submitted_tickets': submitted_tickets,
        'assigned_tickets': assigned_tickets,
        'completed_tickets': completed_tickets,
        }
    return render(request, html, context)


""" Ticket Views """


@login_required
def edit_ticket_view(request, item_id):
    ticket = Ticket.objects.get(id=item_id)
    html = 'edit_ticket.html'
    if request.user.id != ticket.submitted_by.id:
        if request.method == 'POST':
            form = AddTicketForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                ticket.title = data['title']
                ticket.description = data['description']
                ticket.save()
                return HttpResponseRedirect(reverse('ticket_detail', args=(item_id,)))
        form = AddTicketForm(initial={
            'title': ticket.title,
            'description': ticket.description
        })
        context = {'form': form}
        return render(request, html, context)
    return HttpResponseRedirect(reverse('ticket_detail', args=(item_id,)))


@login_required
def assign_ticket_view(request, item_id):
    ticket = Ticket.objects.get(id=item_id)
    if ticket.submitted_by.id != request.user.id:
        if ticket.status != 'Done' and ticket.status != 'In Progress':
            ticket.status = 'In Progress'
            ticket.assigned_user = request.user
            ticket.save()
            return HttpResponseRedirect(reverse('ticket_detail', args=(item_id,)))
    return HttpResponseRedirect(reverse('ticket_detail', args=(item_id,)))
    

@login_required
def return_ticket_view(request, item_id):
    ticket = Ticket.objects.get(id=item_id)
    if ticket.assigned_user:
        if request.user.id == ticket.assigned_user.id:
            ticket.status = 'New'
            ticket.assigned_user = None
            ticket.save()
            return HttpResponseRedirect(reverse('ticket_detail', args=(item_id,)))
    return HttpResponseRedirect(reverse('ticket_detail', args=(item_id,)))


@login_required
def finished_ticket_view(request, item_id):
    ticket = Ticket.objects.get(id=item_id)
    if ticket.assigned_user:
        if request.user.id == ticket.assigned_user.id:
            ticket.status = 'Done'
            ticket.completed_by = request.user
            ticket.assigned_user = None
            ticket.save()
            return HttpResponseRedirect(reverse('ticket_detail', args=(item_id,)))
    return HttpResponseRedirect(reverse('ticket_detail', args=(item_id,)))


@login_required
def invalid_ticket_view(request, item_id):
    ticket = Ticket.objects.get(id=item_id)
    if ticket.status != 'Done':
        if not ticket.assigned_user and request.user.id != ticket.submitted_by.id:
            ticket.status = 'Invalid'
            ticket.save()
            return HttpResponseRedirect(reverse('homepage'))
    if ticket.assigned_user:
        if request.user.id == ticket.assigned_user.id and ticket.status != 'Done':
            ticket.status = 'Invalid'
            ticket.assigned_user = None
            ticket.completed_by_user = None
            ticket.save()
            return HttpResponseRedirect(reverse('homepage'))
    return HttpResponseRedirect(reverse('ticket_detail', args=(item_id,)))



""" Edge Case Checklist 

signed in user makes ticket and tries 
all url paths (nothing should happen) with no assigned user:
    /ticket/assign_ticket/id [x]
    /ticket/return_ticket/id [x]
    /ticket/invalid_ticket/id [x]
    /ticket/edit_ticket/id [x]
    /ticket/finish_ticket/id [x]
---------------------------------------------------------------
signed in user makes ticket and tries 
all url paths (nothing should happen) with assigned user:
    /ticket/assign_ticket/id [x]
    /ticket/return_ticket/id [x]
    /ticket/invalid_ticket/id [x]
    /ticket/edit_ticket/id [x]
    /ticket/finish_ticket/id [x]

user tries all paths with no assigned user (Nothing should happen):
    /ticket/return_ticket/id [x]
    /ticket/finish_ticket/id [x]

assigned user to the ticket tries url paths (should do nothing):
    /ticket/assign_ticket/id [x]

unassigned user tries all paths on a ticket with another assigned user(nothing should happen):

"""