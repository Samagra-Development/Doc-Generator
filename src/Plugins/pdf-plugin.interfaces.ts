import { TDocumentDefinitions } from 'pdfmake/interfaces';

export interface PluginOutput {
  file?: string;
  url?: string;
  images?: { url: string }[];
}

export interface Plugin {
  generateDoc(outputType: string): Promise<PluginOutput>;
  validateTemplate(template: string): boolean;
  getName(): string;
  getSupportedOutputs(): string[];
  getSupportedInputs(): string[];
  transformToPDFMake(
    inputType: string,
    outputType: string,
  ): Promise<PluginOutput>;
  transformPdfToDocsx(pdfFilePath: string): Promise<PluginOutput>;
  transformPdfToImage(pdfFilePath: string): Promise<PluginOutput>;
  transformPdfToExcalidraw(inputFile: string): PluginOutput;
  transformPdfToDrawio(inputFile: string): PluginOutput;
  transformPdfMakeToMermaid(pdfMakeContent: TDocumentDefinitions): string;
  isSupportedConversion(inputType: string, outputType: string): boolean;
}
