import { PluginOutput } from './pdf-plugin.interfaces'; // Make sure you import the correct interface
import puppeteer from 'puppeteer';

export class MermaidInputPlugin {
  public async convertMermaidToPdf(mermaidContent: any): Promise<PluginOutput> {
    try {
      const pdfFilePath = `./generatedMermaid.pdf`; // Adjust the path

      // Launch a headless browser
      const browser = await puppeteer.launch();
      const page = await browser.newPage();

      // Set the content of the page to the Mermaid diagram HTML
      const htmlContent = `<div class="mermaid">${mermaidContent}</div>`;
      await page.setContent(htmlContent);

      // Generate a PDF from the Mermaid diagram HTML
      await page.pdf({ path: pdfFilePath, format: 'A4' });

      await browser.close();

      console.log('Mermaid PDF generated successfully');

      return { file: 'generatedMermaid.pdf' };
    } catch (error) {
      console.error('Error generating Mermaid PDF:', error);
      throw new Error('Failed to convert Mermaid to PDF');
    }
  }
}
