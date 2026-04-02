from src.domain.identity import Entity


class TestEntity:
    def test_entity(self):
        entity = Entity()
        entity.updated('me')

        assert entity.id is not None
        assert entity.updated_by == 'me'
