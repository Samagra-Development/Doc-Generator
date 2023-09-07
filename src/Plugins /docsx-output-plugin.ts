import * as path from 'path';
import * as fs from 'fs';
import officegen from 'officegen';
import { PluginOutput } from './pdf-plugin.interfaces';

export class DocxOutputPlugin {
  public async generateDoc(outputType: string): Promise<PluginOutput> {
    // Add the outputType parameters
    const docxFilePath = path.join(__dirname, 'generatedDocxDocument.docx');

    return new Promise<PluginOutput>((resolve, reject) => {
      const docx = new officegen('docx');

      // Add content and formatting to the document
      const title = docx.createP();
      title.addText('<b><u>Sample DOCX Document</u></b>', { bold: true });

      const paragraph1 = docx.createP();
      paragraph1.addText('This is a sample paragraph with regular formatting.');

      const paragraph2 = docx.createP();
      paragraph2.addText(
        '<b><i>This paragraph has bold and italic formatting.</i></b>',
        { bold: true },
      );

      // Add more content as needed

      // Generate the DOCX file
      const outputStream = fs.createWriteStream(docxFilePath);
      docx.generate(outputStream);

      outputStream.on('finish', () => {
        console.log('DOCX file generated successfully');
        resolve({ file: 'generatedDocxDocument.docx' });
      });

      outputStream.on('error', (error) => {
        console.error('Error generating DOCX:', error);
        reject(error);
      });
    });
  }

  // ...rest of the code...
}
