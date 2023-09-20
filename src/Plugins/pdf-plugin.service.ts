import { Injectable } from '@nestjs/common';
import { Plugin, PluginOutput } from './pdf-plugin.interfaces';
import * as path from 'path';
import * as fs from 'fs';
import { TDocumentDefinitions } from 'pdfmake/interfaces';
import { PdfInputPlugin } from './pdf-input-plugin'; // Import PdfInputPlugin

@Injectable()
export class PluginService implements Plugin {
  constructor(private readonly pdfInputPlugin: PdfInputPlugin) {} // Use PdfInputPlugin here

  validateTemplate(template: string): boolean {
    if (template === 'PDF') {
      return true;
    } else {
      return false;
    }
  }

  getName(): string {
    return 'PDF Plugin';
  }

  getSupportedOutputs(): string[] {
    return ['PDF', 'Image'];
  }

  getSupportedInputs(): string[] {
    return ['PDF'];
  }
  //

  public async transformPdfToImage(pdfFilePath: string): Promise<PluginOutput> {
    const outDir = path.dirname(pdfFilePath);
    const outPrefix = path.basename(pdfFilePath, path.extname(pdfFilePath));

    const pdfImageOptions = {
      format: 'jpeg',
      out_dir: outDir,
      out_prefix: outPrefix,
      page: null,
    };

    try {
      await this.pdfInputPlugin.transformPdfToImage(pdfFilePath);

      console.log('Successfully converted');

      const images = fs.readdirSync(outDir).map((fileName) => ({
        url: path.join(outDir, fileName),
      }));

      return { images: images };
    } catch (error) {
      console.error('Error converting PDF to image:', error);
      throw new Error('PDF to image conversion failed');
    }
  }

  transformToPDFMake(
    inputType: string,
    outputType: string,
  ): Promise<PluginOutput> {
    throw new Error('Method not implemented.');
  }

  transformPdfToDocsx(pdfFilePath: string): Promise<PluginOutput> {
    throw new Error('Method not implemented.');
  }

  transformPdfToExcalidraw(inputFile: string): PluginOutput {
    throw new Error('Method not implemented.');
  }

  transformPdfToDrawio(inputFile: string): PluginOutput {
    throw new Error('Method not implemented.');
  }

  transformPdfMakeToMermaid(pdfMakeContent: TDocumentDefinitions): string {
    throw new Error('Method not implemented.');
  }

  isSupportedConversion(inputType: string, outputType: string): boolean {
    return true;
  }
  generateDoc(outputType: string): Promise<PluginOutput> {
    throw new Error('Method not implemented.');
  }
}
