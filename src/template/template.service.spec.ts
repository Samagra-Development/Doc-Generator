import { HttpException } from '@nestjs/common';
import { Test, TestingModule } from '@nestjs/testing';
import { PrismaService } from '../prisma/prisma.service';
import { TemplateService } from './template.service';

describe('TemplateService', () => {
  let service: TemplateService;
  let prismaService: PrismaService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [TemplateService, PrismaService],
    }).compile();

    service = module.get<TemplateService>(TemplateService);
    prismaService = module.get<PrismaService>(PrismaService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });

  describe('getTemplate', () => {
    it('should throw error when template not found', async () => {
      jest.spyOn(prismaService.template, 'findUnique').mockResolvedValue(null);

      await expect(service.getTemplate(1)).rejects.toThrow(
        new HttpException(`Template not found with ID: 1`, 404),
      );
    });

    it('should return template when found', async () => {
      const mockTemplate = {
        id: '1',
        templateType: 'JSTL',
        content: '${content}',
      };
      jest
        .spyOn(prismaService.template, 'findUnique')
        .mockResolvedValue(mockTemplate as any);

      const result = await service.getTemplate(1);

      expect(result).toBe(mockTemplate);
    });
  });

  describe('remove', () => {
    it('should throw error when template not found', async () => {
      jest.spyOn(prismaService.template, 'findUnique').mockResolvedValue(null);

      await expect(service.remove(1)).rejects.toThrow(
        new HttpException(`Template not found with ID: 1`, 404),
      );
    });

    it('should return template when found', async () => {
      const mockTemplate = {
        id: '1',
        templateType: 'JSTL',
        content: '${content}',
      };
      jest
        .spyOn(prismaService.template, 'findUnique')
        .mockResolvedValue(mockTemplate as any);
      jest
        .spyOn(prismaService.template, 'delete')
        .mockResolvedValue(mockTemplate as any);

      const result = await service.remove(1);

      expect(result).toBe(mockTemplate);
    });
  });

  describe('create', () => {
    it('should create template', async () => {
      const mockTemplate = {
        id: '1',
        templateType: 'JSTL',
        content: '${content}',
      };
      jest
        .spyOn(prismaService.template, 'create')
        .mockResolvedValue(mockTemplate as any);

      const result = await service.create({
        content: '${content}',
        templateType: 'JSTL',
      });

      expect(result).toBe(mockTemplate);
    });
  });
});
