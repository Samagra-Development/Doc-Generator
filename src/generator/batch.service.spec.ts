import { Test, TestingModule } from '@nestjs/testing';
import { BatchService } from './batch.service';
import { PrismaService } from '../prisma/prisma.service';
import { RenderService } from 'templater';
import { HttpException } from '@nestjs/common';

describe('BatchService', () => {
  let batchService: BatchService;
  let prismaService: PrismaService;
  let renderService: RenderService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        BatchService,
        PrismaService,
        {
          provide: RenderService,
          useValue: { renderTemplate: jest.fn() },
        },
        {
          provide: 'BATCH_PROCESSING',
          useValue: {
            emit: jest.fn(),
          },
        },
      ],
    }).compile();

    batchService = module.get<BatchService>(BatchService);
    prismaService = module.get<PrismaService>(PrismaService);
    renderService = module.get<RenderService>(RenderService);
  });

  describe('getBatch', () => {
    it('should throw error when batch not found', async () => {
      jest.spyOn(prismaService.batch, 'findUnique').mockResolvedValue(null);

      await expect(batchService.getBatch('1')).rejects.toThrow(
        new HttpException(`Batch not found with ID: 1`, 404),
      );
    });

    it('should return batch when found', async () => {
      const mockBatch = {
        id: '1',
        template: {
          id: '1',
          templateType: 'JSTL',
          content: '${content}',
        },
        payload: [],
      };
      jest
        .spyOn(prismaService.batch, 'findUnique')
        .mockResolvedValue(mockBatch as any);

      const result = await batchService.getBatch('1');

      expect(result).toBe(mockBatch);
    });
  });

  describe('getBatches', () => {
    it('should return batches', async () => {
      const mockBatches = [
        {
          id: '1',
          template: {
            id: '1',
            templateType: 'JSTL',
            content: '${content}',
          },
          payload: [],
        },
      ];
      jest
        .spyOn(prismaService.batch, 'findMany')
        .mockResolvedValue(mockBatches as any);

      const result = await batchService.getBatches();

      expect(result).toBe(mockBatches);
    });
  });

  describe('deleteBatch', () => {
    it('should throw error when batch not found', async () => {
      jest.spyOn(prismaService.batch, 'delete').mockResolvedValue(null);

      await expect(batchService.deleteBatch('1')).rejects.toThrow(
        new HttpException(`Batch not found with ID: 1`, 404),
      );
    });

    it('should return batch when found', async () => {
      const mockBatch = {
        id: '1',
        template: {
          id: '1',
          templateType: 'JSTL',
          content: '${content}',
        },
        payload: [],
      };
      jest
        .spyOn(prismaService.batch, 'delete')
        .mockResolvedValue(mockBatch as any);

      const result = await batchService.deleteBatch('1');

      expect(result).toBe(mockBatch);
    });
  });
});
