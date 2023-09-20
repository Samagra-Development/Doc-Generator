import { ApiProperty } from '@nestjs/swagger';

export enum TemplateType {
  JSTL = 'JSTL',
  EJS = 'EJS',
  JINJA = 'JINJA',
}
