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


class FilteredSelectMultiple(forms.SelectMultiple):
    """
    A SelectMultiple with a JavaScript filter interface.

    Note that the resulting JavaScript assumes that the jsi18n
    catalog has been loaded in the page
    """

    @property
    def media(self):
        js = [
            'jquery.js',
            'jquery.init.js',
            'core.js',
            'SelectBox.js',
            'SelectFilter2.js',
        ]
        return forms.Media(js=["js/%s" % path for path in js])

    def __init__(self, verbose_name, is_stacked, attrs=None, choices=()):
        self.verbose_name = verbose_name
        self.is_stacked = is_stacked
        super().__init__(attrs, choices)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs']['class'] = 'selectfilter'
        if self.is_stacked:
            context['widget']['attrs']['class'] += 'stacked'
        context['widget']['attrs']['data-field-name'] = self.verbose_name
        context['widget']['attrs']['data-is-stacked'] = int(self.is_stacked)
        return context
