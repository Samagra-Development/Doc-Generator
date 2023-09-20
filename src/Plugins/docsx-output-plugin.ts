import * as path from 'path';
import * as fs from 'fs';
import officegen from 'officegen';
import { PluginOutput } from './pdf-plugin.interfaces'; //

export class DocxOutputPlugin {
  public async generateDoc(
    outputType: string,
    userInput: string[],
  ): Promise<PluginOutput> {
    const docFilePath = path.join('./generatedDocxDocument.docx');

    return new Promise<PluginOutput>((resolve, reject) => {
      const docx = new officegen('docx');

      // Iterate through user input and add paragraphs to the document
      userInput.forEach((input) => {
        const paragraph = docx.createP();
        paragraph.addText(input);
      });

      // Generate the DOCX file
      const outputStream = fs.createWriteStream(docFilePath);
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
}
