int_filter_schema = {
    'type': 'dict',
    'required': False,
    'schema': {
        'from': {'type': 'integer', 'required': False, 'dependencies': 'to'},
        'to': {'type': 'integer', 'required': False, 'dependencies': 'from'},
        'eq': {'type': 'integer', 'required': False},
    }
}

phone_schema = {
    'type': 'string',
    'regex': r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$',
    'required': False,
    'maxlength': 15,
}

email_schema = {
    'type': 'string',
    'regex': r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+',
    'required': True,
    'maxlength': 128
}

password_schema = {
    'type': 'string',
    'required': True,
    'maxlength': 128
}
