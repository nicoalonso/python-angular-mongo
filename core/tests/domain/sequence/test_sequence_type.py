from src.domain.sequence import SequenceType


class TestSequenceType:
    def test_run_when_try_from(self):
        assert SequenceType.try_from("membership") == SequenceType.Membership
        assert SequenceType.try_from("sale") == SequenceType.Sale
        assert SequenceType.try_from("borrow") == SequenceType.Borrow
        assert SequenceType.try_from("invalid") is None

    def test_run_when_get_prefix(self):
        assert SequenceType.Membership.get_prefix() == "SN"
        assert SequenceType.Sale.get_prefix() == "F-"
        assert SequenceType.Borrow.get_prefix() == "P-"
