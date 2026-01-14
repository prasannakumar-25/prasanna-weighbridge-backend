from flask import Blueprint, request, jsonify
from Models.models import Standardload, Vendor, Machine, VehicleType
from Database.database import SessionLocal
import datetime

standardload_bp = Blueprint("standardloadApi", __name__)


@standardload_bp.route("/add/standardload", methods=["POST"])
def add_standardload():
    session = SessionLocal()
    try:
        data = request.get_json()

        vendor_id = data.get("Vendor_Id")
        machine_id = data.get("Machine_Id")
        vehicle_id = data.get("Vehicle_Id")

        serial_no = data.get("Serial_No")
        contact_number = data.get("Contact_Number")
        vehicle_no = data.get("Vehicel_No")
        vehicle_type = data.get("Vehicle_Type")
        location = data.get("Location")
        material = data.get("Material")
        destination_place = data.get("Destination_Place")
        supplier = data.get("Supplier")
        driver_name = data.get("Driver_Name")
        product = data.get("Product")
        load_type = data.get("Load_Type")
        payment_mode = data.get("Payment_Mode")


        if not all([
            contact_number, vehicle_no, vehicle_type, location,
            material, driver_name, load_type, payment_mode
        ]):
            return jsonify({
                "message": "Required fields are missing.",
                "success": False
            }), 400


        if vendor_id:
            vendor = session.query(Vendor).filter_by(Vendor_Id=vendor_id).first()
            if not vendor:
                return jsonify({"message": "Vendor not found.", "success": False}), 400

        if machine_id:
            machine = session.query(Machine).filter_by(Machine_Id=machine_id).first()
            if not machine:
                return jsonify({"message": "Machine not found.", "success": False}), 400
            
        if vehicle_id:
            vehicle = session.query(VehicleType).filter_by(Vehicle_Id=vehicle_id).first()
            if not vehicle:
                return jsonify({"message": "Vehicle not found.", "success": False}), 400

        new_standardload = Standardload(
            Vendor_Id=vendor_id,
            Machine_Id=machine_id,
            Vehicle_Id=vehicle_id,
            Serial_No=serial_no,
            Contact_Number=contact_number,
            Vehicel_No=vehicle_no,
            Vehicle_Type=vehicle_type,
            Location=location,
            Material=material,
            Destination_Place=destination_place,
            Supplier=supplier,
            Driver_Name=driver_name,
            Product=product,
            Load_Type=load_type,
            Payment_Mode=payment_mode
        )

        session.add(new_standardload)
        session.commit()

        return jsonify({
            "message": "Standard load created successfully.",
            "success": True
        }), 201

    except Exception as e:
        session.rollback()
        return jsonify({
            "message": "Internal server error.",
            "error": str(e),
            "success": False
        }), 500
    finally:
        session.close()


@standardload_bp.route("/get/standardload", methods=["GET"])
def get_standardload():
    session = SessionLocal()
    try:
        vendor_id = request.args.get("Vendor_Id")
        machine_id = request.args.get("Machine_Id")
        vehicle_no = request.args.get("Vehicel_No")
        load_type = request.args.get("Load_Type")
        payment_mode = request.args.get("Payment_Mode")

        query = session.query(Standardload)

        if vendor_id:
            query = query.filter_by(Vendor_Id=vendor_id)
        if machine_id:
            query = query.filter_by(Machine_Id=machine_id)
        if vehicle_no:
            query = query.filter_by(Vehicel_No=vehicle_no)
        if load_type:
            query = query.filter_by(Load_Type=load_type)
        if payment_mode:
            query = query.filter_by(Payment_Mode=payment_mode)

        results = query.all()

        data = [
            {
                "Standard_Id": s.Standard_Id,
                "Vendor_Id": s.Vendor_Id,
                "Machine_Id": s.Machine_Id,
                "Vehicle_Id": s.Vehicle_Id,
                "Serial_No": s.Serial_No,
                "Contact_Number": s.Contact_Number,
                "Vehicel_No": s.Vehicel_No,
                "Vehicle_Type": s.Vehicle_Type,
                "Location": s.Location,
                "Material": s.Material,
                "Destination_Place": s.Destination_Place,
                "Supplier": s.Supplier,
                "Driver_Name": s.Driver_Name,
                "Product": s.Product,
                "Load_Type": s.Load_Type,
                "Payment_Mode": s.Payment_Mode,
                "Created_at": str(s.Created_at),
                "Updated_at": str(s.Updated_at)
            }
            for s in results
        ]

        return jsonify({
            "message": "Standard load data retrieved successfully.",
            "success": True,
            "data": data
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



@standardload_bp.route("/update/standardload/<int:standard_id>", methods=["PUT"])
def update_standardload(standard_id):
    session = SessionLocal()
    try:
        data = request.get_json()
        standardload = session.get(Standardload, standard_id)

        if not standardload:
            return jsonify({"message": "Standard load not found.", "success": False}), 404

        for field in [
            "Serial_No", "Contact_Number", "Vehicel_No", "Vehicle_Type",
            "Location", "Material", "Destination_Place", "Supplier",
            "Driver_Name", "Product", "Load_Type", "Payment_Mode"
        ]:
            if data.get(field) is not None:
                setattr(standardload, field, data.get(field))

        standardload.Updated_at = datetime.datetime.utcnow()
        session.commit()

        return jsonify({
            "message": "Standard load updated successfully.",
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


@standardload_bp.route("/delete/standardload/<int:standard_id>", methods=["DELETE"])
def delete_standardload(standard_id):
    session = SessionLocal()
    try:
        standardload = session.query(Standardload).filter(Standardload.Standard_Id == standard_id).first()

        if not standardload:
            return jsonify({
                "message": "Standard load not found.",
                "success": False
            }), 404

        session.delete(standardload)
        session.commit()

        return jsonify({
            "message": "Standard load deleted successfully.",
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
