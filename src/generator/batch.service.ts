import { HttpException, Inject, Injectable } from '@nestjs/common';
import { Batch, BatchStatus } from '@prisma/client';
import { BatchRequest } from './types';
import { v4 as uuidv4 } from 'uuid';
import { PrismaService } from 'src/prisma/prisma.service';
import { ClientProxy } from '@nestjs/microservices';
import { RenderService } from 'templater';

@Injectable()
export class BatchService {
  constructor(
    @Inject('BATCH_PROCESSING')
    private readonly batchProcessingClient: ClientProxy,
    private readonly prisma: PrismaService,
    private readonly renderService: RenderService,
  ) {}

  // is used for processing batches by RabbitMQ
  async processBatch(uid: string) {
    const batch = await this.prisma.batch.findUnique({
      where: {
        id: uid,
      },
      include: {
        template: true,
      },
    });
    if (!batch) {
      throw new HttpException(`Batch not found with ID: ${uid}`, 404);
    }
    const { template, payload } = batch;
    const { templateType, content } = template;
    const output: string[] = [];
    for (const data of payload) {
      const { processed } = await this.renderService.renderTemplate({
        templateContent: content,
        data,
        engineType: templateType,
      });
      output.push(processed);
    }
    await this.prisma.batch.update({
      where: {
        id: uid,
      },
      data: {
        output: output,
        status: BatchStatus.done,
      },
    });
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
      throw new HttpException(
        `Template not found or deleted with ID: ${templateID}`,
        404,
      );
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
    await this.batchProcessingClient.emit('process-batch', {
      batchId: batchId,
    });
    return batch;
  }

  async getBatch(id: string): Promise<Batch> {
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
