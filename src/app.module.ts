import { HttpModule } from '@nestjs/axios';
import { Module } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { TerminusModule } from '@nestjs/terminus';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { PrismaService } from './prisma/prisma.service';
import { PrismaHealthIndicator } from './health/prisma.health';
import { ClientsModule, Transport } from '@nestjs/microservices';
import { HealthController } from './health/health.controller';
import { PrismaModule } from './prisma/prisma.module';
import { RenderModule } from 'templater';
import { GeneratorModule } from './generator/generator.module';
import { TemplateModule } from './template/template.module';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
    }),
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
    HttpModule,
    TerminusModule,
    PrismaModule,
    RenderModule,
    GeneratorModule,
    TemplateModule,
  ],
  controllers: [AppController, HealthController],
  providers: [AppService, PrismaService, PrismaHealthIndicator],
})
export class AppModule {}
