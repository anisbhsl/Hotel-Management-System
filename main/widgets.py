from django import forms
# from django.conf import settings
from django.utils.translation import gettext as _


class MyDateWidget(forms.DateInput):
    @property
    def media(self):
        # extra = '' if settings.DEBUG else '.min'
        js = [
            # 'vendor/jquery/jquery%s.js' % extra,
            'jquery.js',
            'jquery.init.js',
            'calendar.js',
            'DateTimeShortcuts.js',
        ]
        return forms.Media(js=["js/%s" % path for path in js])

    def __init__(self, attrs=None, format=None):
        final_attrs = {'class': 'vDateField', 'size': '10'}
        if attrs is not None:
            final_attrs.update(attrs)
        super().__init__(attrs=final_attrs, format=format)


class MyTimeWidget(forms.TimeInput):
    @property
    def media(self):
        # extra = '' if settings.DEBUG else '.min'
        js = [
            # 'vendor/jquery/jquery%s.js' % extra,
            'jquery.js',
            'jquery.init.js',
            'calendar.js',
            'DateTimeShortcuts.js',
        ]
        return forms.Media(js=["js/%s" % path for path in js])

    def __init__(self, attrs=None, format=None):
        final_attrs = {'class': 'vTimeField', 'size': '8'}
        if attrs is not None:
            final_attrs.update(attrs)
        super().__init__(attrs=final_attrs, format=format)


class MySplitDateTime(forms.SplitDateTimeWidget):
    """
    A SplitDateTime Widget.
    """
    template_name = 'split_datetime.html'

    def __init__(self, attrs=None):
        widgets = [MyDateWidget, MyTimeWidget]
        # Note that we're calling MultiWidget, not SplitDateTimeWidget, because
        # we want to define widgets.
        forms.MultiWidget.__init__(self, widgets, attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['date_label'] = _('Date:')
        context['time_label'] = _('Time:')
        return context
