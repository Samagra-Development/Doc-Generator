import { TDocumentDefinitions } from 'pdfmake/interfaces';
import * as pdfMake from 'pdfmake/build/pdfmake';
import * as pdfFonts from 'pdfmake/build/vfs_fonts';
import * as fs from 'fs';
import * as path from 'path';
import axios from 'axios';
import { PluginOutput } from './pdf-plugin.interfaces';

(pdfMake as any).vfs = pdfFonts.pdfMake.vfs;

export class PdfOutputPlugin {
  public async generateDoc(outputType: string): Promise<PluginOutput> {
    if (outputType.toUpperCase() === 'PDF') {
      const pdfContent: TDocumentDefinitions = {
        content: [
          {
            text: 'Hello PDF generated successfully!',
            fontSize: 16,
            alignment: 'center',
            margin: [0, 100, 0, 0],
          },
        ],
      };

      const pdfDoc = pdfMake.createPdf(pdfContent);
      const pdfFilePath = path.join('.Plugins/generatedDocument.pdf');

      return new Promise<PluginOutput>((resolve, reject) => {
        pdfDoc.getBuffer((buffer) => {
          fs.writeFileSync(pdfFilePath, buffer);
          console.log('PDF generated successfully');
          resolve({ file: 'generatedDocument.pdf' });
        });
      });
    } else {
      throw new Error('Unsupported output type');
    }
  }

  public async createDefaultPdf(): Promise<PluginOutput> {
    const pdfContent: TDocumentDefinitions = {
      content: [
        {
          text: 'Hello, this is a default PDF document!',
          fontSize: 16,
          alignment: 'center',
          margin: [0, 100, 0, 0],
        },
      ],
    };

    const pdfDoc = pdfMake.createPdf(pdfContent);
    const pdfFilePath = './defaultDocument.pdf';

    return new Promise<PluginOutput>((resolve, reject) => {
      pdfDoc.getBuffer((buffer) => {
        fs.writeFileSync(pdfFilePath, buffer);
        console.log('Default PDF generated successfully');

        resolve({
          file: 'defaultDocument.pdf',
          url: 'http://your-domain.com/defaultDocument.pdf', // Replace with the actual PDF URL
        });
      });
    });
  }
}
