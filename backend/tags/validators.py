import re

from django.core.exceptions import ValidationError


def validate_color(value):
	"""Проверка поля color модели Tag."""
	if re.findall(r'[^A-F0-9]+', value[1:]) or value[0] != '#':
		raise ValidationError(
			'Required. 7 characters or fewer.'
			'Letters, digits only.'
		)
