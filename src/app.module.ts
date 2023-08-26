import { HttpModule } from '@nestjs/axios';
import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { TerminusModule } from '@nestjs/terminus';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { PrismaService } from './prisma/prisma.service';
import { PrismaHealthIndicator } from './health/prisma.health';
import { HealthController } from './health/health.controller';
import { PrismaModule } from './prisma/prisma.module';
import { RenderModule } from 'templater';
import { GeneratorModule } from './generator/generator.module';
import { TemplateModule } from './template/template.module';
import { SharedModule } from './shared/shared.module';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
    }),
    SharedModule,
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
