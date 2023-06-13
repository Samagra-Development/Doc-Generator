import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Param,
  Delete,
} from '@nestjs/common';
import { BatchesService } from './batches.service';
import { CreateBatchDto } from './dto/create-batch.dto';
//import { UpdateBatchDto } from './dto/update-batch.dto';
import { BatchEntity } from './entities/batch.entity';
import { ApiCreatedResponse, ApiTags } from '@nestjs/swagger';

@Controller('batches')
@ApiTags('batches')
export class BatchesController {
  constructor(private readonly batchesService: BatchesService) {}

  @Post()
  @ApiCreatedResponse({ status: 200, type: BatchEntity })
  async create(@Body() createBatchDto: CreateBatchDto) {
    return new BatchEntity(await this.batchesService.create(createBatchDto));
  }
  // @Get()
  // findAll() {
  //   return this.batchesService.findAll();
  // }

  // @Get(':id')
  // findOne(@Param('id') id: string) {
  //   return this.batchesService.findOne(+id);
  // }

  // @Patch(':id')
  // update(@Param('id') id: string, @Body() updateBatchDto: UpdateBatchDto) {
  //   return this.batchesService.update(+id, updateBatchDto);
  // }

  // @Delete(':id')
  // remove(@Param('id') id: string) {
  //   return this.batchesService.remove(+id);
  //}
}
