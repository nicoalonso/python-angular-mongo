from src.domain.sequence import SequenceNumber, SequenceType


class TestSequenceNumber:
    def test_should_create(self):
        sequence_number = SequenceNumber.create(SequenceType.Membership)

        assert sequence_number.type == SequenceType.Membership
        assert sequence_number.prefix == 'SN'
        assert sequence_number.number == 1
        assert sequence_number.format() == 'SN00001'

    def test_should_increment(self):
        sequence_number = SequenceNumber.create(SequenceType.Membership)
        sequence_number.next()

        assert sequence_number.number == 2
        assert sequence_number.format() == 'SN00002'
