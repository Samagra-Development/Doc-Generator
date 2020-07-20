KAFKA_CREDENTIAL = {'topic': 'u518r2qy-form',
                    'bootstrap_servers': ['moped-01.srvs.cloudkafka.com:9094',
                                          'moped-02.srvs.cloudkafka.com:9094',
                                          'moped-03.srvs.cloudkafka.com:9094'],
                    'security_protocol': 'SASL_SSL',
                    'sasl_mechanism': 'SCRAM-SHA-256',
                    'sasl_plain_username': 'u518r2qy',
                    'sasl_plain_password': 'xUTDBhfZ-DlmPmRwQ4J1Qw49QsMzieZV',
                    'group_id': 'form-group',
                    'auto_offset_reset': 'earliest', 'enable_auto_commit': True,
                    'auto_commit_interval_ms': 1000
                    }

HEALTHCHECKURL = {'PLUGINURL':'https://hc-ping.com/bd58f889-0a9c-4346-97f4-34410a88fbb0',
                  'KAFKACONSUMERURL':'https://hc-ping.com/aeb00a20-674d-44d6-acbf-9f85f6f57fd4'}