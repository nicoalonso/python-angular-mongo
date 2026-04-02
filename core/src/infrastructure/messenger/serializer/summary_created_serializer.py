from typing import Optional

from src.application.summary.creator import SummaryCreatedEvent
from src.domain.bus import MessengerSerializer


class SummaryCreatedSerializer(MessengerSerializer):
    """
    Serializer for SummaryCreatedEvent to convert it to a message format suitable for sending through the messenger.
    """

    def encode(self, message: SummaryCreatedEvent) -> Optional[dict]:
        """
        Encodes a SummaryCreatedEvent message into a dictionary format.
        :param message: The SummaryCreatedEvent message to decode.
        :return: A dictionary representing the decoded message.
        """
        return {
            'action': message.action,
            'type': message.type,
            'summary': {
                'id': message.summary_id,
            }
        }

    def decode(self, message: dict) -> Optional[SummaryCreatedEvent]:
        """
        Decodes a dictionary message into a SummaryCreatedEvent.
        :param message: The dictionary message to decode.
        :return: A SummaryCreatedEvent object if decoding is successful, otherwise None.
        """
        try:
            summary_data = message.get('summary', {})
            summary_id = summary_data.get('id', '')
            return SummaryCreatedEvent(summary_id=summary_id)

        except Exception as e:
            # Log the error if needed
            print(f"Error encoding message: {e}")
            return None
