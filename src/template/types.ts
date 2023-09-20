import { ApiProperty } from '@nestjs/swagger';
import { TemplateType } from '@prisma/client';

export class CreateTemplateDto {
  @ApiProperty({
    description: 'Template content',
    type: String,
  })
  content: string;
  @ApiProperty({
    description: 'Type of template',
    enum: TemplateType,
  })
  templateType: TemplateType;
}
