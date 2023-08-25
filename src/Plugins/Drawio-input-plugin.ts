import * as fs from 'fs';
import * as path from 'path';
import { PluginOutput } from './pdf-plugin.interfaces';
import puppeteer from 'puppeteer';
import { parseString } from 'xml2js';

export class DrawioInputPlugin {
  public async convertDrawioFileToPdf(
    drawioFilePath: string,
  ): Promise<PluginOutput> {
    try {
      // Read Draw.io file content
      const drawioXml = fs.readFileSync(drawioFilePath, 'utf-8');

      // Parse Draw.io XML to JavaScript object
      let drawioJson;
      parseString(drawioXml, (err, result) => {
        if (err) {
          throw err;
        }
        drawioJson = result;
      });

      // Convert Draw.io JSON object to HTML (manually or using a templating engine)
      const drawioHtml = `<div>${JSON.stringify(drawioJson)}</div>`;

      // Launch a headless browser instance
      const browser = await puppeteer.launch();
      const page = await browser.newPage();

      // Set the content of the page to the Draw.io HTML
      await page.setContent(drawioHtml);

      // Generate a PDF from the rendered HTML content
      const pdfBuffer = await page.pdf();

      // Close the browser
      await browser.close();

      const pdfFilePath = path.join(__dirname, 'generatedDrawio.pdf'); // Adjust the path accordingly
      fs.writeFileSync(pdfFilePath, pdfBuffer);

      console.log('Draw.io PDF generated successfully');

      return { file: 'generatedDrawio.pdf' };
    } catch (error) {
      console.error('Error converting Draw.io file to PDF:', error);
      throw new Error('Failed to convert Draw.io file to PDF');
    }
  }
}
