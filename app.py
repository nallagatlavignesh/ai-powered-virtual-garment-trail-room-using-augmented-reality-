
from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify, Response
from camera import VideoCamera
import mysql.connector, os, base64


app = Flask(__name__)
app.secret_key = 'trails' 
app.config['UPLOAD_FOLDER'] = r'static\New'

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    port="3306",
    database='trails'
)

mycursor = mydb.cursor()

def executionquery(query,values):
    mycursor.execute(query,values)
    mydb.commit()
    return

def retrivequery1(query,values):
    mycursor.execute(query,values)
    data = mycursor.fetchall()
    return data

def retrivequery2(query):
    mycursor.execute(query)
    data = mycursor.fetchall()
    return data



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        c_password = request.form['c_password']

        if password == c_password:
            query = "SELECT email FROM users"
            email_data = retrivequery2(query)
            email_data_list = []
            for i in email_data:
                email_data_list.append(i[0])

            if email not in email_data_list:
                query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
                values = (name, email, password)
                executionquery(query, values)

                return render_template('login.html', message="Successfully Registered!")
            return render_template('register.html', message="This email ID is already exists!")
        return render_template('register.html', message="Conform password is not match!")
    return render_template('register.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        if email.lower() == "admin@gmail.com" and password == "admin":
            return redirect("/admin")
        
        query = "SELECT email FROM users"
        email_data = retrivequery2(query)
        email_data_list = []
        for i in email_data:
            email_data_list.append(i[0])

        if email in email_data_list:
            query = "SELECT * FROM users WHERE email = %s"
            values = (email,)
            password__data = retrivequery1(query, values)
            if password == password__data[0][3]:
                session["user_id"] = password__data[0][0]
                session["user_name"] = password__data[0][1]
                session["user_email"] = email

                return redirect("/home")
            return render_template('login.html', message= "Invalid Password!!")
        return render_template('login.html', message= "This email ID does not exist!")
    return render_template('login.html')


@app.route('/features')
def features():
    return render_template('features.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')




### User panel

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/product', methods = ["GET", "POST"])
def product():
    message = None
    if request.method == "POST":
        id = request.form['id']

        query = "INSERT INTO cart (product_id, status) VALUES (%s, %s)"
        values = (id, "pending")
        executionquery(query, values)
        
        message = "Successfully added into cart!"


    query = "SELECT * FROM cloths"
    gallery_data = retrivequery2(query)

    gallery_list = []
    for item in gallery_data:
        gallery_list.append({
            'id': item[0],
            'name': item[1],
            'category': item[2],
            'cost': item[3],
            'img': item[4]
        })

    return render_template('product.html', gallery_data = gallery_list, message = message)


@app.route('/cart')
def cart():
    query = "SELECT * FROM cart"
    cart_data = retrivequery2(query)

    cart_ids = [str(i[1]) for i in cart_data]

    if cart_ids:
        query = f"SELECT * FROM cloths WHERE id IN ({', '.join(cart_ids)})"
        gallery_data = retrivequery2(query)
    else:
        gallery_data = []

    gallery_list = []
    for item in gallery_data:
        gallery_list.append({
            'id': item[0],
            'name': item[1],
            'category': item[2],
            'cost': item[3],
            'img': item[4]
        })
    return render_template('cart.html', gallery_list=gallery_list)


@app.route('/remove_from_cart', methods=["POST"])
def remove_from_cart():
    product_id = request.form.get('product_id')
    if product_id:
        query = "DELETE FROM cart WHERE product_id = %s"
        values = (product_id,)
        executionquery(query, values)
        return jsonify({'success': True, 'message': 'Item removed from cart'})
    return jsonify({'success': False, 'message': 'Failed to remove item from cart'})


# @app.route('/virtual_trails/<int:product_id>')
# def virtual_trails(product_id):
#     # Retrieve product details from the database
#     query = "SELECT img FROM cloths WHERE id = %s"
#     values = (product_id,)
#     product_data = retrivequery1(query, values)

#     if product_data:
#         # Save the product image to a temporary file
#         product_image_path = os.path.join(app.config['UPLOAD_FOLDER'], f"product_{product_id}.png")
#         with open(product_image_path, "wb") as f:
#             f.write(product_data[0][0])  # Assuming `img` is at index 0

#         # Run the tryOn.py script with the product image path
#         # os.system(f'python tryOn.py {product_image_path}')
#         os.system('python tryOn.py ' + product_image_path)

#         # Redirect to the virtual trial room page
#         return render_template('virtual_trails.html', message="Virtual trial room ready!")
#     else:
#         return render_template('cart.html', message="Product not found for virtual trails.")





# @app.route('/tryon/<file_path>',methods = ['POST', 'GET'])
# def tryon(file_path):
# 	file_path = file_path.replace(',','/')
# 	os.system('python tryOn.py ' + file_path)
# 	return redirect('http://127.0.0.1:5000/',code=302, Response=None)


@app.route('/tryall/<int:product_id>',methods = ['POST', 'GET'])
def tryall(product_id):
    # CART = request.form['mydata'].replace(',', '/')

    query = "SELECT * FROM cloths WHERE id = %s"
    values = (product_id, )
    gallery_data = retrivequery1(query, values)
    img_name = gallery_data[0][4]
    CART = f"static/images/Tops4/{img_name}"
    print(444444444444444, CART)
    os.system('python test.py ' + CART)
    return redirect("/cart")


# def gen(camera):
#     while True:
#         frame = camera.get_frame()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    

# @app.route('/video_feed')
# def video_feed():
#     return Response(gen(VideoCamera()),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')






### Image Trails

import requests
import base64

# Use this function to convert an image file from the filesystem to base64
def image_file_to_base64(image_path):
    with open(image_path, 'rb') as f:
        image_data = f.read()
    return base64.b64encode(image_data).decode('utf-8')

# Use this function to fetch an image from a URL and convert it to base64
def image_url_to_base64(image_url):
    response = requests.get(image_url)
    image_data = response.content
    return base64.b64encode(image_data).decode('utf-8')


@app.route('/image_trail/<int:product_id>',methods = ['POST', 'GET'])
def image_trail(product_id):
    return render_template('image_trail.html', product_id = product_id)


@app.route('/image_trail2',methods = ['POST'])
def image_trail2():
    person_img = request.files["person_img"]
    product_id = request.form["product_id"]

    person_img_name = person_img.filename
    person_img_path = os.path.join('static', 'saved_images', person_img_name)
    person_img.save(person_img_path)

    query = "SELECT * FROM cloths WHERE id = %s"
    values = (product_id, )
    gallery_data = retrivequery1(query, values)
    dress_img_name = gallery_data[0][4]
    dress_image_path = f"static/images/Tops4/{dress_img_name}"
    
    api_key = "SG_976a840f4c19354e"
    url = "https://api.segmind.com/v1/try-on-diffusion"

    # Request payload
    data = {
    "model_image": image_file_to_base64(person_img_path),
    "cloth_image": image_file_to_base64(dress_image_path),
    "category": "Upper body",
    "num_inference_steps": 35,
    "guidance_scale": 2,
    "seed": 12467,
    "base64": False
    }

    headers = {'x-api-key': api_key}
    response = requests.post(url, json=data, headers=headers)
    image_data = response.content

    with open(r'static\saved_images\generated_image.jpg', 'wb') as f:
        f.write(image_data)  

    return render_template('image_trail2.html')





### Admin Panel

@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/add_cloths', methods = ["GET", "POSt"])
def add_cloths():
    if request.method == "POST":
        name = request.form["name"]
        cost = request.form["cost"]
        category = request.form["category"]
        myfile = request.files['img']
        fn = myfile.filename
        mypath = os.path.join('static', 'images', fn)
        myfile.save(mypath)

        query = "INSERT INTO cloths (name, category, cost, img) VALUES (%s, %s, %s, %s)"
        values = (name, category, cost, fn)
        executionquery(query, values)
        return render_template('add_cloths.html', message = "Successfully added!")
    return render_template('add_cloths.html')


@app.route('/manage_cloths', methods = ["GET", "POSt"])
def manage_cloths():
    message = None
    if request.method == "POST":
        cloth_id = int(request.form["id"])
        name = request.form["name"]
        cost = request.form["cost"]
        category = request.form["category"]
        img = request.files["img"]

        if img:
            binary_data = img.read()
            query = "UPDATE cloths SET name = %s, category = %s, cost = %s, img = %s WHERE id = %s"
            values = (name, category, cost, binary_data, cloth_id)
        else:
            query = "UPDATE cloths SET name = %s, category = %s, cost = %s WHERE id = %s"
            values = (name, category, cost, cloth_id)

        executionquery(query, values)
        message = "Updated successfully!"

    query = "SELECT * FROM cloths"
    gallery_data = retrivequery2(query)

    gallery_list = []
    for item in gallery_data:
        gallery_list.append({
            'id': item[0],
            'name': item[1],
            'category': item[2],
            'cost': item[3],
            'img': item[4]
        })

    return render_template('manage_cloths.html', gallery_data = gallery_list, message = message)



@app.route('/delete_cloth/<id>')
def delete_cloth(id):
    query = "DELETE FROM cloths WHERE id = %s"
    values = (id,)
    executionquery(query, values)

    query = "SELECT * FROM cloths"
    gallery_data = retrivequery2(query)

    gallery_list = []
    for item in gallery_data:
        gallery_list.append({
            'id': item[0],
            'name': item[1],
            'category': item[2],
            'cost': item[3],
            'img': item[4]
        })

    return render_template('manage_cloths.html', gallery_data = gallery_list, message = "Deleted successfully!")





if __name__ == '__main__':
    app.run(debug = True)