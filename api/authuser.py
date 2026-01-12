from flask import request,jsonify,Blueprint
from extension import bcrypt
from Database.database import SessionLocal
from flask_jwt_extended import create_access_token
from Models.models import SuperAdmin


auth_user=Blueprint("auth_user",__name__)



@auth_user.route("/auth/register",methods=["POST"])
def user_register():
    session=SessionLocal()
    try:
        data=request.get_json()
        print("RAW DATA:", data)

        
        username=data.get("User_name")
        shortname=data.get("Shortname")
        password=data.get("Password")
        role=data.get("Role")
        # vendor_id=data.get("Vendor_Id")
        isactive=data.get("IsActive")
        
        if not password or not password.strip():
            return jsonify({"message": "Password is required"}), 400
        
        if session.query(SuperAdmin).filter_by(User_name=username).first():
            return jsonify({
                "message":f"user name is already exists {username}",
            }),400
        
        
            
        hash_password=bcrypt.generate_password_hash(password).decode("utf-8")
        print("hash-password",hash_password)
        
        new_user=SuperAdmin(
            
            User_name=username,
            Shortname=shortname,
            Password=hash_password,
            Role=role,
            # Vendor_Id=vendor_id,
            IsActive=isactive
        )
        
        session.add(new_user)
        session.commit()
        
        return jsonify({
            "message":"User registered successfully",
            "success":True
        }),201
        
    except Exception as e:
        session.rollback()
        return jsonify({
            "message":"Failed to register",
            "error":str(e)
        })
        
    finally:
        session.close()
        
        
@auth_user.route("/login",methods=["POST"])
def login_user():
    session=SessionLocal()
    try:
        data = request.get_json()
        
        
        username=data.get("User_name")
        password=data.get("Password")
        
        user=session.query(SuperAdmin).filter_by(User_name=username).first()
        
        if not user:
            return jsonify({
                "success":False,
                "message":"User Name is Not found"
            }),404
            
        if not bcrypt.check_password_hash(user.Password,password):
            return jsonify({
                
                "success":False,
                "message":"Invalid username or password. Please try again."
            }),400
            
        access_token=create_access_token(
            identity={
                "super_id":user.Super_ID,
                "role":user.Role,
                # "vendor_id":user.Vendor_Id
            }
        )
        
        return jsonify({
            "success":True,
            "message":"Login Successfully",
            "user":{
                "token":access_token,
                "Role":user.Role,
                # "vendor_id":user.Vendor_Id
            }
        }),200
        
    except Exception as e:
        return jsonify({
            "success":False,
             "message":f"Internal server error{str(e)}"
        }), 500
    
    finally:
        session.close()
        
        
@auth_user.route("/auth/users", methods=["GET"])
def get_auth_users():
    session = SessionLocal()
    try:
        super_id = request.args.get("Super_ID")
        username = request.args.get("User_name")
        role = request.args.get("Role")
        # vendor_id = request.args.get("Vendor_Id")
        isactive = request.args.get("IsActive")

        query = session.query(SuperAdmin)

        if super_id:
            query = query.filter(SuperAdmin.Super_ID == super_id)

        if username:
            query = query.filter(SuperAdmin.User_name == username)

        if role:
            query = query.filter(SuperAdmin.Role == role)

        # if vendor_id:
        #     query = query.filter(SuperAdmin.Vendor_Id == vendor_id)

        if isactive is not None:
            query = query.filter(SuperAdmin.IsActive == int(isactive))

        users = query.all()

        data = [
            {
                "Super_ID": user.Super_ID,
                "User_name": user.User_name,
                "Shortname": user.Shortname,
                "Role": user.Role,
                # "Vendor_Id": user.Vendor_Id,
                "IsActive": user.IsActive,
                "Created_On": user.Created_On
            }
            for user in users
        ]

        return jsonify({
            "success": True,
            "message": "Auth users retrieved successfully",
            "data": data
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Internal server error",
            "error": str(e)
        }), 500

    finally:
        session.close()
