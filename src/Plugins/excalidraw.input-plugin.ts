import * as fs from 'fs';
import * as path from 'path';
import { PluginOutput } from './pdf-plugin.interfaces'; // Make sure you import the correct interface
import puppeteer from 'puppeteer';

export class ExcalidrawInputPlugin {
  public async convertExcalidrawToPdf(
    excalidrawContent: string,
  ): Promise<PluginOutput> {
    try {
      const pdfFilePath = path.join(__dirname, 'generatedExcalidraw.pdf'); // Adjust the path

      // Launch a headless browser
      const browser = await puppeteer.launch();
      const page = await browser.newPage();

      // Set the content of the page to the Excalidraw SVG
      await page.setContent(excalidrawContent);

      // Generate a PDF from the SVG //
      await page.pdf({ path: pdfFilePath, format: 'A4' });

      await browser.close();

      console.log('Excalidraw PDF generated successfully');

      return { file: pdfFilePath };
    } catch (error) {
      console.error('Error generating Excalidraw PDF:', error);
      throw new Error('Failed to convert Excalidraw to PDF');
    }
  }
}
