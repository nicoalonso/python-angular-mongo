import { provideHttpClient } from '@angular/common/http';
import {
  HttpTestingController,
  provideHttpClientTesting,
} from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { buildEndpoint } from '@tests/helpers/http-util';
import { SummaryMother } from '@tests/fixtures/mothers/summary.mother';
import { ApiResponse } from '@/shared/interfaces/api-response';
import { Summary } from '@/summary/model/summary';
import { SummaryGeneratorService } from '@/summary/services/summary-generator.service';

describe('SummaryGeneratorService', () => {
  let service: SummaryGeneratorService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    service = TestBed.inject(SummaryGeneratorService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should run when get item', (done) => {
    const summary = SummaryMother.description();
    const mockResponse = { data: summary } as ApiResponse<Summary>;

    service.getItem(summary.id).subscribe((result) => {
      expect(result.content).toEqual(summary.content);
      done();
    });

    const url = buildEndpoint('summaries', summary.id);
    const req = httpMock.expectOne(url);
    expect(req.request.method).toBe('GET');
    req.flush(mockResponse);
  });
});
