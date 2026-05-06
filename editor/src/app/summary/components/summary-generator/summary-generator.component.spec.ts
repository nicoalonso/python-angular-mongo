import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { SummaryGeneratorServiceStub } from '@tests/doubles/services/summary-generator-service.stub';
import { SummaryGeneratorService } from '@/summary/services/summary-generator.service';
import { SummaryGeneratorComponent } from '@/summary/components/summary-generator/summary-generator.component';
import { SummaryType } from '@/summary/model/summary-type';
import { findOneByContent } from '@tests/helpers/search-dom';
import { fireEvent } from '@testing-library/dom';
import { Ref } from '@tests/fixtures/ref';

describe('SummaryGeneratorComponent', () => {
  let summaryService: SummaryGeneratorServiceStub;
  let component: SummaryGeneratorComponent;
  let fixture: ComponentFixture<SummaryGeneratorComponent>;

  beforeEach(async () => {
    summaryService = new SummaryGeneratorServiceStub();

    await TestBed.configureTestingModule({
      imports: [SummaryGeneratorComponent],
      providers: [
        provideAnimationsAsync(),
        {
          provide: SummaryGeneratorService,
          useValue: summaryService,
        },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(SummaryGeneratorComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    fixture.componentRef.setInput('title', 'Generar la descripción del libro');
    fixture.componentRef.setInput('name', 'Libro');
    fixture.componentRef.setInput('type', SummaryType.Description);
    fixture.detectChanges();

    expect(component).toBeTruthy();
    expect(fixture).toMatchSnapshot();
  });

  it('should open dialog when on generate', () => {
    fixture.componentRef.setInput('title', 'Generar la descripción del libro');
    fixture.componentRef.setInput('name', 'Libro');
    fixture.componentRef.setInput('type', SummaryType.Description);
    fixture.detectChanges();

    const button = findOneByContent<HTMLButtonElement>(
      fixture,
      'button.p-button',
      'Generar',
    );
    fireEvent.click(button);

    expect(component.modalVisible()).toBeTruthy();
  });

  it('should fail when url is empty on make', () => {
    fixture.componentRef.setInput('title', 'Generar la descripción del libro');
    fixture.componentRef.setInput('name', 'Libro');
    fixture.componentRef.setInput('type', SummaryType.Description);
    fixture.detectChanges();

    component['onGenerate']();
    component['onMake']();

    expect(component.form.invalid).toBeTruthy();
    expect(component.modalVisible()).toBeTruthy();
  });

  it('should run when generate summary', (done) => {
    fixture.componentRef.setInput('title', 'Generar la descripción del libro');
    fixture.componentRef.setInput('name', 'Libro');
    fixture.componentRef.setInput('type', SummaryType.Description);
    fixture.detectChanges();

    summaryService.put(Ref.SummaryDescription);

    component.textGenerated.subscribe((value) => {
      expect(value).toBe('This is a description summary.');
      done();
    });

    component['onGenerate']();
    component.form.get('url')?.setValue('https://example.com');
    component['onMake']();

    expect(component.form.valid).toBeTruthy();
    expect(component.modalVisible()).toBeFalsy();
    expect(summaryService.createPayload).not.toBeNull();
  });
});
