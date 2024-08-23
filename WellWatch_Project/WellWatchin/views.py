from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
import matplotlib.pyplot as plt
plt.switch_backend('Agg')
#switches the backend of matplotlib to the "Agg" backend
#which is a non-interactive backend that is commonly used for generating image files without displaying them on the screen.


# Create your views here.

def home(request):
    if request.user.is_anonymous:
        return redirect('/LoginView')
    else:
        
        context={
            'variable':'this is sent'
        }
        return render(request,'home.html',context)


def aboutus(request):
    
    return render(request,'aboutus.html')

def contactus(request):
    
    return render(request,'contactus.html')

def events(request):
    
    return render(request,'events.html')




import mysql.connector
address=''
city=''
state=''
country=''
pcode=0
pno=0
extra=''
feedback=''
@login_required  # Ensure the user is authenticated
def profile(request):
    
    try:
        # Establish a connection to MySQL
        mydb = mysql.connector.connect(host='localhost', user='root', passwd='raghvi@123', database='wellwatchin')
        mycursor = mydb.cursor(dictionary=True)

        # Retrieve user profile data from MySQL based on the logged-in user's email
        query = "SELECT * FROM wellwatchin_signup WHERE username = %s"
        mycursor.execute(query, (request.user.username,))
        user_profile = mycursor.fetchone()

        # Close the database connection
        mycursor.close()
        mydb.close()

        # Render the profile.html template with the user_profile data
        
        global address,city,state,country,pcode,pno,extra,feedback
        if request.method=='POST':
            mydb_post=mysql.connector.connect(host='localhost',user='root',passwd='raghvi@123',database='wellwatchin')
            mycursor_post=mydb_post.cursor()
            d=request.POST
            for key,value in d.items():
                if key=='address':
                    address=value
                elif key=='city':
                    city=value
                elif key=='state':
                    state=value
                elif key=='country':
                    country=value
                elif key=='pcode':
                    pcode=int(value)
                elif key=='pno':
                    pno=int(value)
                elif key=='extra':
                    extra=value
                elif key=='feedback':
                    feedback=value
            
            c = "INSERT INTO wellwatchin_profile (address, city, state, country, postalcode, phone, extra, feedback,username) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s)"
            values = (address,city,state,country,pcode,pno,extra,feedback,user_profile['username'])
            mycursor_post.execute(c,values)
            
            
            mydb_post.commit()
            mycursor_post.close()
            mydb_post.close()      

            return render(request, 'home.html')
    except mysql.connector.Error as err:
        # Handle database errors
        print("MySQL Error:", err)
        return render(request, 'profile.html', {'user_profile': None})

    return render(request, 'profile.html', {'user_profile':user_profile})




@login_required  # Ensure the user is authenticated
def info(request):
    
    try:
        # Establish a connection to MySQL
        mydb = mysql.connector.connect(host='localhost', user='root', passwd='raghvi@123', database='wellwatchin')
        mycursor = mydb.cursor(dictionary=True)

        # Retrieve user profile data from MySQL based on the logged-in user's email
        query = "SELECT * FROM wellwatchin_signup WHERE username = %s"
        mycursor.execute(query, (request.user.username,))
        user_profile = mycursor.fetchone()
        query2 = "SELECT * FROM wellwatchin_profile WHERE username = %s"
        mycursor.execute(query2, (user_profile['username'],))
        updated_profile = mycursor.fetchone()
        # Close the database connection
        mycursor.close()
        mydb.close()

        


    except mysql.connector.Error as err:
        # Handle database errors
        print("MySQL Error:", err)
        return render(request, 'info.html', {'user_profile': None, 'updated_profile': None})
    
    

    return render(request, 'info.html', {'user_profile': user_profile, 'updated_profile': updated_profile})




import mysql.connector
uname=''
umail=''
username=''
passwd=''
uage=0
gender=''
uheight=0
uweight=0
bloodgroup=''
def signup(request):
    global uname,umail,username,passwd,uage,gender,uheight,uweight,bloodgroup
    if request.method=='POST':
        mydb=mysql.connector.connect(host='localhost',user='root',passwd='raghvi@123',database='wellwatchin')
        mycursor=mydb.cursor(dictionary=True)
        d=request.POST
        for key,value in d.items():
            if key=='uname':
                uname=value
            elif key=='umail':
                umail=value
            elif key=='passwd':
                passwd=value
            elif key=='uage':
                uage=value
            elif key=='gender':
                gender=value
            elif key=='uheight':
                uheight=value
            elif key=='uweight':
                uweight=value
            elif key=='bloodgroup':
                bloodgroup=value
            elif key=='username':
                username=value
        c = "INSERT INTO wellwatchin_signup (name, email, username, password, age, gender, height, weight, bloodgroup) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (uname, umail, username, passwd, uage, gender, uheight, uweight, bloodgroup)
        mycursor.execute(c, values)

        mydb.commit()
        mydb.close()
    return render(request,'signup.html')



def loginview(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('passwd')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return render(request,'login.html')
    else:
        return render(request,'login.html')

def logoutuser(request):
    logout(request)
    return redirect('/LoginView')





import matplotlib.pyplot as plt
from io import BytesIO
import base64  # handling binary data and encoding/decoding data
from datetime import datetime

dur=0
dt=''
username2=''
@login_required
def exercise(request):
    username2=request.user.username
    mydb=mysql.connector.connect(host='localhost',user='root',passwd='raghvi@123',database='wellwatchin')
    mycursor=mydb.cursor()
    q="SELECT date,duration FROM wellwatchin_exercise where username= %s ORDER BY date"
    mycursor.execute(q, [username2],)
    rows=mycursor.fetchall()
    dates = [datetime.strftime(row[0], "%Y-%m-%d") for row in rows]  # Format dates as 'YYYY-MM-DD'
    durations = [row[1] for row in rows]

    

    plt.figure(figsize=(6, 5.5))
    plt.plot(dates, durations, marker='o', linestyle='-', color='blue', linewidth=2, markersize=8, label='Exercise Duration')
    plt.title('Exercise Duration Over Time')
    plt.xlabel('Date ("YYYY-MM-DD")')
    plt.ylabel('Duration (minutes)')
    plt.xticks(rotation=45)
    plt.tight_layout() # automatically adjust subplot parameters to give specified padding.

    for i, txt in enumerate(durations):
        plt.annotate(txt, (dates[i], durations[i]), textcoords="offset points", xytext=(0,5), ha='center')
    #iterates over the durations list along with their corresponding indices. i represents the index of each duration in the list


    # Convert the graph to a base64-encoded image
    buffer = BytesIO()  #creates object
    plt.savefig(buffer, format='png') #Saves the current figure (plot) generated by matplotlib into the buffer object in PNG format
    buffer.seek(0) #his is necessary because after writing data into the buffer, the position is typically at the end
    image_png = buffer.getvalue() # Reads all the data from the buffer and stores it 
    buffer.close() #Closes the buffer, freeing up any system resources


    graph=base64.b64encode(image_png).decode() #converts the binary data into a sequence of ASCII characters.
    #base64.b64encode() returns bytes, and if you want to work with the result as a string, you need to decode it.
    plt.close()
    global dur,dt
    
    if request.method=='POST':
        mydb=mysql.connector.connect(host='localhost',user='root',passwd='raghvi@123',database='wellwatchin')
        mycursor=mydb.cursor(dictionary=True)
        d=request.POST
        for key,value in d.items():
            if key=='duration':
                dur=value
            elif key=='date':
                dt=value
            elif key=='username':
                username2=value
        c = "INSERT INTO wellwatchin_exercise (username,duration,date) VALUES (%s, %s, %s)"
        values = (username2,dur,dt)
        mycursor.execute(c, values)
        mydb.commit()
        mydb.close()
        username2=request.user.username
        mydb=mysql.connector.connect(host='localhost',user='root',passwd='raghvi@123',database='wellwatchin')
        mycursor=mydb.cursor()
        q="SELECT date,duration FROM wellwatchin_exercise where username= %s ORDER BY date"
        mycursor.execute(q, [username2],)
        rows=mycursor.fetchall()
        dates = [datetime.strftime(row[0], "%Y-%m-%d") for row in rows]  # Format dates as 'YYYY-MM-DD'
        durations = [row[1] for row in rows]

        

        plt.figure(figsize=(6, 5.5))
        plt.plot(dates, durations, marker='o', linestyle='-', color='blue', linewidth=2, markersize=8, label='Exercise Duration')
        plt.title('Exercise Duration Over Time')
        plt.xlabel('Date ("YYYY-MM-DD")')
        plt.ylabel('Duration (minutes)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        

        for i, txt in enumerate(durations):
            plt.annotate(txt, (dates[i], durations[i]), textcoords="offset points", xytext=(0,5), ha='center')
            #iterates over the durations list along with their corresponding indices. i represents the index of each duration in the list

        # Convert the graph to a base64-encoded image
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()


        graph=base64.b64encode(image_png).decode()
        plt.close()
        return render(request, 'exercise.html', {'graph': graph})
    return render(request, 'exercise.html', {'graph': graph})


sbp=''
dbp=''
username3=''
def bp(request):
    username3=request.user.username
    context={'variable':'Enter the details above to measure your BP!'}
    if request.method=='POST':
        d=request.POST
        for key,value in d.items():
            if key=='sbp':
                sbp=value
            elif key=='dbp':
                dbp=value
            elif key=='username':
                username3=value
        s=int(sbp)
        dp=int(dbp)
        if (s<120 and dp<80):
            context={
                'variable':'Be Happy! Your BP is NORMAL'
            }
        elif (120<=s<=129 and dp<80):
            context={
                'variable':'Take Care! Your BP is ELEVATED'
            }
        elif (130<=s<=139 or 80<=dp<=89):
            context={
                'variable':'Take Care! Your have HIGH BP STAGE 1'
            }
        elif (s>=140 or dp>=90):
            context={
                'variable':'Take Care! Your have HIGH BP STAGE 2'
            }
        elif (s>=180 or dp>=120):
            context={
                'variable':'Take Care! Your have HYPERTENSIVE CRISIS Pls consult a doctor immediately!'
            }
        return render(request,'bp.html',context)
    return render(request,'bp.html',context)



def tabs(request):
    username2=request.user.username
    context={
        'Variable': username2
    }
    return render(request,'tab_page.html',context)

def weight_tracker(request):
    username2=request.user.username
    mydb=mysql.connector.connect(host='localhost',user='root',passwd='raghvi@123',database='wellwatchin')
    mycursor=mydb.cursor()
    q="SELECT date,weight FROM wellwatchin_weight where username= %s ORDER BY date"
    mycursor.execute(q, [username2],)
    rows=mycursor.fetchall()
    dates = [datetime.strftime(row[0], "%Y-%m-%d") for row in rows]  # Format dates as 'YYYY-MM-DD'
    weights = [row[1] for row in rows] #row in rows, it takes the second element (row[1]) representing weights

    

    plt.figure(figsize=(6, 5.5))
    plt.plot(dates, weights, marker='o', linestyle='-', color='blue', linewidth=2, markersize=8, label='Weight')
    plt.title('Weight')
    plt.xlabel('Date ("YYYY-MM-DD")')
    plt.ylabel('Weight(Kg)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    

    for i, txt in enumerate(weights):
        plt.annotate(txt, (dates[i], weights[i]), textcoords="offset points", xytext=(0,5), ha='center')
    
    # Convert the graph to a base64-encoded image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()


    graph=base64.b64encode(image_png).decode()
    plt.close()
    global dur,dt
    
    if request.method=='POST':
        mydb=mysql.connector.connect(host='localhost',user='root',passwd='raghvi@123',database='wellwatchin')
        mycursor=mydb.cursor(dictionary=True)
        d=request.POST
        for key,value in d.items():
            if key=='weight':
                wht=value
            elif key=='date':
                dt=value
            elif key=='username':
                username2=value
        c = "INSERT INTO wellwatchin_weight (username,weight,date) VALUES (%s, %s, %s)"
        values = (username2,wht,dt)
        mycursor.execute(c, values)
        mydb.commit()
        mydb.close()
        username2=request.user.username
        mydb=mysql.connector.connect(host='localhost',user='root',passwd='raghvi@123',database='wellwatchin')
        mycursor=mydb.cursor()
        q="SELECT date,weight FROM wellwatchin_weight where username= %s ORDER BY date"
        mycursor.execute(q, [username2],)
        rows=mycursor.fetchall()
        dates = [datetime.strftime(row[0], "%Y-%m-%d") for row in rows]  # Format dates as 'YYYY-MM-DD'
        weights = [row[1] for row in rows]

        

        plt.figure(figsize=(6, 5.5))
        plt.plot(dates, weights, marker='o', linestyle='-', color='blue', linewidth=2, markersize=8, label='Weight')
        plt.title('Weight')
        plt.xlabel('Date ("YYYY-MM-DD")')
        plt.ylabel('Weight(Kg)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        

        for i, txt in enumerate(weights):
            plt.annotate(txt, (dates[i], weights[i]), textcoords="offset points", xytext=(0,5), ha='center')
        
        # Convert the graph to a base64-encoded image
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()


        graph=base64.b64encode(image_png).decode()
        plt.close()
        return render(request, 'weight.html', {'graph': graph})
    return render(request, 'weight.html', {'graph': graph})


def sleep_tracker(request):
    username2=request.user.username
    mydb=mysql.connector.connect(host='localhost',user='root',passwd='raghvi@123',database='wellwatchin')
    mycursor=mydb.cursor()
    q="SELECT date,sleep FROM wellwatchin_sleep where username= %s ORDER BY date"
    mycursor.execute(q, [username2],)
    rows=mycursor.fetchall()
    dates = [datetime.strftime(row[0], "%Y-%m-%d") for row in rows]  # Format dates as 'YYYY-MM-DD'
    sleeps = [row[1] for row in rows]

    

    plt.figure(figsize=(6, 5.5))
    # plt.scatter(dates, sleeps, color='blue', label='Sleep', marker='o', s=50)
    plt.stackplot(dates, sleeps, colors=['#197e62'], labels=['Weight'])
    plt.title('Sleep hrs')
    plt.xlabel('Date ("YYYY-MM-DD")')
    plt.ylabel('Sleep(hrs)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    

    for i, txt in enumerate(sleeps):
        plt.annotate(txt, (dates[i], sleeps[i]), textcoords="offset points", xytext=(0,5), ha='center')

    # Convert the graph to a base64-encoded image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()


    graph=base64.b64encode(image_png).decode()
    plt.close()
    global hrs,dt
    
    if request.method=='POST':
        mydb=mysql.connector.connect(host='localhost',user='root',passwd='raghvi@123',database='wellwatchin')
        mycursor=mydb.cursor(dictionary=True)
        d=request.POST
        for key,value in d.items():
            if key=='sleep':
                hrs=value
            elif key=='date':
                dt=value
            elif key=='username':
                username2=value
        c = "INSERT INTO wellwatchin_sleep (username,sleep,date) VALUES (%s, %s, %s)"
        values = (username2,hrs,dt)
        mycursor.execute(c, values)
        mydb.commit()
        mydb.close()
        username2=request.user.username
        mydb=mysql.connector.connect(host='localhost',user='root',passwd='raghvi@123',database='wellwatchin')
        mycursor=mydb.cursor()
        q="SELECT date,sleep FROM wellwatchin_sleep where username= %s ORDER BY date"
        mycursor.execute(q, [username2],)
        rows=mycursor.fetchall()
        dates = [datetime.strftime(row[0], "%Y-%m-%d") for row in rows]  # Format dates as 'YYYY-MM-DD'
        sleeps = [row[1] for row in rows]

        

        plt.figure(figsize=(6, 5.5))
        # plt.scatter(dates, sleeps, color='blue', label='Sleep', marker='o', s=50)
        plt.stackplot(dates, sleeps, colors=['#197e62'], labels=['Weight'])
        plt.title('Sleep hrs')
        plt.xlabel('Date ("YYYY-MM-DD")')
        plt.ylabel('Sleep(hrs)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        

        for i, txt in enumerate(sleeps):
            plt.annotate(txt, (dates[i], sleeps[i]), textcoords="offset points", xytext=(0,5), ha='center')

        # Convert the graph to a base64-encoded image
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()


        graph=base64.b64encode(image_png).decode()
        plt.close()
        return render(request, 'sleep.html', {'graph': graph})
    return render(request, 'sleep.html', {'graph': graph})


quant=0
dt=''
def water_tracker(request):
    username2=request.user.username
    mydb=mysql.connector.connect(host='localhost',user='root',passwd='raghvi@123',database='wellwatchin')
    mycursor=mydb.cursor()
    q="SELECT date,quantity FROM wellwatchin_water where username= %s ORDER BY date"
    mycursor.execute(q, [username2],)
    rows=mycursor.fetchall()
    dates = [datetime.strftime(row[0], "%Y-%m-%d") for row in rows]  # Format dates as 'YYYY-MM-DD'
    quantities = [row[1] for row in rows]

    

    plt.figure(figsize=(6, 5.5))
    plt.bar(dates, quantities, color='blue', label='Water intake(no. of glasses)')
    plt.title('Water intake')
    plt.xlabel('Date ("YYYY-MM-DD")')
    plt.ylabel('Quantity (glasses)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    

    for i, txt in enumerate(quantities):
        plt.annotate(txt, (dates[i], quantities[i]), textcoords="offset points", xytext=(0,5), ha='center')


    # Convert the graph to a base64-encoded image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png =buffer.getvalue()
    buffer.close()


    graph=base64.b64encode(image_png).decode()
    plt.close()
    global quant,dt
    
    if request.method=='POST':
        mydb=mysql.connector.connect(host='localhost',user='root',passwd='raghvi@123',database='wellwatchin')
        mycursor=mydb.cursor(dictionary=True)
        d=request.POST
        for key,value in d.items():
            if key=='quantity':
                quant=value
            elif key=='date':
                dt=value
            elif key=='username':
                username2=value
        c = "INSERT INTO wellwatchin_water (username,quantity,date) VALUES (%s, %s, %s)"
        values = (username2,quant,dt)
        mycursor.execute(c, values)
        mydb.commit()
        mydb.close()
        username2=request.user.username
        mydb=mysql.connector.connect(host='localhost',user='root',passwd='raghvi@123',database='wellwatchin')
        mycursor=mydb.cursor()
        q="SELECT date,quantity FROM wellwatchin_water where username= %s ORDER BY date"
        mycursor.execute(q, [username2],)
        rows=mycursor.fetchall()
        dates = [datetime.strftime(row[0], "%Y-%m-%d") for row in rows]  # Format dates as 'YYYY-MM-DD'
        quantities = [row[1] for row in rows]

        

        plt.figure(figsize=(6, 5.5))
        plt.bar(dates, quantities, color='blue', label='Water intake(no. of glasses)')
        plt.title('Water intake')
        plt.xlabel('Date ("YYYY-MM-DD")')
        plt.ylabel('Quantity (glasses)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        

        for i, txt in enumerate(quantities):
            plt.annotate(txt, (dates[i], quantities[i]), textcoords="offset points", xytext=(0,5), ha='center')


        # Convert the graph to a base64-encoded image
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png =buffer.getvalue()
        buffer.close()


        graph=base64.b64encode(image_png).decode()
        plt.close()
        return render(request, 'water.html', {'graph': graph})
    return render(request, 'water.html', {'graph': graph})


def bmi(request):
    if request.method=='POST':
        mydb=mysql.connector.connect(host='localhost',user='root',passwd='raghvi@123',database='wellwatchin')
        mycursor=mydb.cursor(dictionary=True)
        d=request.POST
        for key,value in d.items():
            if key=='weight':
                weight=float(value)
            elif key=='height':
                height=float(value)
        h = height * height
        context = {
            'Variable': weight / h
        }
        mycursor.close()

        return render(request,'bmi.html',context)
    else:
        return render(request,'bmi.html')