from src.domain.common.address import Address


class TestAddress:
    def test_address(self):
        address = Address(
            street="123 Main St",
            postal_code="12345",
            city="Anytown",
            province="Pontevedra",
            country="Spain"
        )

        assert address.street == "123 Main St"
        assert address.postal_code == "12345"
        assert address.city == "Anytown"
        assert address.province == "Pontevedra"
        assert address.country == "Spain"
