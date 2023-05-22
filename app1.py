from flask import Flask, request, session, redirect
import jsonify
import json
import uuid
import bcrypt

import dbconfig

app = Flask(__name__)

class ConnectDb (object):
    conn = None
    cursr = None 

    uniqueId = None 

    def __init__ (self):
        conn = dbconfig.connectDB()
        cursr = conn.cursor()

        self.cursr = cursr
        self.conn = conn

        self.uniqueId = uuid.uuid4()    

class UserCRUD(ConnectDb):  
    def __init__ (self):
        super().__init__()

    @app.route('/signup', methods = ['POST'])
    def signup (self):
        try:
            print("from post!!")
            userUniqueId = self.uniqueId

            json_data = request.get_json(force=True)
            print("json_data: ", json_data)

            firstName = json_data["firstName"]
            lastName = json_data['lastName']
            username = json_data['username']
            uPassword = json_data['uPassword']
            email = json_data['email']
            phone = json_data['phone']
            active = json_data['active']
            userRoleID = json_data['userRoleID'] 

            hashedPw = bcrypt.hashpw(uPassword.encode('utf-8'), bcrypt.gensalt())

            insert_user_query = """INSERT INTO tblPracticeUsers (UserUniqueID, FirstName, LastName, UserName, UPassword, Email, Phone, Active, userRoleID)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

            values = (userUniqueId, firstName, lastName, username, hashedPw, email, phone, active, userRoleID)

            self.cursr.execute(insert_user_query, values)
            self.conn.commit()
           
            print ("lastrowid", self.cursr.lastrowid)      

        except Exception as e:
            print(str(e))
            return {'from post status': 'Something went wrong'}
        
        finally:
            if self.cursr and self.conn:
                self.cursr.close()
                self.conn.close()     

    @app.route('/signin', methods = ['POST'])
    def signin (self):
        print("from login")
        json_data = request.get_json(force=True)
        print("json_data: ", json_data) 

        username = json_data['username']
        uPassword = json_data['uPassword']

        login_query = """SELECT UserName, UPassword
        FROM tblPracticeUsers WHERE UserName=%s AND UPassword=%s"""

        values = (username, uPassword)

        self.cursr.execute(login_query, values)

        queryResp = self.cursr.fetchone()

        print("queryResp", queryResp)

        user = {
            "username": queryResp[0],
            "password": queryResp[1]
        }
        print("user:", user)

        if user and user.username:
            session['username'] = user.username


        return redirect("/")

    @app.route('/getUsers')
    def getAllUsers (self):
        try:
            allUsers = []
            print("from getUsers!!")  

            get_all_users = """SELECT UserId, userUniqueID, firstName, lastName, userName, uPassword, email, phone, active
                               FROM tblPracticeUsers"""

            self.cursr.execute(get_all_users)
            self.conn.commit()     # should commit everytime a change is added to the database

            users = self.cursr.fetchall() 

            return {
                "users" : users
            }
        
            # userArr = list(users)  

            # print("printed users in list: ", userArr)

            # # for user in userArr:
            # #     allUsers.append(user)

            # return json.dumps(userArr)

        except Exception as e:
            print(str(e))
            return {'from get status': 'Something went wrong'}
        
        finally:
            if self.cursr and self.conn:
                self.cursr.close()
                self.conn.close()      


userCrud = UserCRUD()
userCrud.signup()


if __name__ == "__main__":
    print("from flask_restful")

    app.run(
        host = "0.0.0.0", 
        debug = True, 
        port = 1111
    )