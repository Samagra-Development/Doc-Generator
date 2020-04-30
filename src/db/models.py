from .app import db
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
    raw_data = db.Column(
        db.JSON, nullable=False)  # All the received content (the request)
    tags = db.Column(
        db.JSON)  # All the mapping content 
    doc_url = db.Column(
        db.String(256)
    )  # google doc url of the generated document (will get doc id from it)
    current_status = db.Column(
        db.String(32),
        default='Queue')  # Queue, Processing, Failed, complete, ERROR
    step = db.Column(
        db.Integer,
        default=0)  # 0->data fetch,1->mapping fetch,2->pdf build,3-> upload pdf
    tries = db.Column(
        db.Integer, default=0)  # No. of attempts trying to process the request
    doc_name = db.Column(
        db.String(64)
    )  # Google doc File name on google drive. Name of the google doc and pdf (both names will be same)
    pdf_version = db.Column(
        db.Integer, default=0)  # The PDF version (max 5 allowed)
    error_encountered = db.Column(db.String())  # Google app script url
    task_completed = db.Column(
        db.Boolean, default=False)  # Is the process completed True/False
    
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
    raw_data = db.Column(
        db.JSON, nullable=False)  # All the received content (the request)
    doc_url = db.Column(
        db.String(128)
    )  # google doc url of the generated document (will get doc id from it)
    tags = db.Column(
        db.JSON)  # All the mapping content 
    doc_name = db.Column(db.String(64))  # google doc File name on
    pdf_version = db.Column(
        db.Integer, default=1)  # The PDF version (max 5 allowed)
    
    def __repr__(self):
        return '{}'.format(self.unique_id)

    def dump(self):
        for attr in dir(obj):
            if hasattr(obj, attr):
                print("obj.%s = %s" % (attr, getattr(obj, attr)))
