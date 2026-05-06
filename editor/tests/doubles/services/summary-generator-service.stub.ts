import { EntityServiceStub } from '@tests/doubles/services/entity-service.stub';
import { Summary } from '@/summary/model/summary';
import { SummaryMother } from '@tests/fixtures/mothers/summary.mother';
import { Ref } from '@tests/fixtures/ref';

export class SummaryGeneratorServiceStub extends EntityServiceStub<Summary> {
  constructor() {
    super();
  }

  protected makeFixtures(): void {
    const description = SummaryMother.description();
    this.addFixture(Ref.SummaryDescription, description);

    const biography = SummaryMother.biography();
    this.addFixture(Ref.SummaryBiography, biography);
  }
}
