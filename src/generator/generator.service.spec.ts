import { Test, TestingModule } from '@nestjs/testing';
import { GeneratorService } from './generator.service';
import { RenderService, RenderResponse, TemplateType } from 'templater';

describe('GeneratorService', () => {
  let generatorService: GeneratorService;
  let renderService: RenderService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        GeneratorService,
        {
          provide: RenderService,
          useValue: { renderTemplate: jest.fn() },
        },
      ],
    }).compile();

    generatorService = module.get<GeneratorService>(GeneratorService);
    renderService = module.get<RenderService>(RenderService);
  });

  describe('generate', () => {
    it('should generate processed data', async () => {
      const mockRenderedData: RenderResponse = {
        processed: 'processed data',
        templateType: TemplateType.JSTL,
        data: {
          data: 'data',
        },
        templateBody: 'processed ${data}',
      };
      jest
        .spyOn(renderService, 'renderTemplate')
        .mockResolvedValue(mockRenderedData);

      const genRequest = {
        templateContent: 'processed ${data}',
        data: {
          data: 'data',
        },
        engineType: TemplateType.JSTL,
      };
      const result = await generatorService.generate(genRequest);

      expect(renderService.renderTemplate).toHaveBeenCalledWith(genRequest);
      expect(result).toBe(mockRenderedData.processed);
    });
  });
});
