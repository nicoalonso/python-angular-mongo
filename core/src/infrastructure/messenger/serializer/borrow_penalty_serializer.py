from typing import Optional

from src.application.borrow.sanctioner import BorrowPenaltyEvent
from src.domain.bus import MessengerSerializer


class BorrowPenaltySerializer(MessengerSerializer):
    """
    Serializer for the BorrowPenaltyEvent.
    """

    def encode(self, message: BorrowPenaltyEvent) -> Optional[dict]:
        """
        Encodes a BorrowPenaltyEvent message into a dictionary format.
        :param message: The BorrowPenaltyEvent message to encode.
        :return: A dictionary representing the encoded message.
        """
        return {
            'action': message.action,
            'type': message.type,
        }

    def decode(self, message: dict) -> Optional[BorrowPenaltyEvent]:
        """
        Decodes a dictionary message into a BorrowPenaltyEvent.
        :param message: The dictionary message to decode.
        :return: A BorrowPenaltyEvent object if decoding is successful, otherwise None.
        """
        return BorrowPenaltyEvent()
