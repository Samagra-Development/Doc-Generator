import { Module } from '@nestjs/common';
import { MulterModule } from '@nestjs/platform-express'; // Import MulterModule
import { PluginController } from './plugin.controller';
import { PluginService } from './pdf-plugin.service';
import { PdfInputPlugin } from './pdf-input-plugin';

@Module({
  imports: [
    MulterModule.register({
      dest: './uploads', // Specify the directory to store uploaded file
    }),
  ],
  controllers: [PluginController],
  providers: [PluginService, PdfInputPlugin],
})
export class PluginModule {}
