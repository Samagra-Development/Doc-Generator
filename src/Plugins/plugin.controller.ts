import {
  Controller,
  Post,
  Query,
  UseInterceptors,
  Res,
  Get,
  Body,
  Param,
  Dependencies,
} from '@nestjs/common';
import * as fs from 'fs';
import { PluginService } from './pdf-plugin.service';
import { PluginOutput } from './pdf-plugin.interfaces';
import { PdfOutputPlugin } from './pdf-output-plugin';
import { PdfInputPlugin } from './pdf-input-plugin';
import { DocxOutputPlugin } from './docsx-output-plugin';
import { DocxInputPlugin } from './docsx-input-plugin';
import { ImageOutputPlugin } from './image-output-plugin'; // Import the ImageOutputPlugin
import { ImageInputPlugin } from './image-input-plugin';
import { DrawioInputPlugin } from './Drawio-input-plugin';
import * as path from 'path';
import { parseString } from 'xml2js'; // Import parseString from xml2js
import puppeteer from 'puppeteer';
import { ExcalidrawInputPlugin } from './excalidraw.input-plugin'; // Adjust the import path
import { MermaidInputPlugin } from './Mermaid.input.plugin'; // Adjust the import path

@Controller('plugin')
@Dependencies(PluginService)
export class PluginController {
  private pdfOutputPlugin!: PdfOutputPlugin;
  private pdfInputPlugin!: PdfInputPlugin;
  private docxOutputPlugin!: DocxOutputPlugin;
  private docxInputPlugin!: DocxInputPlugin;
  private imageOutputPlugin!: ImageOutputPlugin; // Add the ImageOutputPlugin
  private imageInputPlugin!: ImageInputPlugin;
  private ExcalidrawInputPlugin!: ExcalidrawInputPlugin;
  private MermaidInputPlugin!: MermaidInputPlugin;
  private DrawioInputPlugin!: DrawioInputPlugin;
  constructor(private readonly pluginService: PluginService) {}

  onModuleInit() {
    this.pdfOutputPlugin = new PdfOutputPlugin();
    this.pdfInputPlugin = new PdfInputPlugin();
    this.docxOutputPlugin = new DocxOutputPlugin();
    this.docxInputPlugin = new DocxInputPlugin();
    this.imageOutputPlugin = new ImageOutputPlugin(); // Initialize the ImageOutputPlugin
    this.imageInputPlugin = new ImageInputPlugin();
    this.ExcalidrawInputPlugin = new ExcalidrawInputPlugin();
    this.DrawioInputPlugin = new DrawioInputPlugin();
    this.MermaidInputPlugin = new MermaidInputPlugin();
  }

  @Get()
  getPluginStatus(): string {
    return 'Plugin is running!';
  }

  @Post('generate-pdf')
  async generatePdf(@Body() userInput: string[]): Promise<PluginOutput> {
    try {
      const result = await this.pdfOutputPlugin.generateDoc('pdf', userInput);
      return result;
    } catch (error: any) {
      console.error('Error generating PDF:', error.message);
      throw new Error('Failed to generate PDF');
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
  @Post('generate-docx')
  async generateDocx(@Body() userInput: string[]): Promise<PluginOutput> {
    try {
      const result = await this.docxOutputPlugin.generateDoc('docx', userInput);
      return result;
    } catch (error: any) {
      console.error('Error generating DOCX:', error.message);
      throw new Error('Failed to generate DOCX');
    }
  }
  @Post('generate-image')
  async generateImage(@Body() userInput: string): Promise<PluginOutput> {
    try {
      return await this.imageOutputPlugin.generateImage('img', userInput);
    } catch (error: any) {
      console.error('Error generating image:', error.message);
      throw new Error('Failed to generate image');
    }
  }

  @Get('convert-pdf-to-images')
  async convertPdfToImages(
    @Query('pdfPath') pdfPath: string,
  ): Promise<PluginOutput> {
    try {
      if (!pdfPath) {
        console.error('PDF file path not provided.');
        throw new Error('PDF file path not provided.');
      }

      // Define the output folder where the images will be saved
      const outputFolder = './generatedImages'; // Change this path as needed

      // Call a function to convert the PDF to images (you should implement this function)
      const pluginOutput = await this.pdfInputPlugin.transformPdfToImage(
        pdfPath,
      );

      // Check if the plugin output contains the list of image URLs
      if (pluginOutput.images) {
        const images = pluginOutput.images;
        images.forEach((image: { url: string }) => {
          console.log('Image', image.url);
        });
      }

      return { images: pluginOutput.images };
    } catch (error: any) {
      console.error('Error converting PDF to images:', error.message);
      throw new Error('PDF to images conversion failed');
    }
  }

  @Get('convert-image-to-pdf')
  async convertImageToPdf(
    @Query('imagePath') imagePath: string,
  ): Promise<PluginOutput> {
    try {
      if (!imagePath) {
        console.error('Image file path not provided.');
        throw new Error('Image file path not provided.');
      }

      const pdfFilePath = `./generatedImage.pdf`; // Output PDF file path

      await this.imageInputPlugin.convertImageToPdf(imagePath, pdfFilePath);

      return { pdfPath: pdfFilePath };
    } catch (error: any) {
      console.error('Error converting image to PDF:', error.message);
      throw new Error('Failed to convert image to PDF');
    }
  }

  @Get('convert-docx-to-pdf')
  async convertDocxToPdf(
    @Query('docxPath') docxPath: string,
  ): Promise<PluginOutput> {
    try {
      if (!docxPath) {
        console.error('DOCX file path not provided.');
        throw new Error('DOCX file path not provided.');
      }

      const pluginOutput = await this.docxInputPlugin.convertDocxToPdf(
        docxPath,
      );

      if (!pluginOutput.file) {
        throw new Error('Generated PDF file not found.');
      }

      return { file: 'generatedPdfDocument.pdf' };
    } catch (error: any) {
      console.error('Error converting DOCX to PDF:', error.message);
      throw new Error('Failed to convert DOCX to PDF');
    }
  }

  @Get('convert-docx-to-images')
  async convertDocxToImages(
    @Query('docxPath') docxPath: string,
  ): Promise<PluginOutput> {
    try {
      if (!docxPath) {
        console.error('DOCX file path not provided.');
        throw new Error('DOCX file path not provided.');
      }

      const pluginOutput = await this.docxInputPlugin.convertDocxToImages(
        docxPath,
      );

      if (!pluginOutput.folder) {
        throw new Error('Generated images folder not found.');
      }

      return { folder: pluginOutput.folder };
    } catch (error: any) {
      console.error('Error converting DOCX to images:', error.message);
      throw new Error('Failed to convert DOCX to images');
    }
  }

  @Get('convert-excalidraw-to-pdf')
  async convertExcalidrawToPdf(
    @Query('excalidrawpath') excalidrawContent: string,
  ): Promise<PluginOutput> {
    try {
      if (!excalidrawContent) {
        console.error('Excalidraw content not provided.');
        throw new Error('Excalidraw content not provided.');
      }

      const pluginOutput =
        await this.ExcalidrawInputPlugin.convertExcalidrawToPdf(
          excalidrawContent,
        );

      if (!pluginOutput.file) {
        throw new Error('Generated PDF file not found.');
      }

      return { file: pluginOutput.file }; // Use the correct property from the pluginOutput//
    } catch (error: any) {
      console.error('Error converting Excalidraw to PDF:', error.message);
      throw new Error('Failed to convert Excalidraw to PDF');
    }
  }
  @Get('convert-drawio-to-pdf')
  async convertDrawioToPdf(
    @Query('drawioFilePath') drawioFilePath: string,
  ): Promise<PluginOutput> {
    try {
      if (!drawioFilePath) {
        console.error('Draw.io file path not provided.');
        throw new Error('Draw.io file path not provided.');
      }

      const pluginOutput = await this.DrawioInputPlugin.convertDrawioFileToPdf(
        drawioFilePath,
      );

      if (!pluginOutput.file) {
        throw new Error('Generated PDF file not found.');
      }

      return { file: pluginOutput.file };
    } catch (error: any) {
      console.error('Error converting Draw.io to PDF:', error.message);
      throw new Error('Failed to convert Draw.io to PDF');
    }
  }
}
