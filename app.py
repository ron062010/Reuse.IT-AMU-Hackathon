import cv2
from flask.wrappers import Request
from flask import Flask , render_template, request, redirect, url_for, session,Response
import re
import pickle
from flask_mysqldb import MySQL
import MySQLdb.cursors
from selenium import webdriver 
import pandas as pd 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from keras.preprocessing.image import load_img
import numpy as np
from keras.preprocessing import image
from numpy import expand_dims
from matplotlib import pyplot

from os import listdir
from xml.etree import ElementTree
from numpy import zeros
from numpy import asarray
from numpy import expand_dims
from matplotlib import pyplot
from matplotlib.patches import Rectangle
from keras.utils.vis_utils import plot_model
from keras.preprocessing.image import img_to_array

from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import decode_predictions
from keras.applications.vgg16 import VGG16


app=Flask(__name__)
camera=cv2.VideoCapture(0)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'trash management'

# Intialize MySQL
mysql = MySQL(app)
app.secret_key = 'key12'
   
#register
@app.route('/')
def register():
    return render_template('index.html')

@app.route('/index')
def same_page():
    return render_template('index.html')
#login
@app.route('/signup',methods=['GET', 'POST'])
def signup():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'address' in request.form and 'locality' in request.form and 'contact' in request.form and 'usertype' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        address = request.form['address']
        locality = request.form['locality']
        contact = request.form['contact']
        usertype = request.form['usertype']
        print("a")
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM login_credentials WHERE username = %s AND password=%s', [username, password])
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
            print("b")
    
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
            print("c")
        elif not username or not password:
            msg = 'Please fill out the form!'
            print("d")
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO login_credentials VALUES(%s,%s,%s,%s,%s,%s)', [username, password,address,locality,contact,usertype])
            mysql.connection.commit()
            msg = 'Successfully registered! Please Sign-In'
            print("e")
            return render_template('login.html', msg=msg)
            
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    return render_template('signup.html')

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        print("gg")
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM login_credentials WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account['type_of_user'] == "Personal":
            print("b")
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['username'] = account['username']
            session['address'] = account['address']
            session['contact'] = account['contact']
            account['type_of_user'] = "Pe"
            # Redirect to home page
            
            return redirect(url_for('user_home'))
        else:
             return redirect(url_for('dealer_home'))      
    return render_template('login.html')   

#user_home
@app.route('/user_home',methods=['GET', 'POST'])
def user_home():
    return render_template('user_home.html')    

@app.route('/logout',methods=['GET', 'POST'])
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('address', None)
    session.pop('password', None)
    session.pop('contact', None)
    return redirect(url_for('same_page'))    

  
@app.route('/video',methods=['GET', 'POST'])
def video():
    if request.method=='POST' and request.form['upload']=='upload_image':
      xyz()  
      return Response(camera(),mimetype='multipart/x-mixed-replace; boundary=frame')
      

def xyz():
    return render_template('camera_page.html')

cam=cv2.VideoCapture(0) 
def camera():
    img_counter=0
    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k%256 == 32:
            print("worked")
            # SPACE pressed
            img_name = "image.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            
        elif k%256 == 27 :
            # ESC pressed
            print("Escape hit, closing...")
            break
    return render_template('camera_page.html')

#dealer_home
@app.route('/dealer_home', methods=['GET', 'POST'])
def dealer_home():
    return render_template('dealer_home.html')   


#after camera summary
@app.route('/camera_page', methods=['GET', 'POST'])
def camera_page():
    return render_template('camera_page.html')   

#dropoff centers      
@app.route('/dropoff_centers')
def dropoff_centers():
    Cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    Cursor.execute('SELECT * FROM dropoff_centers')
    dropoff_list = Cursor.fetchall()
    dropoff_list = list(dropoff_list)
    Dropoff_list = []


    for i in range(len(dropoff_list)):
        x = dropoff_list[i]
        list_h = []
        for key in x.values():
            list_h.append(key)
        Dropoff_list.append(list_h)
    
    return render_template('dropoff_center.html', Dropoff_list= Dropoff_list)   

#ngo list     
@app.route('/ngo_list')
def ngo_list():
    Cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    Cursor.execute('SELECT * FROM ngo_list')
    ngo_list = Cursor.fetchall()
    ngo_list = list(ngo_list)
    NGO_list = []


    for i in range(len(ngo_list)):
        x = ngo_list[i]
        list_h = []
        for key in x.values():
            list_h.append(key)
        NGO_list.append(list_h)
    
    return render_template('ngo_list.html', NGO_list=NGO_list)    

#waste record     
@app.route('/recycle', methods=['GET', 'POST'])
def recycle():
    
    
    Cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
    Cursor.execute('SELECT name_of_shop FROM dropoff_centers')
    dealer_list = Cursor.fetchall()
    dealer_list = list(dealer_list)
    Dealer_list = []  


    for i in range(len(dealer_list)):
        x = dealer_list[i]
        list_h = []
        for key in x.values():
            list_h.append(key)
        Dealer_list.append(list_h)
    if request.method == 'POST' and 'scraptype' in request.form and 'quantity' in request.form and 'filename' in request.form and 'dealer' in request.form:
        
        username = session['username']
        address = session['address']
        scraptype = request.form['scraptype']
        quantity = request.form['quantity']
        image = request.form['filename']
        contact = session['contact']
        dealer = request.form['dealer']
       
        
        Cursor.execute('INSERT INTO pickup_centers VALUES(%s,%s,%s,%s,%s,%s,%s)', [username,scraptype, quantity,address,contact,image,dealer])
        mysql.connection.commit()
   
        
    return render_template('recycle.html',Dealer_list=Dealer_list)  
  
@app.route('/pickup_center')
def pickup_center():
    
    Cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    Cursor.execute('SELECT * FROM pickup_centers')
    pickup_list = Cursor.fetchall()
    pickup_list = list(pickup_list)
    Pickup_list = []


    for i in range(len(pickup_list)):
        x = pickup_list[i]
        list_h = []
        for key in x.values():
            list_h.append(key)
        Pickup_list.append(list_h)
    print(Pickup_list)    
    return render_template('pickup_center.html', Pickup_list=Pickup_list)  



@app.route('/shortest_path')
def shortest_path():
    
    
    return render_template('map_1.html')   


@app.route('/summary')
def summary():
    return render_template('summary.html')     


@app.route('/user_guide')
def user_guide():
    return render_template('user_guide.html')

@app.route('/dealer_guide')
def dealer_guide():
    return render_template('dealer_guide.html')         

"""@app.route('/rates')
def rates():
    return render_template('rates.html') """    

from keras.models import load_model
model1 = load_model('model.h5')

@app.route('/prediction',methods=['GET', 'POST'])
def prediction():
    LIST =[]
    if request.method=='POST' and request.form['summary']=='summary_page':
       
        
        image1 = load_img('image.jpg', target_size=(224, 224))
        image1 = img_to_array(image1)
        # reshape data for the model
        print(image1.shape)
        image1 = image1.reshape((1, image1.shape[0], image1.shape[1], image1.shape[2]))
        print(image1.shape)

        # prepare the image for the VGG model
        image1 = preprocess_input(image1)

        yhat = model1.predict(image1, verbose=0)[0]
        print(yhat)
        print(yhat.max())
        imp = ''
        obj_name = ''
        if yhat[0] == yhat.max():
            obj_name = 'Battery'
        elif yhat[1] == yhat.max():
            obj_name = 'Cardboard'
        elif yhat[2] == yhat.max():
            obj_name = 'Clothes'
        elif yhat[3] == yhat.max():
            obj_name = 'Metal'
        elif yhat[4] == yhat.max():
            obj_name = 'Paper'
        elif yhat[5] == yhat.max():
            obj_name = 'Plastic'
        elif yhat[6] == yhat.max():
            obj_name = 'Shoes'    
        elif yhat[6] == yhat.max():
            obj_name = 'White-glass'                     


        if  obj_name == 'Battery':
            imp = 'Some batteries contain toxic materials whose injection into ecosystems may cause harm. When added to landfills, the toxic materials may enter the local groundwater system and propagate through the food chain in various ways.'
        elif obj_name == 'Cardboard':
            imp = 'Produces Methane (the greenhouse gas) as it breaks down.'
        elif obj_name == 'Clothes':
            imp = 'Blocks sewage if disposed in open space'
        elif obj_name == 'Metal':
            imp = 'Heavy metals can be found in traces in water sources and still be very toxic and impose serious health problems to humans and other ecosystems'
        elif obj_name == 'Paper':
            imp = 'Toxic materials are released into our water, air and soil. When paper rots, it emits methane gas which is 25 times more toxic than CO2.'
        elif obj_name == 'Plastic':
            imp = 'It can take hundreds or even thousands of years for plastic to break down so the environmental damage is long-lasting.'
        elif obj_name == 'White-glass':
            imp = 'Will outlive generations of people simply by laying in a landfill. It can also kill wildlife, contribute to environmental stressors through continuous recreation, and plays a significant role in both air and water pollution when not recycled.'


        PATH = "C:\Program Files (x86)\chromedriver.exe"
        driver = webdriver.Chrome(PATH)
        base = "https://www.youtube.com/results?search_query="
        input1 = "how+to+reuse+"
        input2 = obj_name
        final_url = base+input1+input2
        driver.get(final_url)

        user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
        links = []
        for i in user_data:
                    links.append(i.get_attribute('href'))
        
        glink1 = "how+to+reuse+"
        glink2 = obj_name
        query = glink1+glink2
        glinks=[]
        for page in range(1):
            url = "http://www.google.com/search?q=" + str(query) + "&start=" 
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            # soup = BeautifulSoup(r.text, 'html.parser')

            search = soup.find_all('div', class_="yuRUbf")
            for h in search:
                glinks.append(h.a.get('href'))
                


        google_links =[glinks[0],glinks[1],glinks[2]]
        youtube_inks = [links[0],links[1],links[2]]
        
        LIST=[obj_name,imp,google_links,youtube_inks]


    return render_template('summary.html', LIST=LIST)


if __name__=="__main__":
    app.run(debug=True)