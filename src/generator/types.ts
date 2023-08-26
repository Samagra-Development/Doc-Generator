import { ApiProperty } from '@nestjs/swagger';
import { TemplateType } from '@prisma/client';

export class GenRequest {
  @ApiProperty({
    description: 'Template to be rendered',
    type: String,
  })
  templateContent: string;

  @ApiProperty({
    description: 'Data to be rendered in json format',
    type: Object,
    example: {
      variable_name: 'variable_value',
    },
  })
  data: any;

  @ApiProperty({
    description: 'Type of template',
    enum: TemplateType,
  })
  engineType: TemplateType;
}

export class GenResponse {
  @ApiProperty({
    description: 'Processed string',
    type: String,
  })
  processed: string | string[];
}

export class BatchRequest {
  @ApiProperty({
    description: 'Type of template',
    enum: TemplateType,
  })
  templateType: TemplateType;
  @ApiProperty({
    description: 'Template id',
    type: Number,
  })
  templateID: number;
  @ApiProperty({
    description: 'Data to be rendered in json format',
    type: Object,
    example: {
      variable_name: 'variable_value',
    },
  })
  payload: any[];
}

export class BatchResponse {
  @ApiProperty({
    description: 'Batch id',
    type: String,
  })
  id: string;
  @ApiProperty({
    description: 'Date created',
    type: Date,
  })
  createdAt: Date;
  @ApiProperty({
    description: 'Type of template',
    enum: TemplateType,
  })
  templateType: TemplateType;
  @ApiProperty({
    description: 'Template id',
    type: Number,
  })
  templateID: number;
  @ApiProperty({
    description: 'Data to be rendered in json format',
    type: Object,
    example: {
      variable_name: 'variable_value',
    },
  })
  payload: any[];
  @ApiProperty({
    description: 'Status of batch',
    enum: ['submitted', 'queued', 'running', 'done', 'aborted'],
  })
  status: string;
  @ApiProperty({
    description: 'Output as an array of links',
    type: String,
  })
  output: string[];
  @ApiProperty({
    description: 'Type of output',
    enum: ['png', 'jpeg', 'html', 'pdf', 'qr'],
  })
  outputType: string;
}
