import { Body, Controller, Post } from '@nestjs/common';
import { GeneratorService } from './generator.service';
import { GenReq, GenRes } from './types';
import { ApiOperation, ApiResponse, ApiTags } from '@nestjs/swagger';

@Controller('generate')
@ApiTags('generator')
export class GeneratorController {
  constructor(private generateService: GeneratorService) {}

  @Post('/')
  @ApiOperation({ summary: 'For realtime rendering of templates' })
  @ApiResponse({
    status: 200,
    description: 'processed string',
    type: GenRes,
  })
  gen(@Body() body: GenReq): Promise<string | string[]> {
    const res = this.generateService.generate(body);
    return res;
  }
}
