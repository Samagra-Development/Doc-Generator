import { Module } from '@nestjs/common';
import { PluginController } from './plugin.controller';
import { PluginService } from './pdf-plugin.service';
import { PdfInputPlugin } from './pdf-input-plugin';

@Module({
  controllers: [PluginController],
  providers: [PluginService, PdfInputPlugin],
})
export class PluginModule {}
