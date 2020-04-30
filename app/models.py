from app import db
import pprint
from sqlalchemy import inspect

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


class pdfData(db.Model):
    __tablename__ = 'queuemanager'

    unique_id = db.Column(
        db.Integer, primary_key=True)  # unique_id from the request
    instance_id = db.Column(
        db.String(256), default=None)  # Id of the instance if available
    reqd_data = db.Column(
        db.JSON, nullable=False)  # All the received content (the request)
    g_doc_url = db.Column(
        db.String(256)
    )  # google doc url of the generated document (will get doc id from it)
    current_status = db.Column(
        db.String(32),
        default='Queue')  # Queue, Processing, Failed, complete, ERROR
    gcs_url = db.Column(db.String(256))  # GCS unsigned url
    tries = db.Column(
        db.Integer, default=0)  # No. of attempts trying to process the request
    var_mapping_id = db.Column(db.String(128))  # Id of variable mapping sheet
    doc_template_id = db.Column(db.String(128))  # Id of the doc template
    user_name = db.Column(db.String(128))  # Username from data
    application_id = db.Column(
        db.String(128))  # application_id for mapping forms
    form_id = db.Column(
        db.String(128),
        default=None)  # Form id to fetch responses for custom module
    form_name = db.Column(
        db.String(128),
        default=None)  # Form name to fetch responses for custom module
    google_doc_name = db.Column(
        db.String(64)
    )  # Google doc File name on google drive. Name of the google doc and pdf (both names will be same)
    pdf_version = db.Column(
        db.Integer, default=0)  # The PDF version (max 5 allowed)
    error_encountered = db.Column(db.String())  # Google app script url
    mapping_fetched = db.Column(
        db.Boolean,
        default=False)  # variable and options Mapping Fetched True/False
    gas_url = db.Column(db.String())  # Google app script url
    var_mapped = db.Column(
        db.Boolean, default=False)  # Variables mapped True/False
    gas_url_gen = db.Column(
        db.Boolean, default=False)  # Google app script url generated True/False
    gas_url_call = db.Column(
        db.Boolean, default=False)  # Google app script url called True/False
    pdf_downloaded = db.Column(
        db.Boolean, default=False)  # PDF Downloaded True/False
    pdf_uploaded = db.Column(
        db.Boolean, default=False)  # PDF uploaded to GCS True/False
    task_completed = db.Column(
        db.Boolean, default=False)  # Is the process completed True/False
    udise = db.Column(
        db.Integer, default=1101)  # Storing the udise information
    form_submission_date = db.Column(db.String(64))  # Form Submission date
    # req_received adding the received request current_timestamp
    req_received = db.Column(
        db.DateTime, nullable=False, server_default=db.func.current_timestamp())
    # req_update adding the timestamp for row updated
    req_update = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
        server_onupdate=db.func.current_timestamp())

    def __repr__(self):
        return '{}'.format(self.unique_id)

    def dump(self):
        pp = pprint.PrettyPrinter(indent=4)
        d = object_as_dict(self)
        pp.pprint(d)


class outputTable(db.Model):
    __tablename__ = 'outputtable'

    unique_id = db.Column(
        db.Integer, primary_key=True)  # unique_id from the request
    instance_id = db.Column(
        db.String(256), default=None)  # Id of the instance if available
    g_doc_url = db.Column(
        db.String(128)
    )  # google doc url of the generated document (will get doc id from it)
    gcs_url = db.Column(db.String(256))  # GCS unsigned url
    var_mapping_id = db.Column(db.String(128))  # Id of variable mapping sheet
    user_name = db.Column(db.String(128))  # Username from data
    application_id = db.Column(
        db.String(128))  # application_id for mapping forms
    doc_template_id = db.Column(db.String(128))  # Id of the doc template
    form_id = db.Column(
        db.String(128),
        default=None)  # Form id to fetch responses for custom module
    form_name = db.Column(
        db.String(128),
        default=None)  # Form name to fetch responses for custom module
    google_doc_name = db.Column(db.String(64))  # google doc File name on
    pdf_version = db.Column(
        db.Integer, default=1)  # The PDF version (max 5 allowed)
    gas_url = db.Column(db.String())  # Google app script url
    cache_cleaned = db.Column(
        db.Boolean, default=False
    )  # Check if the cache is cleaned from drive and server True/False. Cache - doc from drive, pdf from server.
    # req_received adding the received request current_timestamp
    udise = db.Column(
        db.Integer, default=1101)  # Storing the udise information
    form_submission_date = db.Column(db.String(64))  # Form Submission date
    req_received = db.Column(db.DateTime)
    # req_completed adding the timestamp for request completed
    req_completed = db.Column(
        db.DateTime, nullable=False, server_default=db.func.current_timestamp())

    def __repr__(self):
        return '{}'.format(self.unique_id)

    def dump(self):
        for attr in dir(obj):
            if hasattr(obj, attr):
                print("obj.%s = %s" % (attr, getattr(obj, attr)))


class udiseData(db.Model):
    __tablename__ = 'udise'

    District = db.Column(db.String())
    Block = db.Column(db.String())
    Cluster = db.Column(db.String())
    Village = db.Column(db.String())
    Udise = db.Column(db.Integer, primary_key=True)
    SchoolName = db.Column(db.String())
    SchoolType = db.Column(db.String())
    RuralOrUrban = db.Column(db.String())
    AcademicCycle = db.Column(db.String())
    PinCode = db.Column(db.Integer)
    LatDeg = db.Column(db.Integer)
    LatMin = db.Column(db.Integer)
    LatSec = db.Column(db.Integer)
    LonDeg = db.Column(db.Integer)
    LonMin = db.Column(db.Integer)
    LonSec = db.Column(db.Integer)

    def __repr__(self):
        return '{}'.format(self.Udise)

    def dump(self):
        for attr in dir(obj):
            if hasattr(obj, attr):
                print("obj.%s = %s" % (attr, getattr(obj, attr)))
