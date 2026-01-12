from flask import Blueprint, request, jsonify
from Models.models import Machine, Weighbridge
from Database.database import SessionLocal
import datetime

weighbridge_bp = Blueprint("weighBridgeApi", __name__)

# add_weighbridge ------------------------
@weighbridge_bp.route("/add/weighbridge", methods=["POST"])
def generate_bridge():
    
    session = SessionLocal()
    try:
        data = request.get_json()
        machine_id = data.get("Machine_Id")
        serial_no = data.get("Serial_no")
        port = data.get("Port")
        baud_rate = data.get("Baud_rate")
        data_bit = data.get("Data_bit")
        stop_bit = data.get("Stop_bit")
        party = data.get("Party")
        
        if not machine_id or not serial_no or not data_bit or not stop_bit or not party:
            return jsonify ({
               "meaaage": "Machine_Id, Serial_no, data_bit, Stop_bit and Party are required.",
               "success": False 
            }), 400
            
        existing_machine = session.query(Machine).filter_by(Machine_Id=machine_id).first()
        if not existing_machine:
            return jsonify({
                "message": "Machine not found.", "success": False
            }), 400
            
         # Check serial number duplicate
        if serial_no and session.query(Weighbridge).filter_by(Serial_no=serial_no).first():
            return jsonify({"message": "Serial number already exists.", "success": False}), 400

        # Create new weighbridge record
        new_weighbridge = Weighbridge (
            Machine_Id = machine_id,
            Serial_no = serial_no,
            Port = port,
            Baud_rate = baud_rate,
            Data_bit = data_bit,
            Stop_bit = stop_bit,
            Party = party
        )
        
        session.add(new_weighbridge)
        session.commit()
        
        return jsonify ({
            "message" : "Weighbridge added successfully",
            "success" : True
        }), 200
        
    except Exception as e: 
        session.rollback()
        return jsonify({
            "message": "Internal server error.",
            "error": str(e),
            "sueecss": False
        }), 500
    finally:
        session.close()
        
        
@weighbridge_bp.route("/get/weighbridge", methods=["GET"])
def get_weighbridge():
    
    session = SessionLocal()
    
    try:
        machine_id = request.args.get("Machine_Id")
        serial_no = request.args.get("Serial_no")
        port = request.args.get("Port")
        baud_rate = request.args.get("Baud_rate")
        data_bit = request.args.get("Data_bit")
        stop_bit = request.args.get("Stop_bit")
        party = request.args.get("Party")
        
        query = session.query(Weighbridge)
        
        if machine_id:
            query = query.filter_by(Machine_Id=machine_id)
            
        if serial_no:
            query = query.filter_by(Serial_no=serial_no)
            
        if port:
            query = query.filter_by(Port=port)
            
        if baud_rate:
            query = query.filter_by(Baud_rate=baud_rate)
            
        if data_bit:
            query = query.filter_by(Data_bit=data_bit)
            
        if stop_bit:
            query = query.filter_by(Stop_bit=stop_bit)
            
        if party:
            query = query.filter_by(Party=party)
            
        results = query.all()
        
        Weighbridge_data = [
            {
                "Weighbridge_Id" : w.Weighbridge_Id,
                "Machine_Id" : w.Machine_Id,
                "Serial_no" : w.Serial_no,
                "Port" : w.Port,
                "Baud_rate" : w.Baud_rate,
                "Data_bit" : w.Data_bit,
                "Stop_bit" : w.Stop_bit,
                "Party" : w.Party,
                "Created_at" : str(w.Created_at),
                "Updated_at" : str(w.Updated_at),
            }
            for w in results
        ]
         
        session.commit()
        return jsonify ({
            "message" : "Weighbridge data retrieved successfully.",
            "success" : True,
            "data" : Weighbridge_data,
        }), 200
        
    except Exception as e:
        session.rollback()
        return jsonify({
            "message" : "Internal server error.",
            "error" : str(e),
            "success": False
        }), 500
    finally:
        session.close()
        
        
@weighbridge_bp.route("/update/weighbridge/<int:weighbridge_id>", methods=["PUT"])
def update_weighbridge(weighbridge_id):
    
    session = SessionLocal()
    
    try:
        
        data = request.get_json()
        serial_no = data.get("Serial_no")
        port = data.get("Port")
        baud_rate = data.get("Baud_rate")
        data_bit = data.get("Data_bit")
        stop_bit = data.get("Stop_bit")
        party = data.get("Party")
        
        weighbridge = session.query(Weighbridge).get(weighbridge_id)
        if not weighbridge:
            return jsonify ({ "message" : "Weighbridge not found.", "success" : False }), 404
        
        # Serial number duplicate check
        if serial_no:
            exists = session.query(Weighbridge).filter(Weighbridge.Weighbridge_Id != weighbridge_id, Weighbridge.Serial_no == serial_no).first()
            
            if exists:
                return jsonify ({ "message": "Serial number already exists.", "success": False }), 400
            
        if serial_no:
            weighbridge.Serial_no = serial_no
            
        if port:
            weighbridge.Port = port
            
        if baud_rate:
            weighbridge.Baud_rate = baud_rate
            
        if data_bit:
            weighbridge.Data_bit = data_bit
            
        if stop_bit:
            weighbridge.Stop_bit = stop_bit
            
        if party:
            weighbridge.Party = party
            
        weighbridge.Updated_at = datetime.datetime.utcnow()
        
        session.commit()
        return jsonify ({ "message" : "Weighbridge updated successfullys.", "success" : True }), 200
    
    except Exception as e:
        session.rollback()
        return jsonify ({
            "message" : "Internal server error.",
            "error" : str(e),
            "success" : False
        }), 500
    finally:
        session.close()
        
        
        
@weighbridge_bp.route("/delete/weighbridge/<int:weighbridge_id>", methods=["DELETE"])
def delete_weighbridge(weighbridge_id):
    
    session = SessionLocal()
    
    try:
        weighbridge = session.query(Weighbridge).filter(Weighbridge.Weighbridge_Id == weighbridge_id).first()
        
        if not weighbridge: 
            return jsonify({
                "massage" : "WeighBridge not found",
                "success" : False
            }), 404
            
        session.delete(weighbridge)
        session.commit()
        
        return jsonify({ "message" : "Weighbridge deleted successfully.", "success" : True }), 200
    
    except Exception as e:
        session.rollback()
        return jsonify({
            "message" : "Internal server error.",
            "error" : str(e),
            "success": False
        }), 500
        
    finally:
        session.close()
        