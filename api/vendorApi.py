from flask import Blueprint, request, jsonify
from Models.models import Vendor, SuperAdmin
from Database.database import SessionLocal
import datetime 

vendor_bp = Blueprint("vendorApi",__name__)

#------------------Add vendor--------------------------
@vendor_bp.route("/add/vendor",methods=["POST"])
def add_vendor():
    session = SessionLocal()
    
    try:
        data = request.get_json() 
        
        vendor_name = data.get("Vendor_name")
        super_id = data.get("Super_ID")
        contact_number = data.get("Contact_number")
        email = data.get("Email")
        address = data.get("Address")
        gst_number = data.get("Gst_number")
        website=data.get("Website")
        
        
        existing_admin = session.query(SuperAdmin).filter_by(Super_ID = super_id). first()
        if not existing_admin:
            return jsonify ({
                "message": "Superadmin not found.",
                "success": False
            }), 400
        
        if not super_id or not vendor_name or not contact_number or not email or not address or not website or not  gst_number:
            return jsonify({
                "message": " Super_id , Vendor_name, Contact_number, Email, Address, website and Gst_number are required.",
                "seccess": True,
            }), 400
            
        existing_vendor_name = session.query(Vendor).filter_by(Vendor_name=vendor_name).first()
        if existing_vendor_name:
            return jsonify({
                "message": "Vendor name already exists.",
                "success": False
            }), 400
            
        existing_vendor_email = session.query(Vendor).filter_by(Email=email).first()
        if existing_vendor_email:
            return jsonify({
                "message": "Email already exists.",
                "success": False
            }), 400
            
        new_vendor = Vendor(
            Super_ID = super_id,
            Vendor_name = vendor_name,
            Contact_number = contact_number,
            Email = email,
            Address = address,
            Gst_number = gst_number,
            Website=website,
        )
        session.add(new_vendor)
        session.commit()
        return jsonify({
            "message": "vendor added successfully",
            "success": True
        }), 200
        
    except Exception as e:
        session.rollback()
        return jsonify({
            "message": "Internal server error occurred",
            "error": str(e),
            "success": False
        }), 500
    finally:
        session.close()


#----------------Get vendor--------------------------
@vendor_bp.route("/get/vendor", methods=["GET"])
def get_vendor():
    session = SessionLocal()
    
    try:
        super_id = request.args.get("Super_ID")
        vendor_id=request.args.get("Vendor_Id")
        vendor_name = request.args.get("Vendor_name")
        contact_number = request.args.get("Contact_number")
        email = request.args.get("Email")
        address = request.args.get("Address")
        gst_number = request.args.get("Gst_number")
        website = request.args.get("Website")
        query = session.query(Vendor)
        
        if super_id:
            query = query.filter_by(Super_ID = super_id)
        
        if vendor_id:
            query =query.filter_by(Vendor_Id = vendor_id)
        
        if vendor_name:
            query = query.filter_by(Vendor_name = vendor_name)
        
        if contact_number:
            query = query.filter_by(Contact_number = contact_number)
        
        if email:
            query = query.filter_by(Email = email)
            
        if address:
            query = query.filter_by(Address = address)
            
        if website:
            query = query.filter_by(Website = website)
            
        if gst_number:
            query = query.filter_by(Gst_number = gst_number)
            
            
        results = query.all()
        
        vendor_data = [
            {
            "Super_ID":v.Super_ID,
            "Vendor_Id":v.Vendor_Id,
            "Vendor_name":v.Vendor_name,
            "Contact_number":v.Contact_number,
            "Email":v.Email,
            "Address":v.Address,
            "Gst_number":v.Gst_number,
            "Website":v.Website,
            "Created_at":v.Created_at,
            "Updated_at":v.Updated_at
            }
            for v in results
        ]
        return jsonify({
            "message": "Vendor data retrieved successfully",
            "success": True,
            "data": vendor_data
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
            

#--------------Update vendor--------------------------
@vendor_bp.route("/update/vendor/<int:vendor_id>", methods=["PUT"])
def update_vendor(vendor_id):
    
    session = SessionLocal()
    
    try:
        data = request.get_json()
        super_id = data.get("Super_ID")
        vendor_name = data.get("Vendor_name")
        contact_number = data.get("Contact_number")
        email = data.get("Email")
        address = data.get("Address")
        gst_number = data.get("Gst_number")
        website=data.get("Website")
        
        vendor = session.query(Vendor).get(vendor_id)
        if not vendor:
            return jsonify({"message": "Vendor not found,", "success": False}), 404
        
        if vendor_name:
            existing_vendor_name = session.query(Vendor).filter(Vendor.Vendor_Id != vendor_id,Vendor.Vendor_name == vendor_name).first()
            if existing_vendor_name:
                return jsonify({"message": "Vendor name already exsits..", "success": False}), 400
        if email:   
            existing_vendor_email = session.query(Vendor).filter(Vendor.Vendor_Id != vendor_id,Vendor.Email == email).first()
            if existing_vendor_email:
                return jsonify({"message": "Email already exsits..", "success": False}), 400
            
        if gst_number:
            existing_gst_number = session.query(Vendor).filter(Vendor.Vendor_Id != vendor_id,Vendor.Gst_number == gst_number).first()
            if existing_gst_number:
                return jsonify({"message": "Gst NumberIs already exists..", "success": False}), 400
            
        if super_id:
            vendor.Super_ID = super_id
            
        if vendor_name:
            vendor.Vendor_name = vendor_name
            
        if contact_number:
            vendor.Contact_number = contact_number
            
        if email:
            vendor.Email = email
            
        if address:
            vendor.Address = address
        
        if gst_number:
            vendor.Gst_number = gst_number
            
        if website:
            vendor.Website = website
            
            
        vendor.Updated_at = datetime.datetime.utcnow()
        
        session.commit()
        return jsonify({
            "message": "Vendor updated successfully.",
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

        
#-------------------Delete vendor----------------------
@vendor_bp.route("/delete/vendor/<int:vendor_id>",methods=["DELETE"])
def delete_vendor(vendor_id):
    session = SessionLocal()
    
    try:
        vendor = session.query(Vendor).get(vendor_id)
        if not vendor:
            return jsonify ({"message": "vendor not found", "seccess": False}), 404
        
        session.delete(vendor)
        session.commit()
        return jsonify({ "message": "vendor deleted successfully.", "success": True }), 200
    
    except Exception as e:
        session.rollback()
        return jsonify ({"message": "Internal server error", "error": str(e), "success": False}), 500
    finally:
        session.close()
        