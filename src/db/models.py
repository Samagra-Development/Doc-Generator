"""
Define Model Use
"""
import pprint
from sqlalchemy import inspect
from .app import DB

def object_as_dict(obj):
    """
    convert object into dict
    """
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


class PdfData(DB.Model):
    """
    Define table which save request received
    """
    __tablename__ = 'queuemanager'

    unique_id = DB.Column(
        DB.Integer, primary_key=True)  # unique_id from the request
    instance_id = DB.Column(
        DB.String(256), default=None)  # Id of the instance if available
    raw_data = DB.Column(
        DB.JSON, nullable=False)  # All the received content (the request)
    tags = DB.Column(
        DB.JSON)  # All the mapping content
    doc_url = DB.Column(
        DB.String(256)
    )  # google doc url of the generated document (will get doc id from it)
    current_status = DB.Column(
        DB.String(32),
        default='Queue')  # Queue, Processing, Failed, complete, ERROR
    step = DB.Column(
        DB.Integer,
        default=0)  # 0->data fetch,1->mapping fetch,2->pdf build,3-> upload pdf
    tries = DB.Column(
        DB.Integer, default=0)  # No. of attempts trying to process the request
    doc_name = DB.Column(
        DB.String(64)
    )  # Google doc File name on google drive. Name of the google doc
    #and pdf (both names will be same)
    pdf_version = DB.Column(
        DB.Integer, default=0)  # The PDF version (max 5 allowed)
    error_encountered = DB.Column(DB.String())  # Google app script url
    task_completed = DB.Column(
        DB.Boolean, default=False)  # Is the process completed True/False
    def __repr__(self):
        """
        return table unique id
        """
        return '{}'.format(self.unique_id)

    def dump(self):
        """
        print data in string format
        """
        pr_p = pprint.PrettyPrinter(indent=4)
        pr_di = object_as_dict(self)
        pr_p.pprint(pr_di)


class OutputTable(DB.Model):
    """
    Define output table which save request processed
    """
    __tablename__ = 'outputtable'

    unique_id = DB.Column(
        DB.Integer, primary_key=True)  # unique_id from the request
    instance_id = DB.Column(
        DB.String(256), default=None)  # Id of the instance if available
    raw_data = DB.Column(
        DB.JSON, nullable=False)  # All the received content (the request)
    doc_url = DB.Column(
        DB.String(128)
    )  # google doc url of the generated document (will get doc id from it)
    tags = DB.Column(
        DB.JSON)  # All the mapping content
    doc_name = DB.Column(DB.String(64))  # google doc File name on
    pdf_version = DB.Column(
        DB.Integer, default=1)  # The PDF version (max 5 allowed)
    def __repr__(self):
        """
        return table unique id
        """
        return '{}'.format(self.unique_id)
