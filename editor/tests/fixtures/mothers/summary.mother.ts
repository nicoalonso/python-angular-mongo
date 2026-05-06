import { BaseMother } from '@tests/fixtures/mothers/base/base-mother';
import { MotherMapping } from '@tests/fixtures/mothers/base/mother-mapping';
import { SummaryType } from '@/summary/model/summary-type';
import { SummaryState } from '@/summary/model/summary-state';
import { Summary } from '@/summary/model/summary';

const DESCRIPTION_SUMMARY = {
  id: '15fb68ed-b078-4d9a-8af3-2f2e073f320d',
  type: SummaryType.Description,
  state: SummaryState.Completed,
  content: 'This is a description summary.',
  createdBy: 'test',
  createdAt: ['2026-04-28T10:25:36', MotherMapping.DATE],
};

const BIOGRAPHY_SUMMARY = {
  id: 'cdf2266c-3a62-4bf8-95d6-730e584a19d9',
  type: SummaryType.Biography,
  state: SummaryState.Completed,
  content: 'This is a biography summary.',
  createdBy: 'test',
  createdAt: ['2026-04-28T10:25:36', MotherMapping.DATE],
};

type SummaryFixture = typeof DESCRIPTION_SUMMARY;

export class SummaryMother extends BaseMother {
  static description(this: void, overrides?: Partial<Summary>): Summary {
    return SummaryMother.create(DESCRIPTION_SUMMARY, overrides);
  }

  static biography(this: void, overrides?: Partial<Summary>): Summary {
    return SummaryMother.create(BIOGRAPHY_SUMMARY, overrides);
  }

  protected static create(
    values: SummaryFixture,
    overrides?: Partial<Summary>,
  ): Summary {
    const fields: Summary = SummaryMother.merge<SummaryFixture, Summary>(
      values,
      overrides,
    );

    return Summary.from(fields);
  }
}
