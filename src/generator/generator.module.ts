import { Module } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { SharedModule } from '../shared/shared.module';
import { RenderModule } from 'templater';
import { BatchService } from './batch.service';
import { GeneratorController } from './generator.controller';
import { GeneratorService } from './generator.service';

@Module({
  imports: [RenderModule, SharedModule],
  providers: [GeneratorService, PrismaService, BatchService],
  controllers: [GeneratorController],
})
export class GeneratorModule {}
