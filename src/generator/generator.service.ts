import { Injectable } from '@nestjs/common';
import { RenderService } from 'templater';
import { GenRequest } from './types';

@Injectable()
export class GeneratorService {
  constructor(private readonly renderService: RenderService) {}

  async generate(data: GenRequest) {
    const { processed } = await this.renderService.renderTemplate(data);
    return processed;
  }
}
