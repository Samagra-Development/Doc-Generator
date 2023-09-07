declare module 'pdf-poppler' {
  export function info(filePath: string): Promise<any>; //
  export function convert(filePath: string, options: any): Promise<string[]>;
}
