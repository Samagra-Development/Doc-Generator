import { Injectable } from '@nestjs/common';
import { CreateBatchDto } from './dto/create-batch.dto';
//import { UpdateBatchDto } from './dto/update-batch.dto';
import { PrismaService } from './../prisma/prisma.service';

@Injectable()
export class BatchesService {
  constructor(private prisma: PrismaService) {}

  create(createBatchDto: CreateBatchDto) {
    return this.prisma.batch.create({ data: createBatchDto });
  }

  // findAll() {
  //   return `This action returns all batches`;
  // }

  // findOne(id: number) {
  //   return `This action returns a #${id} batch`;
  // }

  // update(id: number, updateBatchDto: UpdateBatchDto) {
  //   return `This action updates a #${id} batch`;
  // }

  // remove(id: number) {
  //   return `This action removes a #${id} batch`;
  // }
}
