import { HttpException, Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
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

  async getTemplates() {
    return await this.prisma.template.findMany();
  }

  async getTemplate(id: number) {
    const template = await this.prisma.template.findUnique({
      where: {
        id,
      },
    });
    if (!template) {
      throw new HttpException(`Template not found with ID: ${id}`, 404);
    }
    return template;
  }

  async remove(id: number) {
    const template = await this.prisma.template.findUnique({
      where: {
        id,
      },
    });
    if (!template) {
      throw new HttpException(`Template not found with ID: ${id}`, 404);
    }
    await this.prisma.template.delete({
      where: {
        id,
      },
    });
    return template;
  }
}
