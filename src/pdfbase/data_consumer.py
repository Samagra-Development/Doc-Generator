import json
import uuid
from .config import KAFKA_CREDENTIAL
from kafka import KafkaConsumer, TopicPartition
from utils.func import initialize_logger, info_log, call_healthcheck_url
from db.app import DB, create_app
from db.models import PdfData, BackupPdfData
from .config import HEALTHCHECKURL
import traceback
from confluent_kafka import Consumer, Producer

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
    c = Consumer({
        'bootstrap.servers': KAFKA_CREDENTIAL['bootstrap_servers'],
        'auto.offset.reset': KAFKA_CREDENTIAL['auto_offset_reset'],
        'group.id': KAFKA_CREDENTIAL['group']
    })
    c.subscribe([KAFKA_CREDENTIAL['topic']])

    logger.info('consumer started')
    while True:
        msg = c.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue

        try:
            key = msg.key()
            call_healthcheck_url(HEALTHCHECKURL['KAFKACONSUMERURL'])
            raw_data = json.loads(msg.value().decode('utf-8'))
            info_log(logger.info, "Step1 Save into db Start", raw_data['reqd_data'])
            with app.app_context():
                save_pdf_data(raw_data['reqd_data'], raw_data['tags'], raw_data['instance_id'], raw_data['is_delete'])
                info_log(logger.info, "Step1 Save into db End", raw_data['reqd_data'])
        except:
            print(traceback.format_exc())
            print("Message not in correct format: Ignored")
            c.commit()

    c.close()
except Exception as ex:
    print(traceback.format_exc())
    logger.error('Error in receiving request from kafka')
    logger.error("Exception occurred", exc_info=True)