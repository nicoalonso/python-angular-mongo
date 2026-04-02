import { Entity } from '@/shared/models/entity';
import { SummaryType } from '@/summary/model/summary-type';
import { SummaryState } from '@/summary/model/summary-state';

export class Summary extends Entity {
  constructor(
    id: string,
    public type: SummaryType,
    public state: SummaryState,
    public content: string,
  ) {
    super(id);
  }

  public static from(item: Summary): Summary {
    const summary = new Summary(item.id, item.type, item.state, item.content);

    summary.parse(item);
    return summary;
  }

  isFinished(): boolean {
    return (
      this.state === SummaryState.Completed ||
      this.state === SummaryState.Failed
    );
  }
}
