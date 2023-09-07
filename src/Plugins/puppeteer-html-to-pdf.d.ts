declare module 'puppeteer-html-to-pdf' {
  interface Page {
    goto: (url: string) => Promise<void>;
    waitForSelector: (selector: string) => Promise<void>;
    evaluate: (fn: (xml: string) => void, xml: string) => Promise<void>;
  }

  interface Browser {
    newPage: () => Promise<Page>;
    close: () => Promise<void>;
  }

  function initBrowser(): Promise<Browser>;

  function generatePdfBuffer(page: Page): Promise<Buffer>;
}
