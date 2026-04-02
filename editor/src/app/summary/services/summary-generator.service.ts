import { Injectable } from '@angular/core';
import { MutationService } from '@/shared/interfaces/mutation-service';
import { Summary } from '@/summary/model/summary';

@Injectable({
  providedIn: 'root'
})
export class SummaryGeneratorService extends MutationService<Summary> {
  private readonly resource = 'summaries';

  protected override getResource(): string {
    return this.resource;
  }

  protected override makeItem(item: Summary): Summary {
    return Summary.from(item);
  }
}
