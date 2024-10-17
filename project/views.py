from django.shortcuts import render, get_object_or_404, redirect
from event.models import *
from booking.models import *
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .import views

def index(request):
    index_events = Event.objects.all()
    return render(request, 'frontend/pages/index.html',{'events':index_events})

def viewDetails(request, id):
    single_event = Event.objects.get(id=id)
    tickets = Ticket.objects.filter(event=single_event)
    
    context = {
        'event':single_event,
        'tickets':tickets
    }
    return render(request, 'frontend/pages/event_detail.html', context)

#login_required
def buyTicket(request, id, ticket_id):
    event = get_object_or_404(Event, pk=id)
    ticket= get_object_or_404(Ticket, pk=ticket_id)
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            quantity = int(request.POST['quantity'])
            total_amount = ticket.price * quantity
            full_name = request.POST['full_name']
    
            booking = Booking(
            user=request.user,
            full_name=full_name,
            event=event,
            ticket=ticket,
            quantity=quantity,
            total_amount=total_amount,
            payment_status='unpaid'
            )
            booking.save()
            return redirect(reverse('payment', args=[booking.id]))
        else:
            return redirect('/login')
    return render(request, 'frontend/pages/buy_ticket.html', {'event':event, 'ticket':ticket})


def payment(request, id):
    booking = Booking.objects.get(pk=id)
    return render(request, 'frontend/pages/khalti_payment.html',{'booking':booking})

def paymentWithKhalti(request, id):
    booking = get_object_or_404(Booking, pk=id)
    booking.payment_status = 'paid'
    booking.save()
    messages.info(request,'Payment Successful')
    return redirect('/')
       
def userLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user= User.objects.filter(email=email).first()
        print(user.username)
        loggedinuser =authenticate(request,username=user.username, password=password)
        if loggedinuser:
            login(request, loggedinuser)
            return redirect('/')
        else:
            return render(request,{'error': 'Invalid credentials'})    
    return render(request, 'auth/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if User.objects.filter(username=username).exists():
            return render(request, 'auth/register.html', {'error': 'Username already exists'})
        if User.objects.filter(email=email).exists():
            return render(request, 'auth/register.html', {'error': 'Email already exists'})
       
        if password == confirm_password:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return redirect('/login')
        else:
            return render(request, 'auth/register.html', {'error':'password did not match'})
    return render(request, 'auth/register.html')

def bookingSuccess(request):
    return render(request, 'frontend/pages/booking_success.html')


def events(request):
    return render(request, 'frontend/pages/events.html')

def about(request):
    return render(request, 'frontend/pages/about.html')

def contact(request):
    return render(request, 'frontend/pages/contact.html')