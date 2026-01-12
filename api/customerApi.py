from flask import Blueprint, request, jsonify
from Models.models import Customer, Vendor
from Database.database import SessionLocal

import datetime

customer_bp = Blueprint("customerApi", __name__)

@customer_bp.route("/add/customer", methods=["POST"])
def add_customer():
    session = SessionLocal()
    try:
        data = request.get_json()

        customer_code = data.get("Customer_code")
        customer_name = data.get("Customer_name")
        contact_number = data.get("Contact_number")
        email = data.get("Email")
        address = data.get("Address")
        gst_number = data.get("Gst_number")
        vendor_id = data.get("Vendor_Id")
        status = data.get("Status")


        if not customer_code or not customer_name or not vendor_id:
            return jsonify({
                "message": "Customer_code, Customer_name, and Vendor_Id are required.",
                "success": False
            }), 400

        existing_vendor = session.query(Vendor).filter_by(Vendor_Id=vendor_id).first()
        if not existing_vendor:
            return jsonify({
                "message": "Vendor not found.",
                "success": False
            }), 404

        existing_customer_code = session.query(Customer).filter_by(Customer_code=customer_code).first()
        if existing_customer_code:
            return jsonify({
                "message": "Customer code already exists.",
                "success": False
            }), 400

        if email:
            existing_email = session.query(Customer).filter_by(Email=email).first()
            if existing_email:
                return jsonify({
                    "message": "Email already exists.",
                    "success": False
                }), 400


        new_customer = Customer(
            Customer_code=customer_code,
            Customer_name=customer_name,
            Contact_number=contact_number,
            Email=email,
            Address=address,
            Gst_number=gst_number,
            Vendor_Id=vendor_id,
            Status=status
        )

        session.add(new_customer)
        session.commit()

        return jsonify({
            "message": "Customer added successfully.",
            "success": True
        }), 200

    except Exception as e:
        session.rollback()
        return jsonify({
            "message": "Internal server error occurred.",
            "error": str(e),
            "success": False
        }), 500

    finally:
        session.close()


@customer_bp.route("/get/customer", methods=["GET"])
def get_customer():
    session = SessionLocal()
    try:
        customer_code = request.args.get("Customer_code")
        customer_name = request.args.get("Customer_name")
        vendor_id = request.args.get("Vendor_Id")
        status = request.args.get("Status")

        query = session.query(Customer)

       
        if customer_code:
            query = query.filter_by(Customer_code=customer_code)
        if customer_name:
            query = query.filter(Customer.Customer_name.ilike(f"%{customer_name}%"))
        if vendor_id:
            query = query.filter_by(Vendor_Id=vendor_id)
        if status:
            query = query.filter_by(Status=status)

        results = query.all()

        customer_data = [
            {
                "Customer_Id": c.Customer_Id,
                "Customer_code": c.Customer_code,
                "Customer_name": c.Customer_name,
                "Contact_number": c.Contact_number,
                "Email": c.Email,
                "Address": c.Address,
                "Gst_number": c.Gst_number,
                "Vendor_Id": c.Vendor_Id,
                "Status": c.Status,
                "Created_at": str(c.Created_at),
                "Updated_at": str(c.Updated_at)
            }
            for c in results
        ]

        return jsonify({
            "message": "Customer data retrieved successfully.",
            "success": True,
            "data": customer_data
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



@customer_bp.route("/update/customer/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    session = SessionLocal()
    try:
        data = request.get_json()

        customer = session.query(Customer).get(customer_id)
        if not customer:
            return jsonify({"message": "Customer not found.", "success": False}), 404

        customer_code = data.get("Customer_code")
        customer_name = data.get("Customer_name")
        contact_number = data.get("Contact_number")
        email = data.get("Email")
        address = data.get("Address")
        gst_number = data.get("Gst_number")
        vendor_id = data.get("Vendor_Id")
        status = data.get("Status")

        
        if customer_code:
            existing_code = session.query(Customer).filter(
                Customer.Customer_Id != customer_id,
                Customer.Customer_code == customer_code
            ).first()
            if existing_code:
                return jsonify({"message": "Customer code already exists.", "success": False}), 400

        if email:
            existing_email = session.query(Customer).filter(
                Customer.Customer_Id != customer_id,
                Customer.Email == email
            ).first()
            if existing_email:
                return jsonify({"message": "Email already exists.", "success": False}), 400

        
        if customer_code: 
            customer.Customer_code = customer_code
        if customer_name: 
            customer.Customer_name = customer_name
        if contact_number: 
            customer.Contact_number = contact_number
        if email:
            customer.Email = email
        if address: 
            customer.Address = address
        if gst_number:
            customer.Gst_number = gst_number
        if vendor_id:
            customer.Vendor_Id = vendor_id
        if status: 
            customer.Status = status

        customer.Updated_at = datetime.datetime.utcnow()

        session.commit()

        return jsonify({
            "message": "Customer updated successfully.",
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



@customer_bp.route("/delete/customer/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    session = SessionLocal()
    try:
        customer = session.query(Customer).get(customer_id)
        if not customer:
            return jsonify({
                "message": "Customer not found.",
                "success": False
            }), 404

        session.delete(customer)
        session.commit()

        return jsonify({
            "message": "Customer deleted successfully.",
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
