import { ApiProperty } from '@nestjs/swagger';
import { TemplateType, TemplateTest } from '../app.interface';

export class GenReq {
  @ApiProperty({
    description: 'Template to be rendered',
    type: TemplateTest,
  })
  template: TemplateTest;

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

export class GenRes {
  @ApiProperty({
    description: 'Processed string',
    type: String,
  })
  processed: string | string[];
}
