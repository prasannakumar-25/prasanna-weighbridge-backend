from flask import Flask
from sqlalchemy import Column, String, Integer, Float, Enum
from sqlalchemy import DateTime, Date, DECIMAL, ForeignKey, Text, Numeric
import datetime
from sqlalchemy.orm import declarative_base , relationship
# from zoneinfo import ZoneInfo

from Database.database import engine

Base = declarative_base()

# def generate_current_ist():
#     return datetime.now(ZoneInfo("Asia/Kolkata"))

    
    

class SuperAdmin(Base): 
    
    __tablename__ = "superadmin"
    
    Super_ID = Column(Integer, primary_key=True, autoincrement=True)
    User_name = Column(String(150), nullable=False, unique=True)
    Shortname = Column(String(3), nullable=False, unique=True)
    Password = Column(String(255), nullable=False)   # ------ (changed) ------
    Role = Column(String(50),nullable=False)
    Created_On = Column(DateTime, nullable=False, default=datetime.datetime.utcnow,)
    IsActive = Column(Integer, default='1')
    
    vendors = relationship("Vendor", back_populates="superadmin", cascade="all, delete-orphan")

class Vendor(Base):
    
    
    __tablename__ = "vendor"
    
    Vendor_Id = Column(Integer,primary_key=True,autoincrement=True)
    Super_ID = Column(Integer, ForeignKey("superadmin.Super_ID", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    Vendor_name = Column(String(100), unique=True, nullable=False)
    Contact_number = Column(String(15), nullable=False)
    Email = Column(String(100),unique=True,nullable=False)
    Address = Column(Text, nullable=False)
    Website = Column(String(200), nullable=True)    # ------ (added) ------
    Gst_number = Column(String(20), nullable=False, unique=True)
    Created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    Updated_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    superadmin = relationship("SuperAdmin", back_populates="vendors")
    machines = relationship("Machine", back_populates="vendor", cascade="all, delete-orphan")
    customers = relationship("Customer", back_populates="vendor", cascade="all, delete-orphan")
    vehicles = relationship("VehicleType", back_populates="vendor", cascade="all, delete-orphan")
    weighments = relationship("WeighmentDetails", back_populates="vendor", cascade="all, delete-orphan")
    
    
    
class Machine(Base):
    
    __tablename__ = "machine"
    
    Machine_Id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    Vendor_Id = Column(Integer, ForeignKey("vendor.Vendor_Id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    Machine_name = Column(String(100), nullable=False, unique=True)
    Password = Column(String(255), nullable=False)  # ------ (changed) ------
    Machine_mac = Column(String(50), nullable=False)
    Machine_model = Column(String(50), nullable=False)
    Capacity_ton = Column(DECIMAL(10, 2), nullable=False)
    Last_service_date = Column(Date, nullable=False)
    Machine_type = Column(Enum('Company', 'ThirdParty', 'Estate', name='machine_type_enum'), nullable=False, default='Company')
    Machine_location = Column(String(150), nullable=False)
    
    Status = Column(Enum('Active', 'Inactive', name='vendor_status'), default='Inactive')
    Created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    Updated_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    vendor = relationship("Vendor", back_populates="machines")
    weighments = relationship("WeighmentDetails", back_populates="machine", cascade="all, delete-orphan")
    cameras = relationship("IPCamera", back_populates="machine", cascade="all, delete-orphan")
    weighbridge = relationship("Weighbridge", back_populates="machine",cascade="all, delete-orphan")

    
class User(Base):
    
    __tablename__ = "user"
    
    User_Id = Column(Integer, primary_key=True, autoincrement=True)
    User_name = Column(String(50), unique=True, nullable=False)
    Password = Column(String(255), nullable=False)
    Full_name = Column(String(100), nullable=False)
    Email = Column(String(100), unique=True, nullable=False)
    Mobile_number = Column(String(15), nullable=False)
    Role = Column(Enum('Admin', 'Operator', 'Supervisor', name='user_roles'), nullable=False, default='Operator')
    Department = Column(String(100), nullable=True, default="")
    Created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    Updated_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    
    weighments_created = relationship("WeighmentDetails", back_populates="created_by_user")

class Customer(Base):
    
    __tablename__ = "customer"
    
    Customer_Id = Column(Integer, primary_key=True, autoincrement=True)
    Vendor_Id = Column(Integer, ForeignKey("vendor.Vendor_Id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    Customer_code = Column(String(20), unique=True, nullable=False)
    Customer_name = Column(String(100), nullable=False)
    Contact_number = Column(String(15), nullable=False)
    Email = Column(String(100), unique=True, nullable=False)
    Address = Column(Text, nullable=True)
    Gst_number = Column(String(20), nullable=False) 
    Status = Column(Enum('Active', 'Inactive', name='vendor_status'), default='')
    Created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    Updated_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    vendor = relationship("Vendor", back_populates="customers")
    vehicles = relationship("VehicleType", back_populates="customer", cascade="all, delete-orphan")
    weighments = relationship("WeighmentDetails", back_populates="customer", cascade="all, delete-orphan")
    
class VehicleType(Base):
    
    __tablename__ = "vehicle_type"
    
    Vehicle_Id = Column(Integer, primary_key=True, autoincrement=True)
    Vehicle_type = Column(String(50), nullable=False)
    Vendor_Id = Column(Integer, ForeignKey("vendor.Vendor_Id", ondelete="CASCADE", onupdate="CASCADE"), nullable=True)
    Customer_Id = Column(Integer, ForeignKey("customer.Customer_Id", ondelete="CASCADE", onupdate="CASCADE"), nullable=True)

    Tare_weight = Column(DECIMAL(10, 2), nullable=False)
    Created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    Updated_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    vendor = relationship("Vendor", back_populates="vehicles")
    customer = relationship("Customer", back_populates="vehicles")
    weighments = relationship("WeighmentDetails", back_populates="vehicle", cascade="all, delete-orphan")

    # Vehicle_number = Column(String(20), unique=True, nullable=False)
    # rfid_tag = Column(String(50), unique=True, nullable=True)
    
class WeighmentDetails(Base):
    
    __tablename__ = "weighment_details"

    Weighment_Id = Column(Integer, primary_key=True, autoincrement=True)
    Ticket_no = Column(String(20), unique=True, nullable=False)
 
    # Vendor_Id = Column(Integer, ForeignKey("vendor.Vendor_Id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)      # ------Deleted-----------------
    # Machine_Id = Column(Integer, ForeignKey("machine.Machine_Id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)     # ------Deleted-----------------
    Customer_Id = Column(Integer, ForeignKey("customer.Customer_Id", ondelete="CASCADE", onupdate="CASCADE"), nullable=True)
    Vehicle_Id = Column(Integer, ForeignKey("vehicle_type.Vehicle_Id", ondelete="CASCADE", onupdate="CASCADE"), nullable=True)

    Weighment_type = Column(Enum('Standard', 'Partial', name='weighment_type_enum'),nullable=False, default='Standard')
    First_weight = Column(Numeric(10, 2), nullable=False)              
    Second_weight = Column(Numeric(10, 2), nullable=False)
    Net_weight = Column(Numeric(10, 2), nullable=False)
    Weight_unit = Column(Enum('KG', 'TON', name='weight_unit_enum'),nullable=False, default='KG')
    # Product_name = Column(String(100), nullable=True)
    # Gross_weight = Column(Numeric(10, 2), nullable=True)
    # Tare_weight = Column(Numeric(10, 2), nullable=True)
    # Product_weight = Column(Numeric(10, 2), nullable=True)
    Sequence_no = Column(Integer, nullable=False)               # ------change-----------------

    Image_path = Column(String(255), nullable=False)            # ------change-----------------
    Image_type = Column(Enum('Front', 'Back', 'RightSide', 'LeftSide', name='image_type_enum'),nullable=False, default="")

    Status = Column(Enum('Pending', 'Completed', 'Cancelled', name='status_enum'),nullable=False, default='')
    Created_by = Column(Integer, ForeignKey("user.User_Id"), nullable=False)
    Created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    Updated_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    Completed_at = Column(DateTime, nullable=False)             # ------change-----------------
    
    vendor = relationship("Vendor", back_populates="weighments")
    machine = relationship("Machine", back_populates="weighments")
    customer = relationship("Customer", back_populates="weighments")
    vehicle = relationship("VehicleType", back_populates="weighments")
    created_by_user = relationship("User", back_populates="weighments_created")
    partial_products = relationship("PartialDetails", back_populates="weighment", cascade="all, delete-orphan")
    
class PartialDetails(Base):       # ------change-----------------
    
    __tablename__ = "partial_details"
    
    Partial_Id = Column(Integer, primary_key=True, autoincrement=True)
    Weighment_Id = Column(Integer, ForeignKey("weighment_details.Weighment_Id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    Product_name = Column(String(100), nullable=False)
    Net_weight = Column(Numeric(10, 2), nullable=False) # Or Product weight
    Created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    Updated_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    
    weighment = relationship("WeighmentDetails", back_populates="partial_products")
    
    
class IPCamera(Base):
    
    __tablename__ = "ip_camera"
    
    Camera_Id = Column(Integer, primary_key=True, autoincrement=True)
    Machine_Id = Column(Integer, ForeignKey("machine.Machine_Id", ondelete="CASCADE", onupdate="CASCADE"), nullable=True)
    
    Camera_name = Column(String(100), nullable=False)
    IP_address = Column(String(50), nullable=False)
    RTSP_URL = Column(String(255), nullable=False)
    HTTP_URL = Column(String(255), nullable=False)

    Username = Column(String(100), nullable=False)
    Password = Column(String(255), nullable=False, default='')

    Mac_address = Column(String(50), nullable=False)
    # Model = Column(String(100), nullable=True)
    # Firmware_version = Column(String(100), nullable=True)
    Status = Column(Enum('Online', 'Offline', 'Error', name='camera_status_enum'),nullable=False, default='Offline')
    Location = Column(String(150), nullable=False)
    Installed_date = Column(Date, nullable=False)

    Created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    Updated_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationship → Machine
    machine = relationship("Machine", back_populates="cameras")
    
    
class Weighbridge(Base):
    
    __tablename__ = "weigh_bridge"
    
    Weighbridge_Id = Column(Integer, primary_key=True , autoincrement=True)
    Machine_Id = Column(Integer, ForeignKey("machine.Machine_Id", ondelete="CASCADE", onupdate="CASCADE"), nullable=True)
    Serial_no = Column(String(100), nullable=True)
    
    Port = Column(Enum('COM4', 'COM3', name='weigh-bridge'), default='COM4', nullable=False)
    Baud_rate = Column(Integer, default='19200', nullable=False)
    Data_bit = Column(Integer, nullable=False, default='8')
    Stop_bit = Column(Integer, nullable=False, default='1')
    Party = Column(String(100), nullable=False, default=None)
    
    Created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    Updated_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    machine = relationship("Machine", back_populates="weighbridge")
    
    
class Standardload(Base):
    
    __tablename__ = "standardload"
    
    Standard_Id = Column(Integer, primary_key=True , autoincrement=True)
    Machine_Id = Column(Integer, ForeignKey("machine.Machine.Id", ondelete="CASCADE" , onupdate="CASCADE"), nullable=True)
    Vehicle_Id = Column(Integer, ForeignKey("vehicle_type.Vehicle_Id", ondelete="CASCADE", onupdate="CASCADE"), nullable=True)
    
    Serial_NO = Column(String(100), nullable=True)
    Contact_Number = Column(Integer, )
    

Base.metadata.create_all(bind=engine)
print("Table created succussfully")













# class Weighment_Transaction(Base):
#     __tablename__ = "weighment_transaction"

#     weighment_id = Column(Integer, primary_key=True, autoincrement=True)
#     ticket_no = Column(String(20), unique=True, nullable=False)

#     vendor_id = Column(Integer, ForeignKey("vendor_registration.VENDOR_ID"), nullable=False)
#     machine_id = Column(Integer, ForeignKey("machine_master.machine_id"), nullable=False)
#     customer_id = Column(Integer, ForeignKey("customer_master.customer_id"), nullable=True)
#     vehicle_id = Column(Integer, ForeignKey("vehicle_master.vehicle_id"), nullable=False)

#     weighment_type = Column(Enum('Standard', 'Partial', name='weighment_type_enum'), nullable=False)
#     first_weight = Column(DECIMAL(10, 2), nullable=False)
#     second_weight = Column(DECIMAL(10, 2), nullable=True)
#     net_weight = Column(DECIMAL(10, 2), nullable=True)

#     weight_unit = Column(Enum('KG', 'TON', name='weight_unit_enum'), default='KG', nullable=False)
#     remarks = Column(Text, nullable=True)
#     status = Column(Enum('Pending', 'Completed', 'Cancelled', name='weighment_status_enum'), default='Pending', nullable=False)

#     created_by = Column(Integer, ForeignKey("user_master.user_id"), nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     completed_at = Column(DateTime, nullable=True)


# class Partial_Weighment(Base):
#     __tablename__ = "partial_weighment"

#     partial_id = Column(Integer, primary_key=True, autoincrement=True)
#     weighment_id = Column(Integer, ForeignKey("weighment_transaction.weighment_id"), nullable=False)

#     product_name = Column(String(100), nullable=False)
#     gross_weight = Column(DECIMAL(10, 2), nullable=False)
#     tare_weight = Column(DECIMAL(10, 2), nullable=False)
#     product_weight = Column(DECIMAL(10, 2), nullable=True)
#     sequence_no = Column(Integer, nullable=False)
#     remarks = Column(Text, nullable=True)

#     created_at = Column(DateTime, default=datetime.utcnow)
