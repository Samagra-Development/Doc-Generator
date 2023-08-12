import { ApiProperty } from '@nestjs/swagger';

export class TemplateTest {
  @ApiProperty({ type: String, description: 'Template content' })
  content: string;

  @ApiProperty({ type: String, description: 'Template id' })
  id: string;
}

export enum TemplateType {
  JSTL = 'JSTL',
  EJS = 'EJS',
  JINJA = 'JINJA',
}
