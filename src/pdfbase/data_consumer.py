import json
import uuid
from kafka import KafkaConsumer
from utils.func import initialize_logger, info_log
from db.app import DB, create_app
from db.models import PdfData

logging = initialize_logger()
logger = logging.getLogger(__name__)
app = create_app()

def save_pdf_data(final_data, tags, linked_instance_id):
    unique_ids = []
    json_data = PdfData(
        raw_data=final_data,
        tags=tags,
        instance_id=uuid.uuid4(),
        link_id=linked_instance_id)
    DB.session.add(json_data)  # Adds new User record to database
    DB.session.flush()  # Pushing the object to the database so that it gets assigned a unique id
    unique_ids.append(json_data.unique_id)
    DB.session.commit()  # Commits all changes
    status = 'submitted'
    return {"status": status, "uniqueId": unique_ids}


try:

    consumer = KafkaConsumer('u518r2qy-default', bootstrap_servers=['moped-01.srvs.cloudkafka.com:9094'],
                             security_protocol='SASL_SSL',
                             sasl_mechanism='SCRAM-SHA-256',
                             sasl_plain_username='u518r2qy',
                             sasl_plain_password='xUTDBhfZ-DlmPmRwQ4J1Qw49QsMzieZV',
                             group_id='form-group',
                             auto_offset_reset='earliest', enable_auto_commit=True,
                             auto_commit_interval_ms=1000)
    logger.info('consumer started')
    for message in consumer:
        key = message.key.decode('utf-8')
        logger.info('Message receive')
        raw_data = json.loads(message.value.decode('utf-8'))
        print(key)
        info_log(logger.info, "Step1 Save into db Start",
                 raw_data['reqd_data'])
        with app.app_context():
            save_pdf_data(raw_data['reqd_data'], raw_data['tags'], raw_data['instance_id'])
            info_log(logger.info, "Step1 Save into db End",
                     raw_data['reqd_data'])
            consumer.commit()
    if consumer is not None:
        consumer.close()
        #print(value['receiver_address'])
except Exception as ex:
    logger.error('Error in receiving request from kafka')
    logger.error("Exception occurred", exc_info=True)
