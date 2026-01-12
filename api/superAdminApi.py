from flask import Blueprint, request, jsonify
from Models.models import SuperAdmin
from Database.database import SessionLocal
import datetime

superadmin_bp = Blueprint("superAdminApi", __name__)

@superadmin_bp.route("/add/superadmin", methods=["POST"])
def add_superAdmin():
    session = SessionLocal()
    
    try:
        data = request.get_json()
        
        admin_name = data.get("Admin_name")
        shortname = data.get("Shortname")
        email_id = data.get("Email_ID")
        password = data.get("Password")

        if not admin_name or not shortname or not email_id or not password:
            return jsonify({
                "message": "Admin_name, Shortname, Email_ID and Password are required.",
                "success": False
            }), 400

        # Unique checks
        if session.query(SuperAdmin).filter_by(Admin_name=admin_name).first():
            return jsonify({"message": "Admin name already exists.", "success": False}), 400

        if session.query(SuperAdmin).filter_by(Shortname=shortname).first():
            return jsonify({"message": "Shortname already exists.", "success": False}), 400

        if session.query(SuperAdmin).filter_by(Email_ID=email_id).first():
            return jsonify({"message": "Email already exists.", "success": False}), 400
        
        if session.query(SuperAdmin).filter_by(Password=password).first():
            return jsonify({"message" : "Password already exists.", "success" : False}), 400

        new_admin = SuperAdmin(
            Admin_name=admin_name,
            Shortname=shortname,
            Email_ID=email_id,
            Password=password
        )

        session.add(new_admin)
        session.commit()

        return jsonify({
            "message": "SuperAdmin added successfully",
            "success": True
        }), 200

    except Exception as e:
        session.rollback()
        return jsonify({
            "message": "Internal server error",
            "error": str(e),
            "success": False
        }), 500
    finally:
        session.close()
        
@superadmin_bp.route("/get/superadmin", methods=["GET"])
def get_superAdmin():
    session = SessionLocal()
    
    try:
        super_id = request.args.get("Super_ID")
        admin_name = request.args.get("Admin_name")
        email_id = request.args.get("Email_ID")
        is_active = request.args.get("IsActive")

        query = session.query(SuperAdmin)

        if super_id:
            query = query.filter_by(Super_ID=super_id)
        if admin_name:
            query = query.filter_by(Admin_name=admin_name)
        if email_id:
            query = query.filter_by(Email_ID=email_id)
        if is_active:
            query = query.filter_by(IsActive=is_active)

        results = query.all()

        data = [{
            "Super_ID": s.Super_ID,
            "Admin_name": s.Admin_name,
            "Shortname": s.Shortname,
            "Email_ID": s.Email_ID,
            "IsActive": s.IsActive,
            "Created_On": s.Created_On
        } for s in results]

        return jsonify({
            "message": "SuperAdmin data retrieved successfully",
            "success": True,
            "data": data
        }), 200

    except Exception as e:
        return jsonify({
            "message": "Internal server error",
            "error": str(e),
            "success": False
        }), 500
    finally:
        session.close()
        
        
@superadmin_bp.route("/update/superadmin/<int:super_id>", methods=["PUT"])
def update_superAdmin(super_id):
    session = SessionLocal()
    
    try:
        data = request.get_json()

        admin_name = data.get("Admin_name")
        shortname = data.get("Shortname")
        email_id = data.get("Email_ID")
        password = data.get("Password")
        is_active = data.get("IsActive")

        admin = session.query(SuperAdmin).get(super_id)
        if not admin:
            return jsonify({"message": "SuperAdmin not found", "success": False}), 404

        if admin_name:
            exists = session.query(SuperAdmin).filter(
                SuperAdmin.Super_ID != super_id,
                SuperAdmin.Admin_name == admin_name
            ).first()
            if exists:
                return jsonify({"message": "Admin name already exists", "success": False}), 400
            admin.Admin_name = admin_name

        if shortname:
            exists = session.query(SuperAdmin).filter(
                SuperAdmin.Super_ID != super_id,
                SuperAdmin.Shortname == shortname
            ).first()
            if exists:
                return jsonify({"message": "Shortname already exists", "success": False}), 400
            admin.Shortname = shortname

        if email_id:
            exists = session.query(SuperAdmin).filter(
                SuperAdmin.Super_ID != super_id,
                SuperAdmin.Email_ID == email_id
            ).first()
            if exists:
                return jsonify({"message": "Email already exists", "success": False}), 400
            admin.Email_ID = email_id

        if password:
            admin.Password = password

        if is_active is not None:
            admin.IsActive = is_active

        session.commit()

        return jsonify({
            "message": "SuperAdmin updated successfully",
            "success": True
        }), 200

    except Exception as e:
        session.rollback()
        return jsonify({
            "message": "Internal server error",
            "error": str(e),
            "success": False
        }), 500
    finally:
        session.close()


@superadmin_bp.route("/delete/superadmin/<int:super_id>", methods=["DELETE"])
def delete_superadmin(super_id):
    session = SessionLocal()

    try:
        admin = session.query(SuperAdmin).get(super_id)
        if not admin:
            return jsonify({"message": "SuperAdmin not found", "success": False}), 404

        session.delete(admin)
        session.commit()

        return jsonify({
            "message": "SuperAdmin deleted successfully",
            "success": True
        }), 200

    except Exception as e:
        session.rollback()
        return jsonify({
            "message": "Internal server error",
            "error": str(e),
            "success": False
        }), 500
    finally:
        session.close()
