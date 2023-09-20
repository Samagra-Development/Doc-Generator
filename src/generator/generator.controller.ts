import { Body, Controller, Delete, Get, Param, Post } from '@nestjs/common';
import { GeneratorService } from './generator.service';
import { BatchRequest, BatchResponse, GenRequest, GenResponse } from './types';
import { ApiOperation, ApiResponse, ApiTags } from '@nestjs/swagger';
import { BatchService } from './batch.service';
import { Batch } from '@prisma/client';
import {
  Ctx,
  MessagePattern,
  Payload,
  RmqContext,
} from '@nestjs/microservices';

@Controller('generate')
@ApiTags('generator')
export class GeneratorController {
  constructor(
    private readonly generateService: GeneratorService,
    private readonly batchService: BatchService,
  ) {}

  @MessagePattern('process-batch')
  async processBatch(
    @Payload() data: { batchId: string },
    @Ctx() ctx: RmqContext,
  ) {
    const channel = ctx.getChannelRef();
    const originalMsg = ctx.getMessage();
    try {
      // simulating processing time
      // await new Promise((resolve) => setTimeout(resolve, 5000));
      await this.batchService.processBatch(data.batchId);
      await channel.ack(originalMsg);
    } catch (error: any) {
      throw new Error(error);
    }
  }

  @Post('/render')
  @ApiOperation({ summary: 'For realtime rendering of templates' })
  @ApiResponse({
    status: 200,
    description: 'processed string',
    type: GenResponse,
  })
  generateTemplate(@Body() body: GenRequest): Promise<string | string[]> {
    return this.generateService.generate(body);
  }

  @ApiOperation({ summary: 'For submitting batches of templates' })
  @ApiResponse({
    status: 201,
    description: 'Batch created',
    type: BatchResponse,
  })
  @ApiResponse({
    status: 404,
    description: 'Template not found',
  })
  @Post('/batches')
  async submitNewBatch(@Body() body: BatchRequest): Promise<Batch> {
    return await this.batchService.createBatchAndEnqueue(body);
  }

  @ApiOperation({ summary: 'For getting all  submitted batches' })
  @ApiResponse({
    status: 200,
    description: 'Batches',
    type: BatchResponse,
  })
  @Get('/batches')
  async getBatches(): Promise<Batch[]> {
    return await this.batchService.getBatches();
  }

  @ApiOperation({ summary: 'For getting a submitted batch' })
  @ApiResponse({
    status: 200,
    description: 'Batch',
    type: BatchResponse,
  })
  @ApiResponse({
    status: 404,
    description: 'Batch not found',
  })
  @Get('/batches/:id')
  async getBatch(@Param('id') id: string): Promise<Batch> {
    return await this.batchService.getBatch(id);
  }

  @ApiOperation({ summary: 'For deleting a submitted batch' })
  @ApiResponse({
    status: 200,
    description: 'Batch deleted',
    type: BatchResponse,
  })
  @ApiResponse({
    status: 404,
    description: 'Batch not found',
  })
  @Delete('/batches/:id')
  async deleteBatch(@Param('id') id: string): Promise<Batch> {
    return await this.batchService.deleteBatch(id);
  }
}
