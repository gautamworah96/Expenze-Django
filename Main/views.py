from __future__ import print_function
import argparse
from googleapiclient.discovery import build
from httplib2 import Http

from oauth2client import file, client, tools
import webbrowser
from chartit.templatetags import chartit
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.template import loader,RequestContext
from chartit import DataPool,Chart
from django.db.models.query import RawQuerySet
from django.db import connection
import simplejson
import json
from django.db.models import F,Sum,Q,aggregates, Count

from googleapiclient.discovery import build
from httplib2 import Http
import time
import argparse
import django.core.urlresolvers
from oauth2client.client import flow_from_clientsecrets
import oauth2client
from oauth2client import file, client, tools
import webbrowser
from chartit.templatetags import chartit
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response,HttpResponseRedirect
from django.template import loader,RequestContext
from chartit import DataPool,Chart
import simplejson
import json,os
#from Main import client_secrets.json
from django.db.models import Aggregate
import argparse,httplib2
from oauth2client.tools import run_flow

# Create your views here.


from Main.forms import UserForm
from Main.models import Expense, LoanPremium,Balance, UserDetails,User

CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), '..', 'client_secrets.json')
REDIRECT_URI = 'http://127.0.0.1:8000/Main/addloanpremium/'


def index(request):
    return render_to_response('Main/intro.html', locals(), context_instance=RequestContext(request))

def loginpage(request):
    return render_to_response('Main/login.html', locals(), context_instance=RequestContext(request))

def login_user(request):
    #if not request.user.is_authenticated():
    context =RequestContext(request)
    if request.method == "POST":
            username = request.POST.get('inputEmail')
            password = request.POST.get('inputPassword')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    expenses = Expense.objects.filter(user=request.user).order_by('-date_created')
                    balances =Balance.objects.filter(user=request.user)
                    return render(request, 'Main/home_page.html',{'expenses':expenses[0:10],'balances':balances})
                else:
                    return render(request,'Main/login.html',{'error_message':'Your account has been disabled'})
            else:
                return render(request,'Main/login.html',{'error_message':'Invalid login'})
    else:
        return render(request,'Main/login.html')




def register_user(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
       # user = authenticate(username=username, password=password)
        #if user is not None:
           # if user.is_active:
                #login(request, user)
               # owners = Owner.objects.filter(user=request.user)
        return render(request, 'Main/login.html',{})
    context = {
        "form": form,
    }
    return render(request,'Main/signup.html', context)

def exp_form(request):
    return render(request, 'Main/exp_form.html',None)

def home_page(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date_created')
    balances = Balance.objects.filter(user=request.user)

    return render(request, 'Main/home_page.html',{'expenses':expenses[0:10],'balances':balances})

def save(request):

    return render(request, 'Main/home_page.html', {})

def log_out(request):
    logout(request)
    return render(request,'Main/login.html')

def showtransactions(request):
    if request.method == 'POST':
        x = request.POST['date_in']
        y = request.POST['date_out']
        expenses = Expense.objects.filter(user=request.user).filter(date_created__range=[x,y])
        return render(request, 'Main/transactions.html', {'expenses': expenses})
    else:
        expenses=Expense.objects.filter(user=request.user).order_by('-date_created')
        return render(request,'Main/transactions.html',{'expenses':expenses})





def addexpense(request):
    if request.method == 'POST':
        expenses = Expense()

        user = request.user
        expenses.user = user

        expenses.paid_to = request.POST['expname']
        expenses.source = request.POST['cardtypexp']
        expenses.option = request.POST['types']
        expenses.cost = request.POST['amount']
        expenses.date_created = request.POST['expdate']
        expenses.bill = request.POST['attachment_file_display']
        expenses.tax_details = request.POST['carddet']
        expenses.vat = request.POST['carddet']
        expenses.ext_ref = request.POST['carddet']
        expenses.description = request.POST['carddet']
        expenses.bill = request.FILES['attachment_file']
        expenses.subcategories = request.POST['sub']
        expenses.is_recurrent = request.POST['is_recurrent']
        if expenses.is_recurrent == True:
            expenses.rec_date = request.POST['expdate']
            #expenses.rec_day = request.POST['rec_day']
            #expenses.rec_month = request.POST['rec_month']
            #expenses.rec_year = request.POST['rec_year']
        expenses.save()
        if (request.POST.get("is_recurrent") == "True"):
            print(" \n \n entered iscalendar =tru \n")

            print(" \n \n entered calendar now trying to add event \n \n")
            SCOPES = 'https://www.googleapis.com/auth/calendar'

            # flow = oauth2client.client.flow_from_clientsecrets('C:/Users/ghw/Desktop/ExpenzeGautam/Main/client_secrets.json',SCOPES,redirect_uri='http://127.0.0.1:8000/Main/addloanpremium/')

            # storage = oauth2client.file.Storage('credentials.dat')
            # credentials = storage.get()


            # auth_uri = flow.step1_get_authorize_url()
            # print("\n value of auth uri is "+auth_uri+"\n")
            # return HttpResponseRedirect(auth_uri)
            # print("\ncame back from redirect\n")
            # print("\n\n printing code66"+code66+"\n\n")
            # time.sleep(10)
            # current_url = request.resolver_match.url_name
            # current_url2=request.get_full_path()
            # print(" \n \n printing cureent url2  "+current_url2+"\n\n")
            # print(" \n \n printing cureent url  "+current_url+"\n\n")
            # creds12=flow.step2_exchange(auth_uri)
            # print("\n value of creds is "+creds12+"\n")
            # auth_code = request.GET.get('code')
            # print("\n value of auth code is "+auth_code+"\n")
            # credentials = flow.step2_exchange(auth_code)

            # storage.put(credentials)




            # http = httplib2.Http()
            # http = credentials.authorize(http)


            flow = flow_from_clientsecrets('D:\client_secrets.json', scope=SCOPES)
            storage = oauth2client.file.Storage('credentials.dat')
            # credentials = storage.get()
            http = httplib2.Http()
            flags = tools.argparser.parse_args(args=[])
            credentials = tools.run_flow(flow, storage, flags)
            # credentials = run(flow, storage, http=http)
            http = credentials.authorize(http)
            CAL = build('calendar', 'v3', http=http)

            # ((int(request.GET.get('rate')))/100)

            print("\n  calendar was built successfully \n \n")
            GMT_OFF = '+05:30'  # PDT/MST/GMT-7
            EVENT = {
                'summary': 'Expense : ' + request.POST.get('expname') + ' Amount to be paid is ' +request.POST.get('amount') ,
                'start': {'date': request.POST.get('expdate')},
                'end': {'date': request.POST.get('expdate')},
                'recurrence': ['RRULE:FREQ=' + request.POST.get('etype')],
            }

            e = CAL.events().insert(calendarId='primary',
                                    sendNotifications=True, body=EVENT).execute()
            print("\n \n event successfuly added \n \n")
            url = 'www.google.com/calendar'
            webbrowser.open_new(url)

    return render(request,'Main/exp_form.html',{})

def delete(request,ex_id):

    expenses=Expense.objects.filter(user=request.user).get(pk=ex_id)
    balance=Balance.objects.filter(user=request.user).get(user_id=request.user.id)
    x = expenses.cost
    if expenses.option=='Expense':
         balance.expense -=x
    else:
        balance.income -= x
    balance.save()
    expenses.delete()
    return redirect('Main:home_page')






def getExpense(request):
    def my_custom_sql(self):

        cursor = connection.cursor()
        cursor.execute("""SELECT SUM(cost) from Main_expense WHERE "option"='Expense' GROUP BY date_created""")
        result = cursor.fetchall()
        return result

 # Step 1: Create a DataPool with the data we want to retrieve.

    weatherdata = \
            DataPool(
                series=
                [{'options': {
                    'source': Expense.objects.all().filter(option__exact='Expense')},
                    'terms': [
                        {'expense': Sum('cost')},
                        {'date_expense': 'date_created'},
                    ]},
                    {'options': {
                        'source':Expense.objects.all().filter(option__exact='Income')},
                        'terms': [
                            {'income': Sum('cost')},
                            {'date_income': 'date_created'},
                        ]}
                ])

        # Step 2: Create the Chart object
    cht = Chart(
            datasource=weatherdata,
            series_options=
            [{'options': {
                'type': 'column',
                'stacking': False},
                'terms':{
              'date_expense': [
                'expense',
                ],
              'date_income': [
                'income']
                }}],
            chart_options=
            {'title': {
                'text': 'Income Vs Expenditure'},
                'xAxis': {
                    'title': {
                        'text': 'Date Created'}}})

        # Step 3: Send the chart object to the template.
    return render(request,'Main/chart.html',{'cht':cht})


def gcalender(request):
    try:
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None

    SCOPES = 'https://www.googleapis.com/auth/calendar'
    store = file.Storage('storage2.json')
    # creds = store.get()
    # if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secrets.json', SCOPES)
    creds = tools.run_flow(flow, store, flags) \
        if flags else tools.run_flow(flow, store)
    CAL = build('calendar', 'v3', http=creds.authorize(Http()))

    GMT_OFF = '+05:30'  # PDT/MST/GMT-7
    EVENT = {
        'summary': 'Dinner with friends okkk',
        'start': {'dateTime': '2016-09-01T:00:00%s' % GMT_OFF},
        'end': {'dateTime': '2016-09-02T23:15:00%s' % GMT_OFF},

    }

    e = CAL.events().insert(calendarId='primary',
                            sendNotifications=True, body=EVENT).execute()

    url = 'www.google.com/calendar'
    webbrowser.open_new(url)

    print('''*** %r event added:
        Start: %s
        End:   %s''' % (e['summary'].encode('utf-8'),
                        e['start']['dateTime'], e['end']['dateTime']))


def addloanpremium(request):
    if request.method == 'GET':

       # premium = LoanPremium()
        user = request.user
        # form=loan_pre_form(request.POST)


        if (request.GET.get('typelp') == 'loan'):
            loan = LoanPremium()
            loan.user = user

            # premium.user=user
            print("\n \n entered loan now saving data \n \n")
            loan.loan_premium_name = request.GET.get('lpname')
            loan.loan_premium_amountamount = request.GET.get('lpamount')
            loan.start_date = request.GET.get('sdate')
            loan.end_date = request.GET.get('edate')
            loan.rate_of_interest = request.GET.get('rate')
            ##rtype is for  monthly yearly daily
            loan.type_duration = request.GET.get('rtype')
            amt = (int(request.GET.get('lpamount'))) * (
            (1 + ((int(request.GET.get('rate'))) / 100)) * (int(request.GET.get('years'))))
            amt = amt / 12
            amt = int(amt)
            loan.save()
            dateString=''
            dateString=request.GET.get('edate')
            dates = dateString[0:4] + dateString[5:7] + dateString[8:10]
            print(" \n \n saved all data \n \n")
            # loan.no_of_years=request.POST['nyears']

            if (request.GET.get("iscalender") == "True"):
                print(" \n \n entered iscalendar =tru \n")

                print(" \n \n entered calendar now trying to add event \n \n")
                SCOPES = 'https://www.googleapis.com/auth/calendar'
                flow = flow_from_clientsecrets('D:\client_secrets.json',scope=SCOPES)
                storage = oauth2client.file.Storage('credentials.dat')
                # credentials = storage.get()
                http = httplib2.Http()
                flags = tools.argparser.parse_args(args=[])
                credentials = tools.run_flow(flow, storage, flags)
                # credentials = run(flow, storage, http=http)
                http = credentials.authorize(http)
                CAL = build('calendar', 'v3', http=http)

                # ((int(request.GET.get('rate')))/100)

                print("\n  calendar was built successfully \n \n")
                GMT_OFF = '+05:30'  # PDT/MST/GMT-7
                EVENT = {
                    'summary': 'Loan due to be paid: ' + request.GET.get('lpname') + ' Amount to be paid is ' + str(
                        amt),
                    'start': {'date': request.GET.get('sdate')},
                    'end': {'date': request.GET.get('sdate')},
                    'recurrence': ['RRULE:FREQ=' + request.GET.get('rtype')+';UNTIL='+dates+'T170000Z',],
                }

                e = CAL.events().insert(calendarId='primary',
                                        sendNotifications=True, body=EVENT).execute()
                print("\n \n event successfuly added \n \n")
                url = 'www.google.com/calendar'
                webbrowser.open_new(url)


        else:
            # loan.user=user
            premium = LoanPremium()
            user = request.user
            premium.user = user
            premium.loan_premium_name = request.GET.get('lpname')
            premium.loan_premium_amount = request.GET.get('lpamount')
            premium.start_date = request.GET.get('sdate')
            premium.end_date = request.GET.get('edate')
            # loan.rate_of_interest=request.POST['rate']
            premium.type_duration = request.GET.get('rtype')
            # print (" \n\n "+request.GET.get('lpamount')+"\n\n")
             #amt=(int(request.GET.get('lpamount')))/12
            # amt=int(amt)
            premium.save()
            dateString=''
            dateString = request.GET.get('edate')
            #dates = dateString[0:4] + dateString[5:7] + dateString[8:10]
            print("data was saved premium \n")
            # loan.loan_name=request.POST['lname']
            # loan.no_of_years=request.POST['nyears']
            if (request.GET.get("iscalender") == "True"):
                SCOPES = 'https://www.googleapis.com/auth/calendar'
                flow = flow_from_clientsecrets("D:\client_secrets.json", scope=SCOPES)
                storage = oauth2client.file.Storage('credentials.dat')
                # credentials = storage.get()
                http = httplib2.Http()
                flags = tools.argparser.parse_args(args=[])
                credentials = tools.run_flow(flow, storage, flags)
                # credentials = run(flow, storage, http=http)
                http = credentials.authorize(http)
                CAL = build('calendar', 'v3', http=http)
                dates = dateString[0:4] + dateString[5:7] + dateString[8:10]

                print("\n  calendar was built successfully \n \n")
                GMT_OFF = '+05:30'  # PDT/MST/GMT-7
                EVENT = {
                    'summary': 'Premium due to be paid: ' + request.GET.get(
                        'lpname') + ' Amount to be paid is Rs ' +request.GET.get('lpamount') ,
                    'start': {'date': request.GET.get('sdate')},
                    'end': {'date': request.GET.get('sdate')},
                    'recurrence': ['RRULE:FREQ=' + request.GET.get('rtype')+';UNTIL='+dates+'T170000Z'],
                }

                e = CAL.events().insert(calendarId='primary',
                                        sendNotifications=True, body=EVENT).execute()
                print("\n \n event successfuly added \n \n")
                url = 'www.google.com/calendar'
                webbrowser.open_new(url)

        return render_to_response('Main/loan_pre_form.html', {})


def editprofile(request):
   # if request.method=='POST':
   userdetails = UserDetails.objects.filter(user=request.user)
   return render(request,'Main/editprofile.html',{'userdetails':userdetails})

def profile(request):
    userdetails = UserDetails.objects.filter(user=request.user)

    return render(request,'Main/profile.html', {'userdetails':userdetails})
