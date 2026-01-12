from flask import Blueprint, request, jsonify
from Models.models import User
from Database.database import SessionLocal

from flask import Blueprint, request, jsonify
from Models.models import User
from Database.database import SessionLocal
from datetime import datetime
# from werkzeug.security import generate_password_hash  # Optional for password hashing

user_bp = Blueprint("userApi",__name__)

# -----------Add_User-------------
@user_bp.route("/add/user", methods=["POST"])
def add_user():
    session = SessionLocal()
    
    try:
        data = request.get_json()
        user_name = data.get("User_name")
        password = data.get("Password")
        full_name = data.get("Full_name")
        email = data.get("Email")
        mobile_number = data.get("Mobile_number")
        role = data.get("Role")
        department = data.get("Department")


        if not user_name or not password or not full_name or not mobile_number:
            return jsonify({
                "message": "User_name, Password, Full_name and Mobile number are required.",
                "success": False
            }), 400

        if session.query(User).filter_by(User_name=user_name).first():
            return jsonify({"message": "User name already exists.", "success": False}), 400

        if email and session.query(User).filter_by(Email=email).first():
            return jsonify({"message": "Email already exists.", "success": False}), 400
        
        

        # Optionally hash password for security
        # hashed_password = generate_password_hash(password)
        hashed_password = password  # keep plain if not using hashing yet

        new_user = User(
            User_name=user_name,
            Password=hashed_password,
            Full_name=full_name,
            Email=email,
            Mobile_number=mobile_number,
            Role=role,
            Department=department,
        )

        session.add(new_user)
        session.commit()

        return jsonify({
            "message": "User added successfully.",
            "success": True
        }), 200

    except Exception as e:
        session.rollback()
        return jsonify({
            "message": "Internal server error.",
            "error": str(e),
            "success": False
        }), 500

    finally:
        session.close()


# -----------Get_User-------------
@user_bp.route("/get/user", methods=["GET"])
def get_user():
    session = SessionLocal()
    try:
        # Get query parameters
        user_name = request.args.get("User_name")
        password = request.args.get("Password")
        email = request.args.get("Email")
        role = request.args.get("Role")
        department = request.args.get("Department")
        single = request.args.get("single", "false").lower() == "true"  # optional: for using .first()

        query = session.query(User)

        filter_conditions = {}
        if user_name:
            filter_conditions["User_name"] = user_name
        if password:
            filter_conditions["Password"] = password
        if email:
            filter_conditions["Email"] = email
        if role:
            filter_conditions["Role"] = role
        if department:
            filter_conditions["Department"] = department
      
        if filter_conditions:
            query = query.filter_by(**filter_conditions)

        # --- Example use of filter() for custom conditions ---
        # (optional: show how to use .filter() together)
        # For example, retrieve only active users:

        if single:
            user = query.first()
            if not user:
                return jsonify({"message": "User not found", "success": False}), 404

            user_data = {
                "User_Id": user.User_Id,
                "User_name": user.User_name,
                "Password" : user.Password,
                "Full_name": user.Full_name,
                "Email": user.Email,
                "Mobile_number": user.Mobile_number,
                "Role": user.Role,
                "Department": user.Department,
                "Created_at": str(user.Created_at),
                "Updated_at": str(user.Updated_at),
            }

            return jsonify({
                "message": "Single user retrieved successfully.",
                "success": True,
                "data": user_data
            }), 200

        else:
            users = query.all()
            user_data = [
                {
                    "User_Id": u.User_Id,
                    "User_name": u.User_name,
                    "Password": u.Password,
                    "Full_name": u.Full_name,
                    "Email": u.Email,
                    "Mobile_number": u.Mobile_number,
                    "Role": u.Role,
                    "Department": u.Department,
                    "Created_at": str(u.Created_at),
                    "Updated_at": str(u.Updated_at),
                }
                for u in users
            ]

            return jsonify({
                "message": "User data retrieved successfully.",
                "success": True,
                "data": user_data
            }), 200

    except Exception as e:
        session.rollback()
        return jsonify({
            "message": "Internal server error.",
            "error": str(e),
            "success": False
        }), 500
    finally:
        session.close()


# -----------Updated_User-------------
@user_bp.route("/update/user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    session = SessionLocal()
    
    try:
        data = request.get_json()
        user = session.query(User).get(user_id)

        if not user:
            return jsonify({"message": "User not found.", "success": False}), 404

        user_name = data.get("User_name")
        password = data.get("Password")
        full_name = data.get("Full_name")
        email = data.get("Email")
        mobile_number = data.get("Mobile_number")
        role = data.get("Role")
        department = data.get("Department")

        if user_name and session.query(User).filter(User.User_name == user_name, User.User_Id != user_id).first():
            return jsonify({"message": "User name already exists.", "success": False}), 400

        
        if email and session.query(User).filter(User.Email == email, User.User_Id != user_id).first():
            return jsonify({"message": "Email already exists.", "success": False}), 400
        
        if password and session.query(User).filter(User.Password == password, User.Password != password).first():
            return jsonify({"message": "Passwoer already exists.", "seccess": False}), 400

        
        if user_name:
            user.User_name = user_name
        if password:
            # user.Password = generate_password_hash(password)
            user.Password = password  # plain if not hashing yet
        if full_name:
            user.Full_name = full_name
        if email:
            user.Email = email
        if mobile_number:
            user.Mobile_number = mobile_number
        if role:
            user.Role = role
        if department:
            user.Department = department

        user.Updated_at = datetime.utcnow()

        session.commit()

        return jsonify({
            "message": "User updated successfully.",
            "success": True
        }), 200

    except Exception as e:
        session.rollback()
        return jsonify({
            "message": "Internal server error.",
            "error": str(e),
            "success": False
        }), 500
    finally:
        session.close()


# -----------Delete_User-------------
@user_bp.route("/delete/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    session = SessionLocal()
    
    try:
        user = session.query(User).filter(User.User_Id == user_id).first()

        if not user:
            return jsonify({"message": "User not found.", "success": False}), 404

        session.delete(user)
        session.commit()

        return jsonify({
            "message": "User deleted successfully.",
            "success": True
        }), 200

    except Exception as e:
        session.rollback()
        return jsonify({
            "message": "Internal server error.",
            "error": str(e),
            "success": False
        }), 500
    finally:
        session.close()

