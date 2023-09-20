import * as fs from 'fs';
import PDFDocument from 'pdfkit';

export class ImageInputPlugin {
  async convertImageToPdf(
    imageFilePath: string,
    pdfFilePath: string,
  ): Promise<void> {
    const doc = new PDFDocument();
    const output = fs.createWriteStream(pdfFilePath);

    return new Promise<void>((resolve, reject) => {
      try {
        doc.image(imageFilePath, { fit: [600, 800] }); // Adjust dimensions as needed//
        doc.pipe(output);
        doc.end();

        output.on('finish', () => {
          console.log('Image converted to PDF successfully');
          resolve();
        });

        output.on('error', (error) => {
          console.error('Error converting image to PDF:', error);
          reject(new Error('Image to PDF conversion failed'));
        });
      } catch (error) {
        console.error('Error converting image to PDF:', error);
        reject(new Error('Image to PDF conversion failed'));
      }
    });
  }
}
