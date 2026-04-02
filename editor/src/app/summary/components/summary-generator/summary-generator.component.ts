import {
  ChangeDetectionStrategy,
  Component,
  computed,
  DestroyRef,
  inject,
  input,
  model,
  output,
  signal,
} from '@angular/core';
// Framework
import { Button } from 'primeng/button';
import { Dialog } from 'primeng/dialog';
import {
  FormControl,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { InputText } from 'primeng/inputtext';
import { Message } from 'primeng/message';
// Models
import { Summary } from '@/summary/model/summary';
import { SummaryType } from '@/summary/model/summary-type';
import { SummaryState } from '@/summary/model/summary-state';
// Services
import { SummaryGeneratorService } from '@/summary/services/summary-generator.service';
// Validators
import { emptyValidator } from '@/shared/validators/empty-validator';
import { concatMap, filter, interval, takeWhile, tap } from 'rxjs';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

@Component({
  selector: 'app-summary-generator',
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [
    Button,
    Dialog,
    FormsModule,
    ReactiveFormsModule,
    InputText,
    Message,
  ],
  templateUrl: './summary-generator.component.html',
  styleUrl: './summary-generator.component.less',
})
export class SummaryGeneratorComponent {
  private readonly intervalMilliseconds = 1_000;

  summaryService = inject(SummaryGeneratorService);
  private destroyRef = inject(DestroyRef);

  title = input.required<string>();
  name = input.required<string>();
  type = input.required<SummaryType>();
  textGenerated = output<string>();

  label = computed(() =>
    this.type() == SummaryType.Description ? 'descripción' : 'biografía',
  );
  modalVisible = model<boolean>(false);
  summaryState = signal<SummaryState>(SummaryState.None);

  form: FormGroup;

  constructor() {
    this.form = new FormGroup({
      url: new FormControl('', [
        emptyValidator,
        Validators.pattern('https?://.+'),
      ]),
    });
  }

  protected onGenerate(): void {
    this.modalVisible.set(true);
  }

  protected onMake(): void {
    this.form.markAllAsTouched();
    this.form.get('url')?.markAsDirty();

    if (this.form.invalid) {
      return;
    }

    this.modalVisible.set(false);
    const item = {
      url: this.form.get('url')?.value,
      type: this.type(),
    };

    this.summaryService.createItem(item).subscribe({
      next: (value: Summary) => {
        const summary = Summary.from(value);
        this.summaryState.set(summary.state);
        if (summary.isFinished()) {
          if (summary.state == SummaryState.Completed) {
            this.textGenerated.emit(summary.content);
          }
          return;
        }

        this.checkSummaryGeneration(summary);
      },
      error: (err) => {
        console.error('Error generating summary', err);
        this.summaryState.set(SummaryState.Failed);
      },
    });
  }

  private checkSummaryGeneration(summary: Summary): void {
    let found = summary;
    interval(this.intervalMilliseconds)
      .pipe(
        takeWhile(() => !found.isFinished()),
        takeUntilDestroyed(this.destroyRef),
        concatMap(() => this.summaryService.getItem(found.id)),
        tap((value) => {
          found = value;
        }),
        filter((value) => value.isFinished()),
      )
      .subscribe({
        next: (summary: Summary) => {
          this.summaryState.set(summary.state);
          if (summary.state == SummaryState.Completed) {
            this.textGenerated.emit(summary.content);
          }
        },
        error: (err) => {
          console.error('Error fetching summary', err);
          this.summaryState.set(SummaryState.Failed);
        },
      });
  }

  hasError(field: string, type: string): boolean {
    const control = this.form.get(field);
    if (!control || !control.errors) {
      return false;
    }

    return (
      control.touched && control.dirty && control.errors && control.errors[type]
    );
  }

  protected readonly SummaryState = SummaryState;
}
