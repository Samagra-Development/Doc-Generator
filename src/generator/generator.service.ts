import { Injectable } from '@nestjs/common';
import { RenderService } from 'templater';
import { GenReq } from './types';

@Injectable()
export class GeneratorService {
  constructor(private readonly renderService: RenderService) {}

  async generate(data: GenReq) {
    const { processed } = await this.renderService.renderTemplate(data);
    return processed;
  }
}
