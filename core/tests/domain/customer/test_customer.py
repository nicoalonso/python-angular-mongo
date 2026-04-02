from datetime import datetime

import pytest

from src.domain.customer import Customer
from src.domain.identity.exception import NameEmptyError
from tests.fixtures.mothers import MembershipMother, ContactInfoMother, AddressMother


class TestCustomer:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.membership = MembershipMother.active()
        self.contact = ContactInfoMother.doe()
        self.address = AddressMother.newtown()

    def test_should_fail_when_empty_name(self):
        with pytest.raises(NameEmptyError):
            Customer.create(
                name="",
                surname="Doe",
                membership=self.membership,
                contact=self.contact,
                address=self.address,
                vat_number="123456789"
            )

    def test_should_run_when_create(self):
        customer = Customer.create(
            name="John",
            surname="Doe",
            membership=self.membership,
            contact=self.contact,
            address=self.address,
            vat_number="123456789"
        )

        assert customer.name == "John"
        assert customer.surname == "Doe"
        assert customer.membership == self.membership
        assert customer.contact == self.contact
        assert customer.address == self.address
        assert customer.vat_number == "123456789"

    def test_should_run_when_modify(self):
        customer = Customer.create(
            name="John",
            surname="Doe",
            membership=self.membership,
            contact=self.contact,
            address=self.address,
            vat_number="123456789"
        )

        new_contact = ContactInfoMother.doe()
        new_address = AddressMother.anytown()

        customer.modify(
            name="Jane",
            surname="Smith",
            contact=new_contact,
            address=new_address,
            vat_number="987654321",
            active=True,
            updated_by="admin"
        )

        assert customer.name == "Jane"
        assert customer.surname == "Smith"
        assert customer.contact == new_contact
        assert customer.address == new_address
        assert customer.vat_number == "987654321"

    def test_should_run_when_deactivate(self):
        customer = Customer.create(
            name="John",
            surname="Doe",
            membership=self.membership,
            contact=self.contact,
            address=self.address,
            vat_number="123456789"
        )

        customer.modify(
            name="John",
            surname="Doe",
            contact=self.contact,
            address=self.address,
            vat_number="123456789",
            active=False,
            updated_by="admin"
        )

        assert not customer.membership.active
        assert isinstance(customer.membership.ended_at, datetime)

    def test_should_run_when_get_descriptor(self):
        customer = Customer.create(
            name="John",
            surname="Doe",
            membership=self.membership,
            contact=self.contact,
            address=self.address,
            vat_number="123456789"
        )

        descriptor = customer.get_descriptor()

        assert descriptor.name == "John"
        assert descriptor.surname == "Doe"
        assert descriptor.vat_number == "123456789"
        assert descriptor.number == customer.membership.number
