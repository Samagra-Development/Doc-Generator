import { Controller, Get } from '@nestjs/common';
import { ApiOperation, ApiResponse } from '@nestjs/swagger';
import { AppService } from './app.service';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get('/')
  @ApiOperation({ summary: 'service is alive' })
  @ApiResponse({
    status: 200,
    description: 'Check if service is alive',
  })
  getHello(): string {
    return this.appService.getHello();
  }
}
