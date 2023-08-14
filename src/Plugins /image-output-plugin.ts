import * as fs from 'fs';
import * as path from 'path';
import { createCanvas } from 'canvas';
import { PluginOutput } from './pdf-plugin.interfaces';

export class ImageOutputPlugin {
  public async generateImage(outputType: string): Promise<PluginOutput> {
    if (outputType.toUpperCase() === 'IMG') {
      const canvas = createCanvas(400, 200);
      const context = canvas.getContext('2d');

      context.fillStyle = '#FF0000';
      context.fillRect(0, 0, 400, 200);

      // Draw text on the image
      context.fillStyle = '#FFFFFF';
      context.font = '20px Arial';
      context.fillText('Hello Image!', 50, 100);

      const imageFilePath = path.join(__dirname, 'generatedImage.png');

      return new Promise<PluginOutput>((resolve, reject) => {
        const stream = fs.createWriteStream(imageFilePath);
        const streamOutput = canvas.createPNGStream();

        streamOutput.pipe(stream);

        stream.on('finish', () => {
          console.log('Image generated successfully');
          resolve({ file: 'generatedImage.png' });
        });

        stream.on('error', (error) => {
          console.error('Error generating image:', error);
          reject(error);
        });
      });
    } else {
      throw new Error('Unsupported output type');
    }
  }
}
