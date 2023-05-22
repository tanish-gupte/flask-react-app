from flask import Flask, request, redirect, session, render_template
import dbconfig
from dotenv import load_dotenv 
from flask_session import Session
from flask_restful import Resource, Api, reqparse
import jsonify
import json
import uuid
from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptographyHelper import Cryptography
import rsa



load_dotenv()

app = Flask(__name__)
CORS(app ) #can use supports_credentials=True as an option to allow browsers to send cookies to the server
api = Api(app)


app.config["SECRET_KEY"] = "sessionkey"
app.config["SESSION_TYPE"] = "filesystem"

server_session = Session(app)

bcrypt = Bcrypt(app)


# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

print("appconfig", app.config)

class ConnectDb (Resource):
    conn = None
    cursr = None 

    uniqueId = None 

    def __init__ (self):
        conn = dbconfig.connectDB()
        cursr = conn.cursor()

        self.cursr = cursr
        self.conn = conn

        self.uniqueId = uuid.uuid4()    

class UserSignup(ConnectDb):  
    def __init__ (self):
        super().__init__()

    def post (self):
        try:
            
            with open("public_key.pem", "rb") as f:
                public_key = rsa.PublicKey.load_pkcs1(f.read())

            with open("private_key.pem", "rb") as f:
                private_key = rsa.PrivateKey.load_pkcs1(f.read())   

            print("from post!!")
            userUniqueId = self.uniqueId

            json_data = request.get_json(force=True)

            print("json_data: ", json_data)

            encrypted_json = rsa.encrypt(json_data, public_key)

            print("encrypted_json: ", encrypted_json)


            # encryption logic

            # private_key = rsa.generate_private_key(
            #     public_exponent=65537,
            #     key_size=2048,
            # )

            # public_key = private_key.public_key()

            # encryptedData = public_key.encrypt(
            #     json_data,
            #     padding.OAEP(
            #     mgf=padding.MGF1(algorithm=hashes.SHA256()),
            #     algorithm=hashes.SHA256(),
            #     label=None
            #     )
            # )



            firstName = json_data["firstName"]
            lastName = json_data['lastName']
            username = json_data['username']
            uPassword = json_data['uPassword']
            email = json_data['email']
            phone = json_data['phone']
            active = json_data['active']
            userRoleID = json_data['userRoleID'] 

            hashedPw = bcrypt.generate_password_hash(uPassword)


            insert_user_query = """INSERT INTO tblPracticeUsers (UserUniqueID, FirstName, LastName, UserName, UPassword, Email, Phone, Active, userRoleID)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

            values = (userUniqueId, firstName, lastName, username, hashedPw, email, phone, active, userRoleID)

            self.cursr.execute(insert_user_query, values)
            self.conn.commit()
           
            print ("lastrowid", self.cursr.lastrowid)   
            print ("cursor", self.cursr)   

            return {
                'status': 'Ok',
                'msg': 'User Registered Successfully'
            }   

        except Exception as e:
            print(str(e))
            return {'from post status': 'Something went wrong'}
        
        finally:
            if self.cursr and self.conn:
                self.cursr.close()
                self.conn.close()    

    def get (self):
        try:
            allUsers = []
            print("from get!!")  

            get_all_users = """SELECT UserId, userUniqueID, firstName, lastName, userName, uPassword, email, phone
                               FROM tblPracticeUsers"""

            self.cursr.execute(get_all_users)
            # self.conn.commit()     # should commit everytime a change is added to the database

            users = self.cursr.fetchall() # fetches data in tuple

            for user in users:

                obj = {
                    "userId": user[0],
                    "uniqueUserId" : uuid.uuid4(),
                    "firstname" : user[2],
                    "lastname" : user[3],
                    "username" : user[4],
                    "uPassword" : user[5],
                    "email" : user[6],
                    "phone" : user[7]
                }

                allUsers.append(obj)

            print("allUsers", allUsers)

            return allUsers

        except Exception as e:
            print(str(e))
            return {'from get status': 'Something went wrong'}
        
        finally:
            if self.cursr and self.conn:
                self.cursr.close()
                self.conn.close()                            

class UserSignin (ConnectDb):
    def __init__ (self):
        super().__init__()

    def post (self):
        print("from login")

        # if session.get('user'): # check whether user has already logged in 
        #     return jsonify({'message': 'User is already logged in.'})
        
        json_data = request.get_json(force=True)
        print("json_data: ", json_data) 

        username = json_data['username']
        uPassword = json_data['uPassword']

        print("username type: ", type(username))

        login_query = """SELECT UserName, UPassword
        FROM tblPracticeUsers WHERE UserName=%s"""

        values = (username)

        self.cursr.execute(login_query, values)

        queryResp = self.cursr.fetchone()

        print("queryResp[0]: ", queryResp[0])
        print("queryResp[1]: ", queryResp[1])
        
        if queryResp:
            ifHashed = bcrypt.check_password_hash(queryResp[1], uPassword)
            print('ifhashed', ifHashed)

            print("hashing checked", queryResp[1])

        
        user = {
            "username": queryResp[0],
            "password": queryResp[1]
        }

    
        print("user: ", user)
        print("user.username: ", user['username'])
        print("user.password: ", user['password'])

        session['username'] = user['username']

        print("username in session:", session)

        print("user:", user)


        return {
            'status': 'Ok',
            'user': user
        }
    
        # if user and user.username:
        #     session['loggedin'] = user.username

        #     return redirect()

        # else:
        #     return "Invalid Login Credentials"
    
    # def home (self):


class User (ConnectDb):
    def __init__ (self):
        super().__init__() 

    def get (self):
        print("From /user")

        username = session.get('username')
        print('username from user', username)

        if not username:
            return jsonify({'message': 'User is not logged in.'})
        
        else:
            username = session.get('username') 
    
            if not username:
                return jsonify({"error": "Unauthorised"})
            
            getByUsername = """SELECT UserName, FirstName, LastName, Email, Phone, UPassword
            FROM tblPracticeUsers WHERE UserName=%s"""

            values = (username)

            self.cursr.execute(getByUsername, values)

            userInDb = self.cursr.fetchone()
            print("user route user:", userInDb) 

        user = {
            'UserName': userInDb[0],
            'FirstName': userInDb[1],
            'LastName': userInDb[2],
            'Email': userInDb[3],
            'Phone': userInDb[4],
            'UPassword': userInDb[5]
        }

        return user


class ProfilePage (ConnectDb):
    def __init__ (self):
        super().__init__()   

    def get (self):
        if 'user' in session:
            return app.send_static_file('/profile.js')

        else:
            return redirect('/login')
        
      

class Session ():
    def __init__ (self):
        super().__init__()

    def set_session (self, value):
        session['sessionValue']  = value
        return f'The session value set is {value}'

    def get_session (self, value):
        session.get = value


api.add_resource(UserSignup, '/signup')  
api.add_resource(UserSignin, '/signin')  
api.add_resource(User, '/me')   
api.add_resource(ProfilePage, '/profile-page')  
# api.add_resource(Session, '/user')  

if __name__ == "__main__":
    print("from flask_restful")

    app.run(
        host = "0.0.0.0", 
        debug = True, 
        port = 1111
    )