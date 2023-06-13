import { Module } from '@nestjs/common';
import { BatchesService } from './batches.service';
import { BatchesController } from './batches.controller';

@Module({
  controllers: [BatchesController],
  providers: [BatchesService],
})
export class BatchesModule {}
