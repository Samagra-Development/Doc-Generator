import { Controller, Get, Post, Body, Param, Delete } from '@nestjs/common';
import { ApiOperation, ApiResponse, ApiTags } from '@nestjs/swagger';
import { TemplateService } from './template.service';
import { CreateTemplateDto } from './types';

@Controller('template')
@ApiTags('template')
export class TemplateController {
  constructor(private readonly templateService: TemplateService) {}

  @ApiOperation({ summary: 'For creating templates' })
  @ApiResponse({
    status: 201,
    description: 'Template created',
    type: CreateTemplateDto,
  })
  @Post()
  create(@Body() createTemplateDto: CreateTemplateDto) {
    return this.templateService.create(createTemplateDto);
  }

  @ApiOperation({ summary: 'For getting all templates' })
  @ApiResponse({
    status: 200,
    description: 'Templates',
    type: CreateTemplateDto,
  })
  @Get()
  findAll() {
    return this.templateService.getTemplates();
  }

  @ApiOperation({ summary: 'For getting a template' })
  @ApiResponse({
    status: 200,
    description: 'Template',
    type: CreateTemplateDto,
  })
  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.templateService.getTemplate(+id);
  }

  @ApiOperation({ summary: 'For deleting a template' })
  @ApiResponse({
    status: 200,
    description: 'Template deleted',
    type: CreateTemplateDto,
  })
  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.templateService.remove(+id);
  }
}
