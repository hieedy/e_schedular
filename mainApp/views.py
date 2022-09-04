import email

from django.shortcuts import render, redirect
from mainApp import admin, models as msmodel
from django.http import HttpResponse
import requests
import json
import http
from datetime import date, datetime, timedelta


# Create your views here.

def index_page(request):
    return render(request,'index.html')

def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            #check if credentials are valid or not
            admin_user = msmodel.AdminUser.objects.get(email_id = email , password = password)
            request.session['email_id'] = admin_user.email_id
            request.session['Name'] = admin_user.first_name+" "+admin_user.last_name
            request.session['id'] = admin_user.id

            return redirect(dashboard)

        except msmodel.AdminUser.DoesNotExist:
            return HttpResponse('You are not registered.')
        
        #redirect to home
    return render(request, 'loginPage.html')






    return render(request,'index.html')



def verifyEmail(email_address):
    # email_address = "foo@bar.com"
    response = requests.get(
        "https://isitarealemail.com/api/email/validate",
        params = {'email': email_address})

    status = response.json()['status']
    return status == "valid"




def registeration_page(request):

    if request.method == "POST":
        first_name = request.POST.get('first_name').strip()
        last_name =  request.POST.get('last_name').strip()
        email_id = request.POST.get('emailid').strip()
        password = request.POST.get('password').strip()
        gender = request.POST.get('gender').strip()


        # print(first_name, last_name, email_id, password, gender)
        if msmodel.AdminUser.objects.filter(email_id = email_id).exists():
            return HttpResponse('</h1> This Email is already registered </h1> >')
        else:
            
            #it shud be gmail id 
            split_email_id = email_id.split("@")

            if split_email_id[1] == "gmail.com":


                isVerified = verifyEmail(email_id)

                if isVerified:

                    admin_user = msmodel.AdminUser()
                    admin_user.first_name = first_name
                    admin_user.last_name = last_name
                    admin_user.email_id = email_id
                    admin_user.password = password
                    admin_user.gender = gender

                    admin_user.save()

                    return HttpResponse("<h1> User Account is Succesfully Registered </h1>")
                else:
                    return HttpResponse("<h1> Email Doesnot Exist. Please Enter Valid Gmail ID </h1>")
            else:
                return HttpResponse("<h1> Only Gmail ID can be filled </h1>")




    return render(request,'signUp.html')

def show_myevents(request):
    return render(request,'index.html')

def dashboard(request):
    if request.session.get('id'):
        data = {}
        events = msmodel.Event.objects.filter(user_id = request.session.get('id'))
        #get count of days choosen

        for event in events:
            calendar_entry = len(msmodel.CalendarDate.objects.filter(Event_id = event))

            time_slots = len(msmodel.AvailableSlote.objects.filter(calendardates_id__in = msmodel.CalendarDate.objects.filter(Event_id = event) ))

            data[event] = [calendar_entry,time_slots]
        

        print(data)

        return render(request, "dashboard.html" , {"events":events, "data":data})

    
    return render(request, "loginPage.html")

def create_myevent(request):

    time_values = []
    start_time = datetime(year=2022,month = 5,  day=5,hour=0,minute=0,second=0)
    end_time = datetime(year=2022,month = 5, day=5,hour=23, minute=59,second=59)

    while start_time<end_time:
        # print(start_time.strftime("%H:%M:%S"))
        time_values.append(start_time.strftime("%H:%M:%S")+"-"+ (start_time+timedelta(minutes=30)).strftime("%H:%M:%S"))
        start_time += timedelta(minutes=30)
        




    if request.method == 'POST':
        calendar_dates = request.POST.get('calendar_dates')
        timeslots = request.POST.getlist('timeslots')
        agenda = request.POST.get('meetingName')


        #split dates 
        cal_split_dates = calendar_dates.split(", ")

        print(cal_split_dates)
        print(timeslots)

        #create event 
        event  = msmodel.Event()
        event.event_created_date = date.today()
        event.user_id = msmodel.AdminUser.objects.get(id = request.session.get('id'))
        event.unique_link = "dummy.com"
        event.event_agenda = agenda

        event.save()

        event.unique_link = "http://localhost:8000/bookmeeting/?event_id="+str(event.id)
        event.save()

        print(event.unique_link)



        for cal_date in cal_split_dates:
            calendar_entry = msmodel.CalendarDate()
            calendar_entry.Event_id = event

            date_parts = cal_date.split("-")

            year = int(date_parts[0])
            month = int(date_parts[1])
            day = int(date_parts[2])

            calendar_entry.date = date(year,month,day)
            
            calendar_entry.save()

            for timeslot in timeslots:
                available_slote_entry = msmodel.AvailableSlote()
                available_slote_entry.calendardates_id = calendar_entry

                time_split = time_values[int(timeslot)].split("-")

                start_time = datetime.strptime(time_split[0],"%H:%M:%S")
                end_time = datetime.strptime(time_split[1],"%H:%M:%S")

                print(start_time,end_time)

                available_slote_entry.start_time = start_time
                available_slote_entry.end_time = end_time

                available_slote_entry.status = False
                available_slote_entry.zoomlink = "dummy.com"

                available_slote_entry.save()
        

        print("DONE")
        return render(request, 'createNewLink.html', {'time_values':time_values , "isPosted": True})




    #     print(calendar_dates)
    #     print(timeslots)
    #     print(agenda)

    return render(request, 'createNewLink.html', {'time_values':time_values})











    # presentday = datetime.now() # or presentday = datetime.today()
  

    # # Get Tomorrow
    # tomorrow = presentday + timedelta(1)
  
  
# strftime() is to format date according to
# the need by converting them to string
    # try:
    #     generate_demo_zoom_link(tomorrow.strftime("%Y-%m-%d"), tomorrow.strftime("%H:%M:%S"))
    #     print("DONE")
    # except Exception:
    #     print("Somethign is wrong")

    # return render(request,'index.html')

def show_accountdetails(request):
    return render(request,'index.html')



def generate_demo_zoom_link(start_date, start_time):

    start_time_string = start_date+"T"+start_time+"Z"
    conn = http.client.HTTPSConnection("api.zoom.us")
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IkRYdlloUkdOUlFtR2Vra2xYV2NVM3ciLCJleHAiOjE5MjQ4ODU4MDAsImlhdCI6MTYwNjQ5NTczNn0.l1rT102hxUPebTEAp0yICKcsZ-mTKReTpv-gchrKz9Q"
    headers = {
        'authorization': "Bearer "+token,
        'content-type': "application/json",

    }

    data = {

        "agenda": "Testing",  # Agenda
        "type": "2",  # scheduled meeeting with fixed time
        "start_time": start_time_string,
        "duration": "30",  # meeting duration 90 minutes
        "schedule_for": "",
        "timezone": "Asia/Calcutta",
        "password": "123",  # password for entering in the meeting
        "agenda": "Class",  # agenda of python class

        "settings": {
            "host_video": "True",
            "participant_video": "True",
            "cn_meeting": "False",
            "in_meeting": "True",
            "join_before_host": "True",
            "mute_upon_entry": "True",
            "watermark": "True",
            "use_pmi": "False",
            "approval_type": "1",  # manually aprrove the meeting
            # attendees register once and can attend any of the occurences
            "registration_type": "1",
            "audio": "both",
            "auto_recording": "none",  # audio recording not available
            "enforce_login": "False",
            "enforce_login_domains": "",
            "alternative_hosts": "",
            "global_dial_in_countries": [
                ""
            ],
            "registrants_email_notification": "True",
            "show_share_button": "True",
        }
    }

    conn.request("POST", "/v2/users/-uL10fmYRLWy0P0rBJ0ctg/meetings",
                 headers=headers, body=json.dumps(data))
    # conn.request("GET", "/v2/users", headers = headers)

    res_bytes = (conn.getresponse()).read()
    res_dict = json.loads(res_bytes.decode('utf-8'))

    try:
        print(res_dict.get("id"))
        print(res_dict.get("start_url"))
        print(res_dict.get("join_url"))
        print("zoom link created")
        return (res_dict.get("id"), res_dict.get("start_url"), res_dict.get("join_url"))
    except Exception:
        print("There is some error please contact to the developer")
    # my id "id":"-uL10fmYRLWy0P0rBJ0ctg"