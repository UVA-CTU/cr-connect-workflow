"""Message API"""
from marshmallow import Schema, fields
from crc.services.data_store_service import DataStoreBase

class MessageModel:
    """Message model for status and alternate messages"""
    message_type: [str] = ['status', 'alternate']
    message_value: str

    def __init__(self, message_type, message_value):
        self.message_type = message_type
        self.message_value = message_value


class MessageModelSchema(Schema):
    """Schema for Message"""
    message_type = fields.String(required=True, allow_none=False)
    message_value = fields.String(required=False, allow_none=True)



def status_message():
    """Gets a status message"""
    result = DataStoreBase().get_data_common('user',
                                             'status_message',
                                             None,
                                             'kcm4zc', # g.user.uid
                                             None,
                                             None)
    message = MessageModel('status', result if result else None)
    return MessageModelSchema().dump(message)

def status_message_up(body):
    """Sets a status message"""
    result = DataStoreBase().set_data_common(
        'user',
        'status_message',
        body['message'],
        None,
        None,
        'kcm4zc',
        None,
        None)
    message = MessageModel('status', result if result else None)
    return MessageModelSchema().dump(message)


def status_message_down():
    """Clears a status message"""
    result = DataStoreBase().set_data_common(
        'user',
        'status_message',
        None,
        None,
        None,
        'kcm4zc',
        None,
        None)
    message = MessageModel('status', None)
    return MessageModelSchema().dump(message)

def alternate_message():
    """Gets an alternate message"""
    result = DataStoreBase().get_data_common('user',
                                             'alternate_message',
                                             None,
                                             'kcm4zc', # g.user.uid
                                             None,
                                             None)
    message = MessageModel('alternate', result if result else None)
    return MessageModelSchema().dump(message)

def alternate_message_up(body):
    """Sets an alternate message"""
    result = DataStoreBase().set_data_common(
        'user',
        'alternate_message',
        body['message'],
        None,
        None,
        'kcm4zc',
        None,
        None)
    message = MessageModel('alternate', result if result else None)
    return MessageModelSchema().dump(message)

def alternate_message_down():
    """Clears an alternate message"""
    result = DataStoreBase().set_data_common(
        'user',
        'alternate_message',
        None,
        None,
        None,
        'kcm4zc',
        None,
        None)
    message = MessageModel('alternate', None)
    return MessageModelSchema().dump(message)
