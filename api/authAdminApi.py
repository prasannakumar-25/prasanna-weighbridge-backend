from flask import request, Blueprint, jsonify
from Database.database import SessionLocal
from extension import bcrypt
from flask_jwt_extended import create_access_token
from Models.models import SuperAdmin

auth_admin = Blueprint("auth_Admin",__name__)

@auth_admin.route("/authadmin/regiater",methods=["POST"])
def admin_register():
    session = SessionLocal() 
    
    try:
        data = request.get_json()
        
        
        username = data.get("User_name")
        shortname = data.get("Shortname")
        password = data.get("Password")
        role = data.get("Role")
        vendor_id = data.get("Vendor_Id")
        isactive = data.get("IsActive")
        
        if not password or not password.strip():
            return jsonify({"message" : "Password is required"}), 400
        
        if session.query(SuperAdmin).filter_by(User_name=username).first():
            return jsonify ({
                "message" :f"User already exists{username}"
            }), 400
            
        hash_password = bcrypt.generate_password_hash(password).decode("utf-8")
        print("hash_password" , hash_password)
        
        new_admin = SuperAdmin(
            
            user_name = username,
            Shortname = shortname,
            Password  = password,
            Role = role,
            Vendor_Id = vendor_id,
            IsActive = isactive
        )
        
        session.add(new_admin)
        session.commit()
        
        return jsonify ({
            "message" : "Admin register successfully",
            "success" : True
        }), 201
    
    except Exception as e: 
        session.rollback()
        return jsonify({
            "message": "Failed to register",
            "error" : str(e)
        })
    finally:
        session.close()
        
        
@auth_admin.route("/login", methods=["POST"])
def login_admin():
    session = SessionLocal()
    
    try:
        
        data = request.get_json()
        username = data.get("User_name")
        password = data.get("Possword")
        
        admin = session.query(SuperAdmin).filter_by(User_name=username).first()
        
        if not admin:
            return jsonify({
                "success": False,
                "meassage" : f"User not found {username}"
            }), 404
            
        if not bcrypt.check_password_hash(admin.Password,password):
            return jsonify ({
                "success": False,
                "message":"Check your Username or password is incorrect. Please try again"
            }), 400
            
        access_token = create_access_token (
            identity= {
                "super_id" : admin.Super_ID,
                "role" : admin.Role,
                "vednor_id" : admin.Vendor_Id
            }
        )
        
        return jsonify ({
            "success" : True,
            "message" : "Login Successfully",
            "user" : {
                "token" : access_token,
                "Role" : admin.Role,
                "vendor_id" : admin.Vendor_Id 
            }
        }), 200
        
    except Exception as e:
        return jsonify ({
            "success" : False,
            "message" : f"Internal server error{str(e)}"
        }), 500
    finally:
        session.close()