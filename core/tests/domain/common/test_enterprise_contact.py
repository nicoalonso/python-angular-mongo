from src.domain.common import EnterpriseContact

class TestEnterpriseContact:
    def test_enterprise_contact(self):
        enterprise_contact = EnterpriseContact(
            email='jdoe@gmail.com',
            website='www.jdoe.com',
            phone1='123456789',
            phone2='987654321',
        )

        assert enterprise_contact.email == 'jdoe@gmail.com'
        assert enterprise_contact.website == 'www.jdoe.com'
        assert enterprise_contact.phone1 == '123456789'
        assert enterprise_contact.phone2 == '987654321'
