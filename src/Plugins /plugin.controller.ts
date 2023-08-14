import {
  Controller,
  Post,
  Body,
  Get,
  Param,
  Dependencies,
} from '@nestjs/common';
import { PluginService } from './pdf-plugin.service';
import { PluginOutput } from './pdf-plugin.interfaces';
import { PdfOutputPlugin } from './pdf-output-plugin';
import { PdfInputPlugin } from './pdf-input-plugin';
import { DocxOutputPlugin } from './docsx-output-plugin'; // Import the DocxOutputPlugin
import { DocxInputPlugin } from './docsx-input-plugin';
import { ImageInputPlugin } from './image-input-plugin'; // Import the ImageInputPlugin
import { ImageOutputPlugin } from './image-output-plugin'; // Import the ImageOutputPlugin

@Controller('plugin')
@Dependencies(PluginService)
export class PluginController {
  private pdfOutputPlugin!: PdfOutputPlugin;
  private pdfInputPlugin!: PdfInputPlugin;
  private docxOutputPlugin!: DocxOutputPlugin;
  private docxInputPlugin!: DocxInputPlugin;
  private imageOutputPlugin!: ImageOutputPlugin; // Add the ImageOutputPlugin

  constructor(private readonly pluginService: PluginService) {}

  onModuleInit() {
    this.pdfOutputPlugin = new PdfOutputPlugin();
    this.pdfInputPlugin = new PdfInputPlugin();
    this.docxOutputPlugin = new DocxOutputPlugin();
    this.docxInputPlugin = new DocxInputPlugin();
    this.imageOutputPlugin = new ImageOutputPlugin(); // Initialize the ImageOutputPlugin
  }

  @Post('generate-doc/:outputType')
  async generateDocument(
    @Param('outputType') outputType: string,
  ): Promise<PluginOutput> {
    try {
      if (outputType === 'PDF') {
        return this.pdfOutputPlugin.generateDoc(outputType);
      } else if (outputType === 'DOCX') {
        return this.docxOutputPlugin.generateDoc(outputType);
      } else if (outputType === 'IMG') {
        // Add this condition for image generation
        return this.imageOutputPlugin.generateImage(outputType);
      } else {
        throw new Error('Unsupported output type');
      }
    } catch (error: any) {
      console.error('Error generating document:', error.message);
      throw new Error('Failed to generate document');
    }
  }

  @Post('convert-docx-to-pdf/:docxFilePath')
  async convertDocxToPdf(
    @Param('docxFilePath') docxFilePath: string,
  ): Promise<PluginOutput> {
    try {
      return this.docxInputPlugin.convertDocxToPdf(docxFilePath);
    } catch (error: any) {
      console.error('Error converting DOCX to PDF:', error.message);
      throw new Error('Failed to convert DOCX to PDF');
    }
  }

  @Get()
  getPluginStatus(): string {
    return 'Plugin is running!';
  }

  @Get('/pdf-to-image')
  async convertPdfToImage(): Promise<{ images?: { url: string }[] }> {
    const pdfFilePath = './generatedDocument.pdf';
    try {
      const pluginOutput = await this.pdfInputPlugin.transformPdfToImage(
        pdfFilePath,
      );

      if (pluginOutput.images) {
        const images = pluginOutput.images;
        images.forEach((image: { url: string }) => {
          console.log('Image URL:', image.url);
        });
      }

      return { images: pluginOutput.images };
    } catch (error) {
      console.error('Error converting PDF to image:', error);
      throw new Error('PDF to image conversion failed');
    }
  }

  @Post('create-default-pdf')
  async createDefaultPdf(): Promise<PluginOutput> {
    try {
      return this.pdfOutputPlugin.createDefaultPdf();
    } catch (error: any) {
      console.error('Error creating default PDF:', error.message);
      throw new Error('Failed to create default PDF');
    }
  }
}
