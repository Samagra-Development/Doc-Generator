import { Controller, Get } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { Transport } from '@nestjs/microservices';
import { ApiOperation, ApiResponse } from '@nestjs/swagger';
import { DiskHealthIndicator, HealthCheck, HealthCheckService, HttpHealthIndicator, MemoryHealthIndicator, MicroserviceHealthIndicator } from '@nestjs/terminus';
import { PrismaHealthIndicator } from 'prisma/prisma.health';
import { AppService } from './app.service';

@Controller()
export class AppController {
  constructor(
    private readonly appService: AppService,
    private configService: ConfigService,
    private healthCheckService: HealthCheckService,
    private http: HttpHealthIndicator,
    private microservice: MicroserviceHealthIndicator,
    private prismaIndicator: PrismaHealthIndicator,
    private memory: MemoryHealthIndicator,
    private readonly disk: DiskHealthIndicator,
    ) {}

  @Get()
  @HealthCheck()
  @ApiOperation({ summary: 'Get Health Check Status' })
  @ApiResponse({ status: 200, description: 'Result Report for All the Health Check Services' })
  async checkHealth() {
    return this.healthCheckService.check([
      async () => this.prismaIndicator.isHealthy('db'),
      async () => this.microservice.pingCheck('rmq', {
        transport: Transport.RMQ,
      }),
      async () => this.disk.checkStorage('storage', { path: '/', thresholdPercent: this.configService.get<number>('DISK_THRESHOLD_CHECK') || 0.5}),
      async () => this.memory.checkHeap('memory_heap', this.configService.get<number>('HEAP_SIZE_CHECK') || 150 * 1024 * 1024),
      async () => this.memory.checkRSS('memory_rss', this.configService.get<number>('RSS_SIZE_CHECK') || 150 * 1024 * 1024),
    ])
  }
}
