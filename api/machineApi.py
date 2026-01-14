from flask import Blueprint, request, jsonify
from Models.models import Machine, Vendor
from Database.database import SessionLocal
import datetime


machine_bp = Blueprint("machineApi", __name__)

# Add_machine--------------------------
@machine_bp.route("/add/machine", methods=["POST"])
def generate_machine_id():
    
    session = SessionLocal()
    try:
        data = request.get_json()
        vendor_id = data.get("Vendor_Id")
        machine_name = data.get("Machine_name")
        password = data.get("Password")
        machine_mac = data.get("Machine_mac")
        machine_model = data.get("Machine_model")
        capacity_ton = data.get("Capacity_ton")
        last_service_date = data.get("Last_service_date")
        status = data.get("Status")
        machine_type = data.get("Machine_type")
        machine_location = data.get("Machine_location")
        
        existing_vendor = session.query(Vendor).filter_by(Vendor_Id = vendor_id).first()
        if not existing_vendor:
            return jsonify({
                "message": "vendor not found.",
                "success": False
            }), 400
            
        print()
            
        if not vendor_id or not machine_name or not machine_mac or not machine_model or not capacity_ton or not last_service_date or not machine_location:
            return jsonify({
                "message": "Vendor Id, Machine name, Machine mac, Machine model, Capacity ton, Last service date and machine location are required.",
                "success": False
            }), 400
            
        if password and session.query(Machine).filter_by(Password=password).first():
            return jsonify({"message": "Password already exists", "success": False}), 400
            
        existing_machine_name = session.query(Machine).filter_by(Machine_name=machine_name).first()
        if existing_machine_name:
            return jsonify({
                "message": "Machine name already exists.",
                "success": False
            }), 400
            
        # machine_id = generate_machine_id(session, existing_vendor.Vendor_name)
        
        new_machine = Machine(
            Vendor_Id = vendor_id,
            Machine_name = machine_name,
            Password = password,
            Machine_mac = machine_mac,
            Machine_model = machine_model,
            Capacity_ton = capacity_ton,
            Last_service_date = last_service_date,
            Machine_type = machine_type,
            Machine_location = machine_location,
        )
        session.add(new_machine)
        session.commit()
        return jsonify({
            "message": "Machine added successfully.",
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

        
# Get_machine--------------------------       
@machine_bp.route("/get/machine", methods=["GET"])

def get_machine():
    
    session = SessionLocal()
    
    try:
        vendor_id = request.args.get("Vendor_Id")
        machine_name = request.args.get("Machine_name")
        machine_mac = request.args.get("Machine_mac")
        machine_model = request.args.get("Machine_model")
        capacity_ton = request.args.get("Capacity_ton")
        last_service_date = request.args.get("Last_service_date")
        machine_type = request.args.get("Machine_type")
        machine_location = request.args.get("Machine_location")
        status = request.args.get("Status")
        query = session.query(Machine)
        
        if vendor_id:
            query = query.filter_by(Vendor_Id = vendor_id)
            
        if machine_name:
            query = query.filter_by(Machine_name = machine_name)
            
        if machine_mac:
            query = query.filter_by(Machine_mac = machine_mac)
            
        if machine_model:
            query = query.filter_by(Machine_model = machine_model)
            
        if capacity_ton:
            query = query.filter_by(Capacity_ton = capacity_ton)
            
        if last_service_date:
            query = query.filter_by(Last_service_date = last_service_date)
            
        if machine_type:
            query = query.filter_by(Machine_type = machine_type)
            
        if machine_location:
            query = query.filter_by(Machine_location = machine_location)
            
        if status:
            query = query.filter_by(Status = status)
            
        results = query.all()
        
        machine_data = [
            {
                "Machine_Id": m.Machine_Id,
                "Vendor_Id": m.Vendor_Id,
                "Machine_name": m.Machine_name,
                "Machine_mac": m.Machine_mac,
                "Machine_model": m.Machine_model,
                "Capacity_ton": m.Capacity_ton,
                "Last_service_date": str(m.Last_service_date),
                "Machine_type": m.Machine_type,
                "Machine_location": m.Machine_location,
                "Status": m.Status,
                "Created_at": str(m.Created_at),
                "Updated_at": str(m.Updated_at)
            }
            for m in results
        ]
        return jsonify({
            "message": "machine data retrieved successfully",
            "success": True,
            "data": machine_data
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


# Update_machine--------------------------
@machine_bp.route("/update/machine/<int:machine_id>", methods=["PUT"])
def update_machine(machine_id):
    
    session = SessionLocal()
    
    try:
        data = request.get_json()
        machine_name = data.get("Machine_name")
        password = data.get("Password")
        machine_mac = data.get("Machine_mac")
        machine_model = data.get("Machine_model")
        capacity_ton = data.get("Capacity_ton")
        last_service_date = data.get("Last_service_date")
        machine_type = data.get("Machine_type")
        machine_location = data.get("Machine_location")
        status = data.get("Status")
        
        machine = session.query(Machine).get(machine_id)
        if not machine:
            return jsonify({"message": "Machine not found", "success": False}), 404
        
        existing_machine_name = session.query(Machine).filter(Machine.Machine_Id != machine_name,Machine.Machine_Id == machine_name).first()
        if existing_machine_name:
            return jsonify({"message": "Machine name already exit..", "success": False}), 400
        
        if password and session.query(Machine).filter(Machine.Password == password, Machine.Password != password).first():
            return jsonify({"message": "Passwoer already exists.", "seccess": False}), 400
        
        if machine_name:
            machine.Machine_name = machine_name
            
        if password:
            machine.Password = password
            
        if machine_mac:
            machine.Machine_mac = machine_mac
            
        if machine_model:
            machine.Machine_model = machine_model
            
        if capacity_ton:
            machine.Capacity_ton = capacity_ton
            
        if last_service_date:
            machine.Last_service_date = last_service_date
            
        if machine_type:
            machine.Machine_type = machine_type
            
        if machine_location:
            machine.Machine_location = machine_location
            
        if status:
            machine.Status = status
            
        machine.Updated_at = datetime.datetime.utcnow()
        
        session.commit()
        return jsonify({
            "message": "Machine updated successfully.",
            "success": True
        }), 200
        
    except Exception as e:
        session.rollback()
        return jsonify({
            "message": "Internal server error.",
            "error": str(e),
            "success": False
        }), 500


# Delete_machine--------------------------
@machine_bp.route("/delete/machine/<int:machine_id>", methods=["DELETE"])
def delete_machine(machine_id):
    
    session = SessionLocal()
    
    try:
        machine = session.query(Machine).filter(Machine.Machine_Id == machine_id).first()
        
        if not machine:
            return jsonify({
                "message": "machine not found",
                "success": False
            }), 404
        session.delete(machine)
        session.commit()
        return jsonify({
            "message": "machine deleted successfully",
            "success": True
        }), 200
    except Exception as e:
        session.rollback()
        return jsonify({
            "message": "Internal server error.",
            "error":str(e),
            "success": False
            }), 500
    finally:
        session.close()
        