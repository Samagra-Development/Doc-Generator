import json
import uuid
from .config import KAFKA_CREDENTIAL
from kafka import KafkaConsumer
from utils.func import initialize_logger, info_log, call_healthcheck_url
from db.app import DB, create_app
from db.models import PdfData, BackupPdfData
from .config import HEALTHCHECKURL

logging = initialize_logger()
logger = logging.getLogger(__name__)
app = create_app()

def save_pdf_data(final_data, tags, linked_instance_id, is_delete):

    unique_ids = []
    json_data = PdfData(
        raw_data=final_data,
        tags=tags,
        instance_id=uuid.uuid4(),
        link_id=linked_instance_id,
        is_delete=is_delete
    )
    DB.session.add(json_data)  # Adds new User record to database
    DB.session.flush()  # Pushing the object to the database so that it gets assigned a unique id
    unique_ids.append(json_data.unique_id)
    DB.session.commit()  # Commits all changes
    obj = DB.session.query(BackupPdfData).filter(BackupPdfData.link_id == linked_instance_id).first()
    if obj:
        DB.session.delete(obj)
        DB.session.commit()
    status = 'submitted'
    return {"status": status, "uniqueId": unique_ids}


try:

    consumer = KafkaConsumer(KAFKA_CREDENTIAL['topic'], bootstrap_servers=KAFKA_CREDENTIAL['bootstrap_servers'],
                             security_protocol=KAFKA_CREDENTIAL['security_protocol'],
                             sasl_mechanism=KAFKA_CREDENTIAL['sasl_mechanism'],
                             sasl_plain_username=KAFKA_CREDENTIAL['sasl_plain_username'],
                             sasl_plain_password=KAFKA_CREDENTIAL['sasl_plain_password'],
                             group_id=KAFKA_CREDENTIAL['group_id'],
                             auto_offset_reset=KAFKA_CREDENTIAL['auto_offset_reset'],
                                                                enable_auto_commit=KAFKA_CREDENTIAL['enable_auto_commit'],
                             auto_commit_interval_ms=KAFKA_CREDENTIAL['auto_commit_interval_ms'])
    logger.info('consumer started')
    for message in consumer:
        key = message.key.decode('utf-8')
        logger.info('Message receive')
        call_healthcheck_url(HEALTHCHECKURL['KAFKACONSUMERURL'])
        raw_data = json.loads(message.value.decode('utf-8'))
        print(key)
        info_log(logger.info, "Step1 Save into db Start",
                 raw_data['reqd_data'])
        with app.app_context():
            save_pdf_data(raw_data['reqd_data'], raw_data['tags'], raw_data['instance_id'], raw_data['is_delete'])
            info_log(logger.info, "Step1 Save into db End",
                     raw_data['reqd_data'])
            consumer.commit()
    if consumer is not None:
        consumer.close()
        #print(value['receiver_address'])
except Exception as ex:
    logger.error('Error in receiving request from kafka')
    logger.error("Exception occurred", exc_info=True)
