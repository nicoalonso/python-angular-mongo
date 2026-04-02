from typing import Optional

from src.domain.book import BookDescriptor
from src.domain.bus import MessengerSerializer
from src.application.book.inventory import BookInventoryEvent


class BookInventorySerializer(MessengerSerializer):
    """
    Serializer for BookInventoryEvent to convert it to a message format suitable for sending through the messenger.
    """

    def encode(self, message: BookInventoryEvent) -> dict:
        """
        Encodes a BookInventoryEvent message into a dictionary format.

        :param message: The BookInventoryEvent message to decode.
        :return: A dictionary representing the decoded message.
        """
        return {
            'action': message.action,
            'type': message.type,
            'book': {
                'id': message.descriptor.id,
                'title': message.descriptor.title,
                'isbn': message.descriptor.isbn,
            }
        }

    def decode(self, message: dict) -> Optional[BookInventoryEvent]:
        """
        Decodes a dictionary message into a BookInventoryEvent.
        :param message: The dictionary message to decode.
        :return:A BookInventoryEvent object if decoding is successful, otherwise None.
        """
        try:
            book_data = message.get('book', {})
            descriptor = BookDescriptor(
                id=book_data.get('id', ''),
                title=book_data.get('title', ''),
                isbn=book_data.get('isbn', '')
            )
            return BookInventoryEvent(descriptor)

        except Exception as e:
            # Log the error if needed
            print(f"Error encoding message: {e}")
            return None
