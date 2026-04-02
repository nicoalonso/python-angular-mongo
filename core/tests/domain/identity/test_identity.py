from src.domain.identity import Identity

class TestIdentity:
    def test_should_create(self):
        identity = Identity("12345678")

        assert identity.id == "12345678"

    def test_should_empty(self):
        identity = Identity()

        assert identity.id is not None
        assert hash(identity) is not None

    def test_should_equal(self):
        identity1 = Identity("12345678")
        identity2 = Identity("12345678")

        assert identity1 == identity2
        assert hash(identity1) == hash(identity2)

    def test_should_not_equal(self):
        identity1 = Identity("12345678")
        identity2 = Identity("87654321")

        assert identity1 != identity2
        assert identity1 != 1235
        assert hash(identity1) != hash(identity2)
