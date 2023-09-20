import { Injectable } from '@nestjs/common';
import { PluginOutput } from './pdf-plugin.interfaces';
import { promisify } from 'util';
import { exec } from 'child_process'; //

@Injectable()
export class DocxInputService {
  async convertToPdf(docxFilePath: string): Promise<PluginOutput> {
    const pdfFilePath = docxFilePath.replace('.docx', '.pdf');

    const execAsync = promisify(exec);

    try {
      const command = `pandoc ${docxFilePath} -o ${pdfFilePath}`;
      await execAsync(command);

      console.log('PDF file generated successfully');
      return { file: pdfFilePath };
    } catch (error: any) {
      // Cast error to 'any' type
      console.error('Error converting to PDF:', error.message);
      throw new Error('Failed to convert DOCX to PDF');
    }
  }
}
