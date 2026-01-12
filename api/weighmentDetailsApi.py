from flask import Blueprint, request, jsonify
from Models.models import WeighmentDetails, Vendor, Machine, Customer, VehicleType, User
from Database.database import SessionLocal
import datetime

Weighment_Details_bp = Blueprint("weighmentDetailsApi", __name__)


@Weighment_Details_bp.route("/add/weighmentDetails", methods=["POST"])
def add_weighmentDetails():
    session = SessionLocal()
    
    try:
        data = request.get_json()
        
        
        ticket_no = data.get("Ticket_no")
        vendor_id = data.get("Vendor_Id")
        machine_id = data.get("Machine_Id")
        created_by = data.get("Created_by")
        
        #required field check
        if not ticket_no:
            return jsonify({"message": "Ticket number are required.", "success": False}), 400
        
        if not vendor_id:
            return jsonify({"message": "Vendor Id is required.", "success": False}), 400
        
        if not machine_id:
            return jsonify({"message": "Machine Id is required.", "success": False}), 400
        
        if not created_by:
            return jsonify({"message": "created by (User Id) is required.", "success": False}), 400
        
        existing_ticket = session.query(WeighmentDetails).filter_by(Ticket_no=ticket_no).first()
        if existing_ticket:
            return jsonify({"message": "Ticket number already exists.", "success": False}), 400
        
        valid_weighment_types = ['Standard', 'Partial']
        if data.get("Weighment_type") not in valid_weighment_types:
            return jsonify({"message": f"Invalid Weighment_type. Allowed: {valid_weighment_types}", "success": False}), 400
        
        # foreign keys
        vendor = session.query(Vendor).filter_by(Vendor_Id=vendor_id).first()
        if not vendor:
            return jsonify({"message": "Vendor not found.", "success": False}), 404
        
        machine = session.query(Machine).filter_by(Machine_Id=machine_id).first()
        if not machine:
            return jsonify({"message": "Machine not found.", "success": False}), 404
        
        user = session.query(User).filter_by(User_Id=created_by).first()
        if not user:
            return jsonify({"message": "User not found.", "success":  False}), 404
        
        new_weighment = WeighmentDetails(
            
            Ticket_no=ticket_no,
            Vendor_Id=vendor_id,
            Machine_Id=machine_id,
            Customer_Id=data.get("Customer_Id"),
            Vehicle_Id=data.get("Vehicle_Id"),
            Weighment_type=data.get("Weighment_type"),
            First_weight=data.get("First_weight"),
            Second_weight=data.get("Second_weight"),
            Net_weight=data.get("Net_weight"),
            Weight_unit=data.get("Weight_unit"),
            Sequence_no=data.get("Sequence_no"),
            Image_path=data.get("Image_path"),
            Image_type=data.get("Image_type"),
            Status="Pending",
            Created_by=created_by,
            Created_at=data.get("Created_at"),
            Completed_at=data.get("Completed_at")
        )
        
        
        session.add(new_weighment)
        session.commit()
        return jsonify({
            "message": "Weighment details added successfully.",
            "success": True,
            "data": {"Weighment_Id": new_weighment.Weighment_Id} 
            })
    
    except Exception as e:
        session.rollback()
        return jsonify({
            "message": "Internal server error.",
            "error": str(e),
            "success": False
        }), 500
    finally:
        session.close()
        
    

@Weighment_Details_bp.route("/get/weighment", methods=["GET"])
def get_weighment_detail():
    session = SessionLocal()
    
    try:
        
        weighment_id = request.args.get("Weighment_Id")
        vendor_id = request.args.get("Vendor_Id")
        machine_id = request.args.get("Machine_Id")
        ticket_no = request.args.get("Ticket_no")
        
        query = session.query(WeighmentDetails)
        
        if weighment_id:
            query = query.filter_by(Weighment_Id=weighment_id)
            
        if vendor_id:
            query = query.filter_by(Vendor_Id=vendor_id)
        
        if machine_id:
            query = query.filter_by(Machine_Id=machine_id)
            
        if ticket_no:
            query = query.filter_by(Ticket_no=ticket_no)
            
        results = query.all()
        
        weighment_data = [
            {
                "Weighment_Id": w.Weighment_Id,
                "Ticket_no": w.Ticket_no,
                "Vendor_Id": w.Vendor_Id,
                "Machine_Id": w.Machine_Id,
                "Customer_Id": w.Customer_Id,
                "Vehicle_Id": w.Vehicle_Id,
                "Weighment_type": w.Weighment_type,
                "First_weight": str(w.First_weight) if w.First_weight else None,
                "Second_weight": str(w.Second_weight) if w.Second_weight else None,
                "Net_weight": str(w.Net_weight) if w.Net_weight else None,
                "Weight_unit": w.Weight_unit,
                "Sequence_no": w.Sequence_no,
                "Image_path": w.Image_path,
                "Image_type": w.Image_type,
                "Status": w.Status,
                "Created_by": w.Created_by,
                "Created_at": w.Created_at,
                "Completed_at": w.Completed_at
            }
            for w in results
        ]
        
        return jsonify({
            "message": "Weighment Details retrieved successfully.",
            "success": True,
            "data": weighment_data
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
    

@Weighment_Details_bp.route("/update/weighment/<int:weighment_id>", methods=["PUT"])
def update_weighment_Details(weighment_id):
    session = SessionLocal()
    
    try:    
        data = request.get_json()
        
        weighment = session.query(WeighmentDetails).filter(WeighmentDetails.Weighment_Id == weighment_id).first()
        if not weighment:
            return jsonify({"message": "weighment record not found.", "success": False}), 404
            
        
        if "Ticket_no" in data:
            existing = session.query(WeighmentDetails).filter(
                WeighmentDetails.Ticket_no == data["Ticket_no"],
                WeighmentDetails.Weighment_Id != weighment_id
            ).first()
            if existing:
                return jsonify({"message": "Ticket number already exists.", "success": False}), 400
        
            
        fields_to_update = [
            "Ticket_no", "Vendor_Id", "Machine_Id", "Customer_Id", "Vehicle_Id",
            "Weighment_type", "First_weight", "Second_weight", "Net_weight",
            "Weight_unit", "Sequence_no", "Image_path", "Image_type",
            "Status", "Completed_at"
        ]
        
        for field in fields_to_update:
            if field in data and data[field] is not None:
                setattr(weighment, field, data[field])
                
        if "Vendor_Id" in data:
            vendor = session.query(Vendor).filter_by(Vendor_Id=data["Vendor_Id"]).first()
            if not vendor:
                return jsonify({"message": "Vendor not found.", "success": False }), 404
            
        if "Machine_Id" in data:
            machine = session.query(Machine).filter_by(Machine_Id=data["Machine_Id"]).first()
            if not machine:
                return jsonify({"messsage": "Machine not found.", "success": False }), 404
            
        if "Created_by" in data:
            user = session.query(User).filter_by(User_Id=data["Created_by"]).first()
            if not user:
                return jsonify({"message": "User not found.", "success": False }), 404
            
        weighment.Updated_at = datetime.datetime.utcnow()
        
        session.commit()
        return jsonify({
            "message": "Weighment Details updated successfully.", 
            "success": True,
            "data": {"Weighment_Id": weighment.Weighment_Id}
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
        
        
        
@Weighment_Details_bp.route("/delete/weightDetails/<int:weighment_id>", methods=["DELETE"])
def delete_weighmentDetails(weighment_id):
    session = SessionLocal()
    
    try:
        weighment = session.query(WeighmentDetails).filter_by(Weighment_Id = weighment_id).first()
        
        if not weighment:
            return jsonify({
                "message": "Weight recoard is not found.",
                "success": False
            }), 404
            
        session.delete(weighment)
        session.commit()
        return jsonify({
            "message": "Weighment Details deleted successfully.",
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
        