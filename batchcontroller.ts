import { Controller, Post, Body } from '@nestjs/common';
import { BatchService } from './batch.service';
import { CreateBatchDto } from './dto/create-batch.dto';

@Controller('batches')
export class BatchController {
  constructor(private readonly batchService: BatchService) {}

  @Post()
  async createBatch(@Body() createBatchDto: CreateBatchDto) {
    return this.batchService.createBatch(createBatchDto);
  }
}
