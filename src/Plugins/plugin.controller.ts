import { Controller, Post, Get, Param, Dependencies } from '@nestjs/common';
import * as fs from 'fs';
import { PluginService } from './pdf-plugin.service';
import { PluginOutput } from './pdf-plugin.interfaces';
import { PdfOutputPlugin } from './pdf-output-plugin';
import { PdfInputPlugin } from './pdf-input-plugin';
import { DocxOutputPlugin } from './docsx-output-plugin';
import { DocxInputPlugin } from './docsx-input-plugin';
import { ImageOutputPlugin } from './image-output-plugin'; // Import the ImageOutputPlugin
import { ImageInputPlugin } from './image-input-plugin';

@Controller('plugin')
@Dependencies(PluginService)
export class PluginController {
  private pdfOutputPlugin!: PdfOutputPlugin;
  private pdfInputPlugin!: PdfInputPlugin;
  private docxOutputPlugin!: DocxOutputPlugin;
  private docxInputPlugin!: DocxInputPlugin;
  private imageOutputPlugin!: ImageOutputPlugin; // Add the ImageOutputPlugin
  private imageInputPlugin!: ImageInputPlugin;
  constructor(private readonly pluginService: PluginService) {}

  onModuleInit() {
    this.pdfOutputPlugin = new PdfOutputPlugin();
    this.pdfInputPlugin = new PdfInputPlugin();
    this.docxOutputPlugin = new DocxOutputPlugin();
    this.docxInputPlugin = new DocxInputPlugin();
    this.imageOutputPlugin = new ImageOutputPlugin(); // Initialize the ImageOutputPlugin
    this.imageInputPlugin = new ImageInputPlugin();
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

  @Get('convert-img-to-pdf')
  async convertImageToPdf(): Promise<PluginOutput> {
    try {
      const imageFilePath = './generatedImage.png'; // Replace with the actual path to the image
      const pdfFilePath = './generatedImage.pdf';

      await this.imageInputPlugin.convertImageToPdf(imageFilePath, pdfFilePath);

      return { file: 'generatedImage.pdf' };
    } catch (error: any) {
      console.error('Error converting image to PDF:', error.message);
      throw new Error('Failed to convert image to PDF');
    }
  }

  @Get('convert-docx-to-pdf')
  async convertDocxToPdf(): Promise<PluginOutput> {
    try {
      const docxFilePath = './generatedDocxDocument.docx'; // Adjust the path accordingly
      const pdfFilePath = './generated-document.pdf';

      const pluginOutput = await this.docxInputPlugin.convertDocxToPdf(
        docxFilePath,
      );

      if (!pluginOutput.file) {
        throw new Error('Generated PDF file not found.');
      }

      fs.renameSync(pluginOutput.file, pdfFilePath);

      return { file: 'generated-document.pdf' };
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
