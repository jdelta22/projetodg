from django.core.exceptions import ValidationError
import re

def add_attr(field, attr_name, attr_new_value):
    existing = field.widget.attrs.get(attr_name, '')
    if existing:
        attr_new_value = f'{existing} {attr_new_value}'
    field.widget.attrs[attr_name] = attr_new_value

def add_placeholder(field, placeholder):
    add_attr(field, 'placeholder', placeholder)

def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
            code='invalid'
        )
