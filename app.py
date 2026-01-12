from flask import Flask
from flask import Blueprint, jsonify, request
from flask_cors import CORS
from api.vendorApi import vendor_bp
from api.machineApi import machine_bp
from api.userApi import user_bp
from api.customerApi import customer_bp
from api.vehicletypeApi import vehicletype_bp
from api.weighmentDetailsApi import Weighment_Details_bp
from api.partialDetailsApi import partialDarails_bp
from api.weighBridgeApi import weighbridge_bp
from api.ipCameraApi import ipcamera_bp
from api.authuser import auth_user
# from api.authAdminApi import auth_admin
from dotenv import load_dotenv
from extension import bcrypt,jwt
from flask_bcrypt import Bcrypt
import os



load_dotenv()

from Database.database import SessionLocal
app = Flask(__name__)
CORS(app)
# bcrypt = Bcrypt(app)

bcrypt.init_app(app)
jwt.init_app(app)



app.config["JWT_SECRET_KEY"]=os.getenv("JWT_SECRET_KEY")

CORS(app, resources={r"/*": {"origins": "*"}}) 


app.register_blueprint(vendor_bp)
app.register_blueprint(machine_bp)
app.register_blueprint(user_bp)
app.register_blueprint(customer_bp)
app.register_blueprint(vehicletype_bp)
app.register_blueprint(Weighment_Details_bp)
app.register_blueprint(partialDarails_bp)
app.register_blueprint(weighbridge_bp)
app.register_blueprint(ipcamera_bp)
app.register_blueprint(auth_user)
# app.register_blueprint(auth_admin)


@app.route('/health', methods=["GET"])
def healthCheck():
    try:
        return jsonify({"message":"backend runing successfully"})
    except Exception as e:
        return jsonify({"message":"Something error", "error": str(e)})
    
if __name__ == "__main__":
    app.run(debug=True)
