import { Test, TestingModule } from '@nestjs/testing';
import { BatchService } from './batch.service';
import { PrismaService } from '../prisma/prisma.service';
import { RenderService } from 'templater';
import { HttpException } from '@nestjs/common';
import { BatchStatus } from '@prisma/client';
import { ClientProxy } from '@nestjs/microservices';

describe('BatchService', () => {
  let batchService: BatchService;
  let prismaService: PrismaService;
  let renderService: RenderService;
  let batchProcessingClient: ClientProxy;

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
    batchProcessingClient = module.get<ClientProxy>('BATCH_PROCESSING');
  });

  describe('processBatchTest', () => {
    it('should throw error when batch not found', async () => {
      jest.spyOn(prismaService.batch, 'findUnique').mockResolvedValue(null);

      await expect(batchService.processBatchTest('1')).rejects.toThrow(
        new HttpException(`Batch not found with ID: 1`, 404),
      );
    });

    it('should process batch', async () => {
      const mockBatch = {
        id: 'test',
        template: {
          id: '1',
          templateType: 'JSTL',
          content: '${content}',
        },
        payload: [
          {
            content: 'content',
          },
        ],
      };
      const mockRendered = {
        processed: 'content',
      };
      jest
        .spyOn(prismaService.batch, 'findUnique')
        .mockResolvedValue(mockBatch as any);
      jest
        .spyOn(renderService, 'renderTemplate')
        .mockResolvedValue(mockRendered as any);
      jest.spyOn(prismaService.batch, 'update').mockResolvedValue(null);
      await batchService.processBatchTest('test');
      expect(prismaService.batch.update).toHaveBeenCalledWith({
        where: {
          id: 'test',
        },
        data: {
          output: ['content'],
          status: BatchStatus.done,
        },
      });
    });
  });

  describe('createBatchAndEnqueue', () => {
    it('should create batch and enqueue message', async () => {
      // Mock PrismaService findUnique method
      const mockTemplateID = 1;
      const mockTemplate = {
        id: mockTemplateID,
        templateType: 'JSTL',
        content: '${content}',
      };
      const mockPayload = [
        {
          content: 'content',
        },
      ];
      jest
        .spyOn(prismaService.template, 'findUnique')
        .mockResolvedValue(mockTemplate as any);

      // Mock PrismaService create method
      const mockBatch = {
        id: 'batch_id',
        payload: mockPayload,
        template: { id: mockTemplateID },
      };
      jest.spyOn(prismaService.batch, 'create').mockResolvedValue(mockBatch);

      // Mock ClientProxy emit method
      const mockEmit = jest
        .spyOn(batchProcessingClient, 'emit')
        .mockImplementation();

      // Call the method and verify
      const result = await batchService.createBatchAndEnqueue({
        templateID: mockTemplateID,
        payload: mockPayload,
        templateType: 'JSTL',
      });

      // Verify Prisma calls
      expect(prismaService.template.findUnique).toHaveBeenCalledWith({
        where: { id: mockTemplateID },
      });

      expect(prismaService.batch.create).toHaveBeenCalledWith({
        data: {
          id: expect.any(String),
          payload: mockPayload,
          template: { connect: { id: mockTemplateID } },
        },
        include: { template: true },
      });

      // Verify RabbitMQ operation
      expect(batchProcessingClient.emit).toHaveBeenCalledWith('process-batch', {
        batchId: expect.any(String),
      });

      expect(result).toEqual(mockBatch);
    });
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
