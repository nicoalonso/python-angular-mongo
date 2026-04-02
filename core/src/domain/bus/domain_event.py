from src.domain.bus.domain_route import DomainRoute


class DomainEvent:
    """
    Domain event

    :ivar action: The action that triggered the event (e.g., "created", "updated", "deleted").
    :ivar type: The type of the event (e.g., "Sale", "Borrow", "Customer").
    :ivar route: (DomainRoute) The route or endpoint associated with the event
    """
    def __init__(self, action: str, type_: str, route: DomainRoute = DomainRoute.NONE):
        self.action = action
        self.type = type_
        self.route = route

    def change_route(self, route: DomainRoute) -> None:
        """
        Change the route associated with the event.

        :param route: The new route to associate with the event.
        """
        self.route = route
