from django.shortcuts import render
from .models import Destination, Flights

# Create your views here.
def index(request):

    # dest1= Destination()
    # dest1.name= 'Mumbai'
    # dest1.desc =" The city that doesn't sleep"
    # dest1.img ='destination_1.jpg'
    # dest1.price = 700
    # dest1.offer = False
    #
    #
    # dest2 = Destination()
    # dest2.name = 'Hyderabad'
    # dest2.desc = " 1st Briyani, next Sherwani"
    # dest2.img = 'destination_2.jpg'
    # dest2.price = 600
    # dest2.offer = True
    #
    # dest3 = Destination()
    # dest3.name = 'Bengalure'
    # dest3.desc = " Stride.ai"
    # dest3.img = 'destination_3.jpg'
    # dest3.price = 650
    # dest3.offer =True
    #
    # dests = [dest1,dest2, dest3]

    dests= Destination.objects.all()
    #
    #
    fl= Flights.objects.all()
    #
    return render(request, 'index.html', {'dests': dests, 'fl' : fl})

    #return render(request,'index.html')
