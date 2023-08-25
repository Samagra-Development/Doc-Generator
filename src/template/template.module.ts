import { Module } from '@nestjs/common';
import { TemplateService } from './template.service';
import { TemplateController } from './template.controller';
import { PrismaService } from 'src/prisma/prisma.service';

@Module({
  controllers: [TemplateController],
  providers: [TemplateService, PrismaService],
})
export class TemplateModule {}
