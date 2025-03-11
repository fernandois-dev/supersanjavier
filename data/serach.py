# -*- coding: utf-8 -*-
from django.db.models import Q


def buscar_modelo(queryset, texto_busqueda):
    """
    Busca registros en el modelo dado que coincidan con el texto de búsqueda.

    Args:
        queryset: El queryset en el que buscar.
        texto_busqueda (str): El texto a buscar en los campos.

    Returns:
        QuerySet: Un queryset filtrado.
    """
    if not texto_busqueda:
        return queryset

    q_objects = Q()
    for field in queryset.model._meta.fields:
        if field.get_internal_type() in ('CharField', 'TextField', 'EmailField', "IntegerField"):
            q_objects |= Q(**{f'{field.name}__icontains': texto_busqueda})

    return queryset.filter(q_objects).distinct()
