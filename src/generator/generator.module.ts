import { Module } from '@nestjs/common';
import { RenderModule } from 'templater';
import { GeneratorController } from './generator.controller';
import { GeneratorService } from './generator.service';

@Module({
  imports: [RenderModule],
  providers: [GeneratorService],
  controllers: [GeneratorController],
})
export class GeneratorModule {}
