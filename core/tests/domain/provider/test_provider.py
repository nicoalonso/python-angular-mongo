import pytest

from src.domain.identity.exception import NameEmptyError
from src.domain.provider import Provider
from tests.fixtures.mothers import AddressMother, EnterpriseContactMother


class TestProvider:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.contact = EnterpriseContactMother.amazon()
        self.address = AddressMother.newtown()

    def test_should_fail_when_name_is_empty(self):
        with pytest.raises(NameEmptyError):
            Provider.create(
                name='',
                comercial_name='Amazon',
                contact=self.contact,
                address=self.address,
                vat_number='123456789',
                created_by='test',
            )

    def test_should_create_provider(self):
        provider = Provider.create(
            name='Amazon',
            comercial_name='Amazon',
            contact=self.contact,
            address=self.address,
            vat_number='123456789',
            created_by='test',
        )

        assert provider.name == 'Amazon'
        assert provider.comercial_name == 'Amazon'
        assert provider.contact == self.contact
        assert provider.address == self.address
        assert provider.vat_number == '123456789'

    def test_should_modify_provider(self):
        provider = Provider.create(
            name='Amazon',
            comercial_name='Amazon',
            contact=self.contact,
            address=self.address,
            vat_number='123456789',
            created_by='test',
        )

        new_contact = EnterpriseContactMother.anaya()
        new_address = AddressMother.anytown()

        provider.modify(
            name='Anaya',
            comercial_name='Anaya',
            contact=new_contact,
            address=new_address,
            vat_number='987654321',
            updated_by='test',
        )

        assert provider.name == 'Anaya'
        assert provider.comercial_name == 'Anaya'
        assert provider.contact == new_contact
        assert provider.address == new_address
        assert provider.vat_number == '987654321'

    def test_should_run_when_get_descriptor(self):
        provider = Provider.create(
            name='Amazon',
            comercial_name='Amazon',
            contact=self.contact,
            address=self.address,
            vat_number='123456789',
            created_by='test',
        )

        descriptor = provider.get_descriptor()

        assert descriptor.id == provider.id
        assert descriptor.name == provider.name
