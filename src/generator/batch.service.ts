import { HttpException, Inject, Injectable } from '@nestjs/common';
import { Batch } from '@prisma/client';
import { BatchRequest } from './types';
import { v4 as uuidv4 } from 'uuid';
import { PrismaService } from 'src/prisma/prisma.service';
import { ClientProxy } from '@nestjs/microservices';

@Injectable()
export class BatchService {
  constructor(
    @Inject('BATCH_PROCESSING')
    private readonly batchProcessingClient: ClientProxy,
    private readonly prisma: PrismaService,
  ) {}

  async processBatch(data: any) {
    console.log(data + 'rec');
  }

  async createBatchAndEnqueue(data: BatchRequest): Promise<Batch> {
    const { templateID, payload } = data;
    const batchId = uuidv4();
    const isTemplate = await this.prisma.template.findUnique({
      where: {
        id: templateID,
      },
    });
    if (!isTemplate) {
      throw new HttpException(`Template not found with ID: ${templateID}`, 404);
    }
    const batch = await this.prisma.batch.create({
      data: {
        id: batchId,
        payload,
        template: {
          connect: {
            id: templateID,
          },
        },
      },
      include: {
        template: true,
      },
    });
    await this.batchProcessingClient.emit('process-batch', { batchId: 'test' });
    return batch;
  }

  async getBatch(id: string) {
    const batch = await this.prisma.batch.findUnique({
      where: {
        id,
      },
      include: {
        template: true,
      },
    });
    if (!batch) {
      throw new HttpException(`Batch not found with ID: ${id}`, 404);
    }
    return batch;
  }

  async getBatches(): Promise<Batch[]> {
    const batches = await this.prisma.batch.findMany({
      include: {
        template: true,
      },
    });
    return batches;
  }

  async deleteBatch(id: string) {
    const batch = await this.prisma.batch.delete({
      where: {
        id,
      },
    });
    if (!batch) {
      throw new HttpException(`Batch not found with ID: ${id}`, 404);
    }
    return batch;
  }
}
