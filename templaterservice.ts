import { Injectable } from '@nestjs/common';
import axios from 'axios';
import { CreateBatchDto } from './dto/create-batch.dto';

@Injectable()
export class TemplaterService {
  async createBatch(createBatchDto: CreateBatchDto) {
    // Make API call to Templater to create a new batch
    const response = await axios.post('/templater/batches', createBatchDto);

    // Return the created batch from the response
    return response.data;
  }
}
