import * as path from 'path';
import { PluginOutput } from './pdf-plugin.interfaces';
import * as pdfPoppler from 'pdf-poppler';

export class PdfInputPlugin {
  public async transformPdfToImage(pdfFilePath: string): Promise<PluginOutput> {
    const outDir = path.dirname(pdfFilePath);
    const outPrefix = path.basename(pdfFilePath, path.extname(pdfFilePath));

    const pdfImageOptions = {
      format: 'jpeg',
      out_dir: outDir,
      out_prefix: outPrefix,
      page: null,
    };

    try {
      const result = await pdfPoppler.convert(pdfFilePath, pdfImageOptions);

      console.log('Successfully converted');
      console.log(result);

      const images = Array.isArray(result)
        ? result.map((imagePath: string) => ({ url: imagePath }))
        : [{ url: result }];

      return { images: images };
    } catch (error) {
      console.error('Error converting PDF to image:', error);
      throw new Error('PDF to image conversion failed');
    }
  }
  //
}
