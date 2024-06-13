
from django.template import loader
from django.http import HttpResponse
from listen.models import SpeedInstance
from django.utils import timezone

import plotly.express as px
import plotly.graph_objects as go

import os
import json
import requests

# Create your views here.

def generate_tables():
    # format all speed info into values and cells to make table
    sorted_speeds = SpeedInstance.objects.order_by("-true_date")
    speeds, dates, ids, text = zip(*[(float(s.speed), format_date(str(s.recorded_at)), s.id, str(s.custom_text)) for s in sorted_speeds])

    fig = go.Figure(data=[go.Table(header=dict(values=['Instance ID', 'Speed', 'Time Recorded', 'Custom Text']),
                 cells=dict(values=[ids, speeds, dates, text]))
                     ])
    fig.write_html('listen/templates/listen/recent_instances.html', full_html=False, include_plotlyjs='cdn')

    return

def index(request):
    # Make sure the table resource exists when accessed
    if not os.path.exists("listen/recent_instances.html"):
        generate_tables()

    template = loader.get_template("listen/index.html")
    
    context = {"custom_title": "speeding is cool"}
    return HttpResponse(template.render(context, request))

def ping(request):
    return HttpResponse("Hello, World!")

def save(request):
    if request.method == "POST":
        try:
            s = SpeedInstance(  true_date=timezone.now(),
                                recorded_at=format_date(str(timezone.now())),
                                speed=request.headers["captured-speed"],
                                direction=request.headers["direction"],
                                custom_text=request.headers["custom-text"])
            # Save it to the table
            s.save()
            # Update the table
            generate_tables()
        
            
            return HttpResponse("SpeedInstance has been sucessfully acknowledged and saved.")
        except:
            return HttpResponse("There has been an error processing your request")
    else: 
        return HttpResponse("Please use POST")
    
def format_date(recorded_at: str):
    '''Use this to quickly format the DateTimeFields to readable strings
    To Be Implemented'''
    recorded_at = recorded_at.split(" ")
    recorded_at[1] = ":".join(recorded_at[1].split(":")[:2])
    
    if (int(recorded_at[1][:(recorded_at[1].index(":"))])>=12):
        recorded_at[1] = str(int(recorded_at[1][:(recorded_at[1].index(":"))])-16) + recorded_at[1][2:]
    
    recorded_at = f"{recorded_at[0]} {recorded_at[1]}"
    return recorded_at