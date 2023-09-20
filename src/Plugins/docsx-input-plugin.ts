import * as path from 'path';
import * as mammoth from 'mammoth';
import * as puppeteer from 'puppeteer';
import { PluginOutput } from './pdf-plugin.interfaces'; //

export class DocxInputPlugin {
  public async convertDocxToPdf(docxFilePath: string): Promise<PluginOutput> {
    try {
      const outputPdfPath = `./DocxToPdf.pdf`;
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
  public async convertDocxToImages(
    docxFilePath: string,
  ): Promise<PluginOutput> {
    try {
      const imagesFolderPath = path.join(__dirname, './generatedImages');
      const htmlContent = await this.convertDocxToHtml(docxFilePath);
      await this.htmlToImages(htmlContent, imagesFolderPath);

      console.log('Images generated successfully');
      return { folder: imagesFolderPath };
    } catch (error) {
      console.error('Error generating images:', error);
      throw new Error('Failed to convert DOCX to images');
    }
  }

  private async htmlToImages(
    htmlContent: string,
    imagesFolderPath: string,
  ): Promise<void> {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.setContent(htmlContent);

    const elements = await page.$$('img'); // Get all img elements in the HTML
    for (let i = 0; i < elements.length; i++) {
      const imgElement = elements[i];
      const imgSrc = await imgElement.evaluate((node) =>
        node.getAttribute('src'),
      );
      const imgName = `image_${i}.png`;
      const imgPath = path.join(imagesFolderPath, imgName);

      // Wait for images to load
      await page.waitForFunction(() => {
        const images = document.getElementsByTagName('img');
        return Array.from(images).every((img) => img.complete);
      });

      await imgElement.screenshot({ path: imgPath });
    }

    await browser.close();
  }
}
