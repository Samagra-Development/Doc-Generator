import { ApiProperty } from '@nestjs/swagger';

export class CreateBatchDto {
  @ApiProperty()
  id: string;

  @ApiProperty()
  createdAt: Date;

  @ApiProperty()
  updatedAt: Date;

  @ApiProperty()
  name: string;

  @ApiProperty({ required: false, nullable: true })
  description: string | null;

  @ApiProperty()
  templateType: string;

  @ApiProperty()
  templateInput: string;

  @ApiProperty()
  dataInput: string;

  @ApiProperty()
  status: string;

  @ApiProperty()
  output: string;
}
