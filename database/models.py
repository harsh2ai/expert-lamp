from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ShipmentTracking(Base):
    __tablename__ = "VIEW_TITANIUM_PLATINUM_REPORT"
    __table_args__ = {'schema': 'public'}

    # Using AWB_CODE as primary key
    AWB_CODE = Column(String, primary_key=True)
    
    # Geographical and Classification columns
    ZONE = Column(Enum('z_a', 'z_b', 'z_c', 'z_d', 'z_e', 'z_e2', name='zone_enum'))
    CITY_TIER = Column(Enum('Tier1', 'Tier2', 'Tier3', 'Metro', 'Others', name='city_tier_enum'))
    DELIVERY_STATE = Column(String)
    
    # Timestamps
    ASSIGNED_DATE_TIME = Column(DateTime)
    PICKED_DATE = Column(DateTime)
    PICKED_UP_DATE = Column(DateTime)
    FIRST_NDR_RAISED = Column(DateTime)
    FIRST_ATTEMPT_DATE = Column(DateTime)
    AWB_DELIVERED_DATE = Column(DateTime)
    
    # Identifiers
    COMPANY_ID = Column(String)
    ORDER_ID = Column(String)
    PARENT_COURIER = Column(String)
    
    # Shipment Details
    MODE_OF_SHIPMENT = Column(Enum('PREPAID', 'COD', name='shipment_mode_enum'))
    COURIER_MODE = Column(Enum('air', 'surface', name='courier_mode_enum'))
    SHIP_TYPE = Column(Enum('advance_rule', 'bulk', 'external_api', 'single_ship', 'wrapper_api', 
                           name='ship_type_enum'))
    
    # Metrics and Flags
    IS_DELIVERYBOOST = Column(Boolean)
    SHIPMENT_STATUS = Column(String)
    TOTAL_SHIPMENTS = Column(Integer, default=1)
    RTO_SHIPMENTS = Column(Boolean)
    NOT_ATTEMPTED = Column(Boolean)
    FASR_SHIPMENT = Column(Boolean)
    NO_OF_ATTEMPTS = Column(Integer)
    NDR_RAISED_SHIPMENTS = Column(Boolean)
    NDR_DELIVERED_SHIPMENTS = Column(Boolean)
    DELIVERED_SHIPMENTS = Column(Boolean)
    
    # Weight and Value
    IS_WEIGHT_DESCRIPANCY = Column(Boolean)
    APPLIED_WEIGHT = Column(Float)
    COURIER_CHARGED_WEIGHT = Column(Float)
    ORDER_VALUE = Column(Float)
    
    # Customer Response
    BUYER_POSITIVE_RESPONSE_TOTAL_SHIPMENTS = Column(Boolean)
    BUYER_POSITIVE_RESPONSE_DELIVERED_SHIPMENTS = Column(Boolean)

    def to_dict(self):
        """Convert model instance to dictionary"""
        return {column.name: getattr(self, column.name) 
                for column in self.__table__.columns}

class QueryCache(Base):
    """Optional: Cache for frequent queries"""
    __tablename__ = "query_cache"

    id = Column(Integer, primary_key=True)
    query_hash = Column(String, unique=True)
    query_text = Column(String)
    result = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)