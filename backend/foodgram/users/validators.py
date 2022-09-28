from django import forms


def validate_username(value):
    fail_sym = r'^[\w.@+-]+\z'
    for chr in value:
        if chr in fail_sym:
            raise forms.ValidationError(
                'Недопустимые символы в имени пользователя!',
                params={'value': value},
            )
    if value.lower() == 'me':
        raise forms.ValidationError(
            'Недопустимое имя пользователя!',
            params={'value': value},
        )