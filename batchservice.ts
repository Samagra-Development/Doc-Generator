import { Injectable } from '@nestjs/common';
import { TemplaterService } from './templater.service';
import { CreateBatchDto } from './dto/create-batch.dto';

@Injectable()
export class BatchService {
  constructor(private readonly templaterService: TemplaterService) {}

  async createBatch(createBatchDto: CreateBatchDto) {
    // Perform any necessary validation or pre-processing here

    // Call the Templater service to create the batch
    const batch = await this.templaterService.createBatch(createBatchDto);

    // Perform any additional operations or post-processing if needed

    return batch;
  }
}
