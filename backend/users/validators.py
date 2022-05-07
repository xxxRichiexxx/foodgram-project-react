import re

from django.core.exceptions import ValidationError


def validate_username(value):
	"""Проверка поля username модели user."""
	if re.findall(r'[^\w.@+-]+|_', value):
		raise ValidationError(
			'Required. 150 characters or fewer.'
			'Letters, digits and . @ + - only.'
		)
