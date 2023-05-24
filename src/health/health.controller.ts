import { Controller, Get } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { Transport } from '@nestjs/microservices';
import { ApiOperation, ApiResponse } from '@nestjs/swagger';
import {
  DiskHealthIndicator,
  HealthCheck,
  HealthCheckService,
  MemoryHealthIndicator,
  MicroserviceHealthIndicator,
} from '@nestjs/terminus';
import { PrismaHealthIndicator } from './prisma.health';

@Controller('health')
export class HealthController {
  constructor(
    private readonly configService: ConfigService,
    private readonly healthCheckService: HealthCheckService,
    private readonly microserviceHealthIndicator: MicroserviceHealthIndicator,
    private readonly prismaHealthIndicator: PrismaHealthIndicator,
    private readonly memoryHealthIndicator: MemoryHealthIndicator,
    private readonly diskHealthIndicator: DiskHealthIndicator,
  ) {}

  @Get()
  @HealthCheck()
  @ApiOperation({ summary: 'Get Health Check Status' })
  @ApiResponse({
    status: 200,
    description: 'Result Report for All the Health Check Services',
  })
  async checkHealth() {
    return this.healthCheckService.check([
      async () => this.prismaHealthIndicator.isHealthy('db'),
      async () =>
        this.microserviceHealthIndicator.pingCheck('rmq', {
          transport: Transport.RMQ,
          options: {
            urls: [this.configService.getOrThrow<string>('RMQ_URL')],
          },
        }),
      async () =>
        this.diskHealthIndicator.checkStorage('storage', {
          path: '/',
          thresholdPercent:
            this.configService.get<number>('DISK_THRESHOLD_CHECK') || 0.5,
        }),
      async () =>
        this.memoryHealthIndicator.checkHeap(
          'memory_heap',
          this.configService.get<number>('HEAP_SIZE_CHECK') ||
            150 * 1024 * 1024,
        ),
      async () =>
        this.memoryHealthIndicator.checkRSS(
          'memory_rss',
          this.configService.get<number>('RSS_SIZE_CHECK') || 150 * 1024 * 1024,
        ),
    ]);
  }
}
