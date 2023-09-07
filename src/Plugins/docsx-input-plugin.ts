import * as path from 'path';
import * as mammoth from 'mammoth';
import * as puppeteer from 'puppeteer';
import { PluginOutput } from './pdf-plugin.interfaces';

export class DocxInputPlugin {
  public async convertDocxToPdf(docxFilePath: string): Promise<PluginOutput> {
    try {
      const outputPdfPath = path.join(__dirname, './generatedPdfDocument.pdf');
      const htmlContent = await this.convertDocxToHtml(docxFilePath);
      await this.htmlToPdf(htmlContent, outputPdfPath);

      console.log('PDF file generated successfully');
      return { file: outputPdfPath };
    } catch (error) {
      console.error('Error generating PDF:', error);
      throw new Error('Failed to convert DOCX to PDF');
    }
  }

  private async convertDocxToHtml(docxFilePath: string): Promise<string> {
    const result = await mammoth.convertToHtml({ path: docxFilePath });
    return result.value;
  }

  private async htmlToPdf(htmlContent: string, pdfPath: string): Promise<void> {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.setContent(htmlContent);
    await page.pdf({ path: pdfPath, format: 'A4' });

    await browser.close();
  }
}
