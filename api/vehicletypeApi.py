from flask import Blueprint, request, jsonify
from Models.models import VehicleType, Vendor, Customer
from Database.database import SessionLocal
import datetime


vehicletype_bp = Blueprint("vehicleApi", __name__)

@vehicletype_bp.route("/add/vehicle", methods=["POST"])
def create_vehicle():
    sesssion = SessionLocal()
    
    try:
        data = request.get_json()
        
        vendor_id = data.get("Vendor_Id")
        customer_id = data.get("Customer_Id")
        vehicle_tpye = data.get("Vehicle_type")
        tare_weight = data.get("Tare_weight")
        
        if not vendor_id or not vehicle_tpye or not tare_weight:
            return jsonify({
                "message": "Vendor Id, Vehicle type and Tare weight are required,",
                "success": False
            }), 400
            
        vendor = sesssion.query(Vendor).filter_by(Vendor_Id = vendor_id).first()
        if not vendor:
            return jsonify({
                "message": "Vendor not found.",
                "success": False
            }), 404

        # customer = sesssion.query(Customer).filter_by(Customer_Id = customer_id).first()
        # if not customer:
        #     return jsonify({
        #         "message": "Customer not found.",
        #         "success": False
        #     }), 404
        
        new_vehicle = VehicleType(
            
            Vendor_Id = vendor_id,
            Customer_Id = customer_id,
            Vehicle_type = vehicle_tpye,
            Tare_weight = tare_weight
        )
        
        sesssion.add(new_vehicle)
        sesssion.commit()
        
        return jsonify({
            "message": "Vehicle added successfully",
            "success": True
        }), 200
        
    except Exception as e:
        sesssion.rollback()
        return jsonify({
            "message": "Internal server error.",
            "error": str(e),
            "success": False
        }), 500
        
    finally:
        sesssion.close()
        
        
@vehicletype_bp.route("/get/vehicle", methods=["GET"])
def get_vehicle():
    session = SessionLocal()
    
    try:
        vehicle_id = request.args.get("Vehicle_Id")
        vendor_id = request.args.get("Vendor_Id")
        customer_id = request.args.get("Customer_Id")
        vehicle_type = request.args.get("Vehicle_type")
        tare_weight = request.args.get("tare_weight")
        
        query = session.query(VehicleType)
        
        if vehicle_id:
            query = query.filter_by(Vehicle_Id = vehicle_id)
            
        if vendor_id:
            query = query.filter_by(Vendor_Id = vendor_id)
        
        if customer_id:
            query = query.filter_by(Customer_Id = customer_id)
            
        if vehicle_type:
            query = query.filter_by(Vehicle_type = vehicle_type)
            
        if tare_weight:
            query = query.filter(Tare_weight = tare_weight)
            
        results = query.all()
        
        vehicle_data = [
            {
                "Vehicle_Id": v.Vehicle_Id,
                "Vendor_Id": v.Vendor_Id,
                "Customer_Id": v.Customer_Id,
                "Vehicle_type": v.Vehicle_type,
                "Tare_weight": str(v.Tare_weight),
                "Created_at": str(v.Created_at),
                "Updated_at": str(v.Updated_at)
            }
            for v in results
        ]
        
        return jsonify({
            "message": "Vehicle data retrieved successfully.",
            "success": True,
            "data": vehicle_data
        }), 200
        
    except Exception as e:
        session.rollback()
        return jsonify({
            "message": "Internal Server error.",
            "error": str(e),
            "success": False
        })
    finally:
        session.close()
        
        
        

@vehicletype_bp.route("/update/vehicle/<int:vehicle_id>", methods=["PUT"])
def update_vehicle(vehicle_id):
    session = SessionLocal()
    try:
        data = request.get_json()

        vehicle = session.query(VehicleType).filter(VehicleType.Vehicle_Id == vehicle_id).first()
        if not vehicle:
            return jsonify({"message": "Vehicle not found.", "success": False}), 404

        vendor_id = data.get("Vendor_Id")
        customer_id = data.get("Customer_Id")
        vehicle_type = data.get("Vehicle_type")
        tare_weight = data.get("Tare_weight")

        if vendor_id:
            vendor = session.query(Vendor).get(vendor_id)
            if not vendor:
                return jsonify({"message": "Vendor not found.", "success": False}), 404
            vehicle.Vendor_Id = vendor_id

        if customer_id:
            customer = session.query(Customer).get(customer_id)
            if not customer:
                return jsonify({"message": "Customer not found.", "success": False}), 404
            vehicle.Customer_Id = customer_id
            
        # if vehicle_type:
        #     customer = session.query(Customer).get(vehicle_type)
        #     if not customer:
        #         return jsonify({"message": "Vehicle type not found.", "success": False}), 404
        #     vehicle.Vehicle_type = vehicle_type

        if vehicle_type:
            vehicle.Vehicle_type = vehicle_type
        if tare_weight:
            vehicle.Tare_weight = tare_weight

        vehicle.Updated_at = datetime.datetime.utcnow()

        session.commit()
        session.refresh(vehicle)

        return jsonify({
            "message": "Vehicle updated successfully.",
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


@vehicletype_bp.route("/delete/vehicle/<int:vehicle_id>", methods=["DELETE"])
def delete_vehicle(vehicle_id):
    session = SessionLocal()
    
    try:
        vehicle = session.query(VehicleType).filter(VehicleType.Vehicle_Id == vehicle_id).first()
        
        if not vehicle:
            return jsonify({
                "message": "Vehicle not found.",
                "success": False
            }), 404
            
        session.delete(vehicle)
        session.commit()
        return jsonify({
            "message": "Vehicle deleted successfully.",
            "success": True
        }), 200
        
    except Exception as e:
        session.rollback()
        return jsonify({
            "message": "Internal derver error.",
            "error": str(e),
            "success": False
        }), 500
    finally:
        session.close()

