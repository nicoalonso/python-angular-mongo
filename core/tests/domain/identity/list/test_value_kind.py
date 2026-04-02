from datetime import datetime

from src.domain.identity.list import ValueKind

class TestValueKind:
    def test_should_run_when_check_value_kind(self):
        assert ValueKind.check(ValueKind.String)
        assert ValueKind.check(ValueKind.Boolean)
        assert ValueKind.check(ValueKind.Integer)
        assert ValueKind.check(ValueKind.Float)
        assert ValueKind.check(ValueKind.Date)
        assert ValueKind.check('wrong') == False

    def test_should_run_when_parse_string(self):
        kind = ValueKind.String

        assert kind.parse('test') == 'test'
        assert kind.parse(123) == '123'
        assert kind.parse(None) == ''

    def test_should_run_when_parse_boolean(self):
        kind = ValueKind.Boolean

        assert kind.parse('true') == True
        assert kind.parse('1') == True
        assert kind.parse('yes') == True
        assert kind.parse('y') == True
        assert kind.parse('on') == True
        assert kind.parse(True) == True
        assert kind.parse(1) == True

        assert kind.parse('false') == False
        assert kind.parse('0') == False
        assert kind.parse('no') == False
        assert kind.parse('n') == False
        assert kind.parse('off') == False
        assert kind.parse(False) == False
        assert kind.parse(0) == False

    def test_should_run_when_parse_integer(self):
        kind = ValueKind.Integer

        assert kind.parse('10') == 10
        assert kind.parse(10) == 10
        assert kind.parse('invalid') == 0
        assert kind.parse(None) == 0

    def test_should_run_when_parse_float(self):
        kind = ValueKind.Float

        assert kind.parse('10.5') == 10.5
        assert kind.parse(10.5) == 10.5
        assert kind.parse('invalid') == 0.0
        assert kind.parse(None) == 0.0

    def test_should_run_when_parse_date(self):
        kind = ValueKind.Date

        assert kind.parse('2024-01-01') == datetime(2024, 1, 1)
        assert kind.parse('invalid') is None
        assert kind.parse(None) is None

    def test_should_run_when_is_short_date(self):
        assert ValueKind.is_short_date('2024-01-01')
        assert ValueKind.is_short_date('2024-01-01T10:00:00') == False
        assert ValueKind.is_short_date('invalid') == False

    def test_should_run_when_to_list(self):
        assert ValueKind.to_list('a,b,c') == ['a', 'b', 'c']
        assert ValueKind.to_list('a, b, c') == ['a', 'b', 'c']
        assert ValueKind.to_list('a b c') == ['a', 'b', 'c']
        assert ValueKind.to_list('') == []
