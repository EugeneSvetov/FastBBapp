# -*- coding: utf-8 -*-
import dataclasses

from django import forms
from django.forms import ChoiceField


class Export(forms.Form):
    def __init__(self, *args, **kwargs):
        super(Export, self).__init__(*args, **kwargs)
        self.fields['format'].widget.attrs.update({'class': 'dropdown-item', 'id':'ddlViewBy'})
        self.fields['format'].widget.get_context(format, value=1, attrs={'class': 'dropdown-item', 'id':'ddlViewBy'})

    format = ChoiceField(choices=(
    ('fpx', 'fpx'), ('pdf', 'pdf'), ('xml', 'xml'), ('html', 'html'), ('docx', 'docx'), ('pptx', 'pptx'), ('xlsx', 'xlsx'), ('rtf', 'rtf'),
    ('odt', 'odt'), ('odp', 'odp'), ('png', 'png'), ('jpg', 'jpg'), ('jpeg', 'jpeg'), ('svg', 'svg')), label="Формат")
