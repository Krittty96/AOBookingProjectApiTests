BOOKING_DETAILS_SCHEMA = {
    'type': 'object',
    'properties': {
        'bookingid': {'type': 'integer', 'minimum': 1},
        'booking': {
            'type': 'object',
            'properties': {
                'firstname': {'type': 'string'},
                'lastname': {'type': 'string'},
                'totalprice': {'type': 'number', 'minimum': 0},
                'depositpaid': {'type': 'boolean'},
                'bookingdates': {
                    'type': 'object',
                    'properties': {
                        'checkin': {'type': 'string', 'format': 'date'},
                        'checkout': {'type': 'string', 'format': 'date'}
                    },
                    'required': ['checkin', 'checkout']
                },
                'additionalneeds': {'type': 'string'}
            },
            'required': ['firstname', 'lastname', 'totalprice', 'depositpaid', 'bookingdates']
        }
    },
    'required': ['bookingid', 'booking'],

    'additionalProperties': False
}
