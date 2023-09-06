// shared.module.ts
import { Module } from '@nestjs/common';
import { ClientsModule, Transport } from '@nestjs/microservices';
import { ConfigModule, ConfigService } from '@nestjs/config';

@Module({
  imports: [
    ClientsModule.registerAsync([
      {
        name: 'BATCH_PROCESSING',
        imports: [ConfigModule],
        useFactory: async (config: ConfigService) => ({
          transport: Transport.RMQ,
          options: {
            urls: [config.getOrThrow<string>('RMQ_URL')],
            queue: config.getOrThrow<string>('RMQ_QUEUE'),
            queueOptions: {
              durable:
                config.getOrThrow<string>('RMQ_QUEUE_DURABLE') === 'true'
                  ? true
                  : false,
            },
          },
        }),
        inject: [ConfigService],
      },
    ]),
  ],
  exports: [ClientsModule],
})
export class SharedModule {}
