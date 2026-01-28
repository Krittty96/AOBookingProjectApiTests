BOOKING_DETAILS_SCHEMA = {
    'type': 'object',
    'properties': {
        'firstname': {
            'type': 'string'
        },
        'lastname': {
            'type': 'string'
        },
        'totalprice': {
            'type': 'number',
            'minimum': 0
        },
        'depositpaid': {
            'type': 'boolean'
        },
        'bookingdates': {
            'type': 'object',
            'properties': {
                'checkin': {
                    'type': 'string',
                    'format': 'date'
                },
                'checkout': {
                    'type': 'string',
                    'format': 'date'
                }
            },
            'required': ['checkin', 'checkout'],
            'additionalProperties': False
        },
        'additionalneeds': {
            'type': 'string'
        }
    },
    'required': ['firstname', 'lastname', 'totalprice', 'depositpaid', 'bookingdates'],
    'additionalProperties': False
}