from flask import Blueprint, request, jsonify
from Models.models import IPCamera, Machine
from Database.database import SessionLocal
from datetime import datetime, date

ipcamera_bp = Blueprint("ipCameraApi", __name__)

@ipcamera_bp.route("/add/ipcamera", methods=["POST"])
def add_ipcamera():
    session = SessionLocal()
    
    try:
        data = request.get_json()
        
        machine_id = data.get("Machine_Id")
        camera_name = data.get("Camera_name")
        ip_address = data.get("IP_address")
        rtsp_url = data.get("RTSP_URL")
        http_url = data.get("HTTP_URL")
        username = data.get("Username")
        password = data.get("Password")
        
        mac_address = data.get("Mac_address")
        # model = data.get("Model")
        status = data.get("Status")
        location = data.get("Location")
        installed_date_str = data.get("Installed_date")

        if installed_date_str:
            try:
                installed_date = datetime.strptime(installed_date_str, "%Y-%m-%d").date()
            except ValueError:
                return jsonify({
                    "message": "Installed_date must be in YYYY-MM-DD format",
                    "success": False
                }), 400
        else:
            installed_date = date.today()

        
        # Check Machine exists
        if machine_id:
            existing_machine = session.query(Machine).filter_by(Machine_Id=machine_id).first()
            if not existing_machine:
                return jsonify ({ "message": "Machine not found", "success" : False}), 400
            
        # Required fields validation
        if not camera_name or not ip_address or not password:
            return jsonify ({ "message" : "Camere_name, IP_address, password are required", "success" : False}), 400
        
    
        existing_camara_name = session.query(IPCamera).filter_by(Camera_name=camera_name). first()
        if existing_camara_name:
            return jsonify({ "message" : "Camera Name already exists.", "success" : False }), 400
        
        existing_ip = session.query(IPCamera).filter_by(IP_address=ip_address).first()
        if existing_ip:
            return jsonify({ "message" : "IP address already exists.", "success": False }), 400
        
        new_camera = IPCamera (
            Machine_Id = machine_id,
            Camera_name = camera_name,
            IP_address = ip_address,
            RTSP_URL = rtsp_url,
            HTTP_URL = http_url,
            Username = username,
            Password = password or "",
            Mac_address = mac_address,
            # Model = model,
            Status = status if status else "Offline",
            Location = location,
            Installed_date = installed_date,
        )
        
        print("new-cameras",new_camera)
        
        session.add(new_camera)
        session.commit()
        
        return jsonify({
            "message" : "IP camera added successfully",
            "success" : True
        }), 200
        
    except Exception as e:
        session.rollback()
        return jsonify({ 
          "message" : "Internal server error", 
          "error": str(e),
          "success" : False
        })
    finally:
        session.close() 
        
    
@ipcamera_bp.route("/get/ipcamera", methods=["GET"])
def get_ipcamera():
    session = SessionLocal()
    
    try:
        camera_id = request.args.get("Camera_id")
        machine_id = request.args.get("Machine_Id")
        camera_name = request.args.get("Camera_name")
        ip_address = request.args.get("IP_address")
        mac_address = request.args.get("Mac_address")
        username = request.args.get("Username")
        password = request.args.get("Password")
        # model = request.args.get("Model")
        status = request.args.get("Status")
        location = request.args.get("Location")
        
        query = session.query(IPCamera)
        
        if camera_id:
            query = query.filter_by(Camera_Id=camera_id)
            
        if machine_id:
            query = query.filter_by(Machine_Id=machine_id)
            
        if camera_name:
            query = query.filter_by(Camera_name=camera_name)
            
        if ip_address:
            query = query.filter_by(IP_address=ip_address)
            
        if mac_address:
            query = query.filter_by(Mac_address=mac_address)
            
        if username:
            query = query.filter_by(Username=username)
            
        if password:
            query = query.filter_by(Password=password)
            
        # if model:
        #     query =query.filter_by(Model=model)
            
        if status:
            query = query.filter_by(Status=status)
            
        if location:
            query = query.filter_by(Location=location)
            
        results = query.all()
        
        camera_data = [
            {
                "Camera_Id" : c.Camera_Id,
                "Machine_Id" : c.Machine_Id,
                "Camera_name" : c.Camera_name,
                "IP_address" : c.IP_address,
                "RTSP_URL" : c.RTSP_URL,
                "HTTP_URL" : c.HTTP_URL,
                "Username" : c.Username,
                "Password" : c.Password,
                "Mac_address" : c.Mac_address,
                # "Model" : c.Model,
                "Status" : c.Status,
                "Location" : c.Location,
                "Installed_date" : c.Installed_date,
                "Created_at" : c.Created_at,
                "Updated_at" : c.Updated_at
            }
            for c in results
        ]
        
        return jsonify ({
            "message" : "IP Camera data retrieved successfully.",
            "success" : True,
            "data" : camera_data
        }), 200
        
    except Exception as e: 
        session.rollback()
        return jsonify({
            "message" : "Internal server error.",
            "error" : str(e),
            "success" : False
        }), 500
    finally:
        session.close()
        

@ipcamera_bp.route("/update/ipcamera/<int:camera_id>", methods=["PUT"])
def update_ipcamera(camera_id):
    session = SessionLocal()
    
    try:
        data = request.get_json()
        
        camera = session.query(IPCamera).get(camera_id)
        if not camera:
            return jsonify({ "message" : "Camera not found", "success" : False }), 404
        
        camera_name = data.get("Camera_name")
        ip_address = data.get("IP_address")
        rtsp_url = data.get("RTSP_URL")
        http_url = data.get("HTTP_URL")
        username = data.get("Username")
        password = data.get("Password")
        mac_address = data.get("Mac_address")
        # model = data.get("Model")
        status = data.get("Status")
        location = data.get("Location")
        installed_date = data.get("Installed_date")
        
        # Unique camera name check
        if camera_name and session.query(IPCamera).filter(
            IPCamera.Camera_Id != camera_id,
            IPCamera.Camera_name == camera_name
        ).first():
            return jsonify({"message": "Camera name already exists.", "success": False}), 400

        # Unique IP address check
        if ip_address and session.query(IPCamera).filter(
            IPCamera.Camera_Id != camera_id,
            IPCamera.IP_address == ip_address
        ).first():
            return jsonify({"message": "IP Address already exists.", "success": False}), 400
        
        # Updated fields
        
        if camera_name: camera.Camera_name = camera_name
            
        if ip_address: camera.IP_address = ip_address
        
        if rtsp_url: camera.RTSP_URL = rtsp_url
        
        if http_url: camera.HTTP_URL = http_url
        
        if username: camera.Username = username
        
        if password is not None:
            camera.Password = password
        
        if mac_address: camera.Mac_address = mac_address
        
        # if model: camera.Model = model
        
        if status: camera.Status = status
        
        if location: camera.Location = location
        
        if installed_date: camera.Installed_date = installed_date
        
        
        session.commit()
        
        return jsonify ({
            "message" : "IP Camera Updated successfully.",
            "success" : True
        }), 200
        
    except Exception as e:
        session.rollback()
        return jsonify ({
            "message" : "Internal server error.",
            "error" : str(e),
            "success" : False
        }), 500
    finally:
        session.close()
        
    
@ipcamera_bp.route("/delete/ipcamera/<int:camera_id>", methods=["DELETE"])
def delete_ipcamera(camera_id):
    session = SessionLocal()
    
    try:
        camera = session.query(IPCamera).filter(IPCamera.Camera_Id == camera_id). first()
        
        if not camera:
            return jsonify ({
                "message" : "Camera not found.",
                "success" : False
            }), 404
            
        session.delete(camera)
        session.commit()
        
        return jsonify({
            "message" : "IP Camera deleted successfully.",
            "success" : True
        }), 200
        
    except Exception as e:
        session.rollback()
        return jsonify({
            "message" : "Internal server error.",
            "error" : str(e),
            "success" : False
        }), 500
    finally:
        session.close()