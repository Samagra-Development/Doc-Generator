import { Module } from '@nestjs/common';
import { PrismaService } from 'src/prisma/prisma.service';
import { RenderModule } from 'templater';
import { BatchService } from './batch.service';
import { GeneratorController } from './generator.controller';
import { GeneratorService } from './generator.service';

@Module({
  imports: [RenderModule],
  providers: [GeneratorService, PrismaService, BatchService],
  controllers: [GeneratorController],
})
export class GeneratorModule {}
