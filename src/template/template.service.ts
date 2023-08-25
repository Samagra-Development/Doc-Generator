import { Injectable } from '@nestjs/common';
import { PrismaService } from 'src/prisma/prisma.service';
import { CreateTemplateDto } from './types';

@Injectable()
export class TemplateService {
  constructor(private readonly prisma: PrismaService) {}

  async create(createTemplateDto: CreateTemplateDto) {
    const { content, templateType } = createTemplateDto;
    const template = await this.prisma.template.create({
      data: {
        content,
        templateType,
      },
    });
    return template;
  }

  async findAll() {
    return await this.prisma.template.findMany();
  }

  async findOne(id: number) {
    return await this.prisma.template.findUnique({
      where: {
        id,
      },
    });
  }

  async remove(id: number) {
    return await this.prisma.template.delete({
      where: {
        id,
      },
    });
  }
}
