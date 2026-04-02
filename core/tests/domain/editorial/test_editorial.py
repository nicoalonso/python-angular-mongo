import pytest

from src.domain.editorial import Editorial
from src.domain.identity.exception import NameEmptyError
from tests.fixtures.mothers import AddressMother, EnterpriseContactMother


class TestEditorial:
    def test_fail_when_name_is_empty(self):
        address = AddressMother.anytown()
        contact = EnterpriseContactMother.anaya()

        with pytest.raises(NameEmptyError):
            Editorial.create(
                name='',
                comercial_name='A leading publisher of science fiction and fantasy books.',
                contact=contact,
                address=address,
                created_by='test',
            )

    def test_create_editorial(self):
        address = AddressMother.anytown()
        contact = EnterpriseContactMother.anaya()

        editorial = Editorial.create(
            name='Anaya',
            comercial_name='A leading publisher of science fiction and fantasy books.',
            contact=contact,
            address=address,
            created_by='test',
        )

        assert editorial.name == 'Anaya'
        assert editorial.comercial_name == 'A leading publisher of science fiction and fantasy books.'
        assert editorial.contact == contact
        assert editorial.address == address

    def test_should_modify_editorial(self):
        address = AddressMother.anytown()
        contact = EnterpriseContactMother.anaya()

        editorial = Editorial.create(
            name='Anaya',
            comercial_name='A leading publisher of science fiction and fantasy books.',
            contact=contact,
            address=address,
            created_by='test',
        )

        new_address = AddressMother.newtown()
        new_contact = EnterpriseContactMother.amazon()

        editorial.modify(
            name='Planet',
            comercial_name='A leading publisher of science fiction and fantasy books.',
            contact=new_contact,
            address=new_address,
            updated_by='test',
        )

        assert editorial.name == 'Planet'
        assert editorial.comercial_name == 'A leading publisher of science fiction and fantasy books.'
        assert editorial.contact == new_contact
        assert editorial.address == new_address

    def test_should_run_when_get_descriptor(self):
        address = AddressMother.anytown()
        contact = EnterpriseContactMother.anaya()

        editorial = Editorial.create(
            name='Anaya',
            comercial_name='A leading publisher of science fiction and fantasy books.',
            contact=contact,
            address=address,
            created_by='test',
        )

        descriptor = editorial.get_descriptor()

        assert descriptor.id == editorial.id
        assert descriptor.name == 'Anaya'
