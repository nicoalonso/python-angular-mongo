from src.domain.user import User


class TestUser:
    def test_create_as_admin(self):
        user = User('admin', 'Admin User', ['admin'])

        assert user.name == 'admin'
        assert user.display_name == 'Admin User'
        assert user.groups == ['admin']
        assert user.is_admin() is True

    def test_create_as_regular_user(self):
        user = User('john_doe', 'John Doe', ['user'])

        assert user.name == 'john_doe'
        assert user.display_name == 'John Doe'
        assert user.groups == ['user']
        assert user.is_admin() is False
