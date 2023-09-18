export interface PluginOutput {
  file?: string;
  url?: string;
  pdfPath?: string;
  folder?: string; // Add this line to include the 'folder' properties
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
}
