from flask import Blueprint, request, jsonify
from Models.models import PartialDetails, WeighmentDetails
from Database.database import SessionLocal
import datetime

partialDarails_bp = Blueprint("partialDetailsApi", __name__)

@partialDarails_bp.route("/add/partialdetails", methods=["POST"])
def add_partialDetails():
    session = SessionLocal()
    
    try:
        data = request.get_json()
        
        weighment_id = data.get("Weighment_Id")
        product_name = data.get("Product_name")
        net_weight = data.get("Net_weight")
        
        if not weighment_id:
            return jsonify({"message": "Weighment Id is required.", "success": False}), 400
        
        if not product_name:
            return jsonify({"message": "Product name is required.", "success": False}), 400
        
        weighment = session.query(WeighmentDetails).filter_by(Weighment_Id=weighment_id).first()
        if not weighment:
            return jsonify({"message": "Weighment record is not found.", "success": False}), 404
        
        new_partial = PartialDetails(
            
            Weighment_Id=weighment_id,
            Product_name=product_name,
            Net_weight=net_weight
        )
        
        session.add(new_partial)
        session.commit()
        return jsonify({
            "message": "Partial Details added successfully.",
            "success": True,
            "data": {"Partial_Id": new_partial.Partial_Id}
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


@partialDarails_bp.route("/get/partialDetails", methods=["GET"])
def get_partial_details():
    session = SessionLocal()
    
    try:
        
        partial_id = request.args.get("Partial_Id")
        weighment_id = request.args.get("Weighment_Id")
        
        query = session.query(PartialDetails)
        
        if partial_id:
            query = query.filter_by(Partial_Id = partial_id)
            
        if weighment_id:
            query = query.filter_by(Weighment_Id = weighment_id)
            
        results = query.all()
        
        if not results:
            return jsonify({"message": "no records found.", "success": False}), 404
        
        partial_data = [
            {
                "Partial_Id": p.Partial_Id,
                "Weighment_Id": p.Weighment_Id,
                "Product_name": p.Product_name,
                "Net_weight": str(p.Net_weight) if p.Net_weight else None
            }
            for p in results
        ]
        
        return jsonify({
            "message": "Partial Details retrieved successfully.",
            "success": True,
            "data": partial_data
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
        

@partialDarails_bp.route("/update/partialDetails/<int:partial_id>", methods=["PUT"])
def update_partial_details(partial_id):
    session = SessionLocal()
    
    try:
        data = request.get_json()
        
        partial = session.query(PartialDetails).filter_by(Partial_Id=partial_id).first()
        if not partial:
            return jsonify({"message": "Partial record not found.", "success": False}), 404
        
        if "Weighment_Id" in data:
            weighment = session.query(WeighmentDetails).filter_by(Weighment_Id=data["Weighment_Id"]).first()
            if not weighment:
                return jsonify({"message": "Weighment record not found.", "success": False}), 404
            partial.Weighment_Id = data["Weighment_Id"]
            
        if "Product_name" in data:
            partial.Product_name = data["Product_name"]
            
        if "Net_weight" in data:
            partial.Net_weight = data["Net_weight"]
            
        session.commit()
        return jsonify({
            "message": "Weighment Details Updated successfully",
            "success": True,
            "data": {"Partial_Id": partial.Partial_Id}
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
        

@partialDarails_bp.route("/delete/partialDetails/<int:partial_id>", methods=["DELETE"])
def delete_partial_Details(partial_id):
    session = SessionLocal()
    
    try:
        
        partial = session.query(PartialDetails).filter_by(Partial_Id = partial_id).first()
        
        if not partial:
            return jsonify({"message": "Partial record not found.", "success": False}), 404
        
        session.delete(partial)
        session.commit()
        
        return jsonify({
            "message": "Partial Details deleted successfully.",
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