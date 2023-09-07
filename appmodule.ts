import { Module } from '@nestjs/common';
import { BatchController } from './batch.controller';
import { BatchService } from './batch.service';
import { TemplaterService } from './templater.service';

@Module({
  imports: [],
  controllers: [BatchController],
  providers: [BatchService, TemplaterService],
})
export class AppModule {}
