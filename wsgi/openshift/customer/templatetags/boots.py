'''
Template tags for Bootstrap form controls

Supported controls:
  - input with types: text, checkbox, radio, password, datetime,
                      datetime-local, date, month, time, week, number, email,
                      url, search, tel, color;
  - textarea;
  - select.
'''

from django import template

register = template.Library()

def _base_attrs(fld, *args, **kwargs):
    '''
    Base attributes of form controls
    '''
    attrs = {
        'id': ' id="{0}"'.format(fld.id_for_label),
        'class': '',
        'name': ' name="{0}"'.format(fld.html_name),
        'value': '',
        'pure_value': '',
        'maxlength': '',
        'required': (' required' if fld.field.required else ''),
        'autofocus': (' autofocus' if 'autofocus' in args else ''),
        'errors': '',
        'label': '',
        'placeholder': ''
    }
    # Changes some attributes
    # [class]
    spec_class = (' ' + kwargs.get('spec_class', '')).rstrip()
    attrs['class'] = ' class="form-control{0}"'.format(spec_class)
    # [value]
    value = fld.value()
    if value is not None:
        attrs['value'] = ' value="{0}"'.format(value)
        attrs['pure_value'] = value
    # [maxlength]
    maxlen = getattr(fld.field, 'max_length', None)
    if maxlen is not None:
        attrs['maxlength'] = ' maxlength="{0}"'.format(maxlen)
    # [errors] (rel, data-errors)
    if fld.errors:
        attrs['errors'] = ' rel="popover" data-errors="<p>{0}</p>"' \
                          .format('</p><p>'.join(fld.errors))
    # [label]
    labeled = ('labeled' in args)
    unlabeled = ('unlabeled' in args)
    attrs['label'] = '<label{cls} for="{id}">{lbl}</label>' \
                     .format(cls=('' if labeled else ' class="sr-only"'),
                             id=fld.id_for_label, lbl=fld.label)
    # [placeholder]
    if not (labeled or unlabeled):
        attrs['placeholder'] = ' placeholder="{0}"'.format(fld.label)
    #
    return attrs

@register.simple_tag
def b_input(fld, *args, **kwargs):
    '''
    Input form control

    Supported options: autofocus, labeled, unlabeled, type and spec_class.
    '''
    attrs = _base_attrs(fld, *args, **kwargs)
    attrs.update({'type': ''})
    # Changes some attributes
    # [type]
    input_type = kwargs.get('type', 'text')
    attrs['type'] = ' type="{0}"'.format(input_type)
    # [value]
    if input_type == 'password':
        attrs['value'] = ''
        attrs['pure_value'] = ''
    #
    return '{label}<input{type}{id}{class}{name}{value}{placeholder}' \
           '{maxlength}{required}{autofocus}{errors} />'.format(**attrs)

@register.simple_tag
def b_checkbox(fld, *args, **kwargs):
    '''
    Checkbox form control

    Supported options: autofocus, checked and spec_class.
    '''
    attrs = _base_attrs(fld, *args, **kwargs)
    attrs.update({'checked': (' checked' if 'checked' in args else '')})
    # Changes some attributes
    # [class]
    attrs['class'] = ' class="checkbox{0}"' \
                     .format('-inline' if 'inline' in args else '')
    # [label]
    attrs['label'] = fld.label
    #
    return '<div{id}{class}><label><input type="checkbox"{name}{value}' \
           '{checked}{required}{autofocus}{errors} />{label}</label></div>' \
           .format(**attrs)

@register.simple_tag
def b_radio(fld, *args, **kwargs):
    '''
    Radio button form control

    Supported options: autofocus, checked and spec_class.
    '''
    attrs = _base_attrs(fld, *args, **kwargs)
    attrs.update({'checked': (' checked' if 'checked' in args else '')})
    # Changes some attributes
    # [class]
    attrs['class'] = ' class="radio{0}"' \
                     .format('-inline' if 'inline' in args else '')
    # [label]
    attrs['label'] = fld.label
    #
    return '<div{id}{class}><label><input type="radio"{name}{value}' \
           '{checked}{required}{autofocus}{errors} />{label}</label></div>' \
           .format(**attrs)

@register.simple_tag
def b_textarea(fld, *args, **kwargs):
    '''
    Textarea form control

    Supported options: autofocus, labeled, unlabeled, rows and spec_class.
    '''
    attrs = _base_attrs(fld, *args, **kwargs)
    attrs.update({'rows': ''})
    # Changes some attributes
    # [rows]
    if 'rows' in kwargs:
        attrs['rows'] = ' rows="{0}"'.format(kwargs['rows'])
    #
    return '{label}<textarea{id}{class}{name}{placeholder}{rows}' \
           '{maxlength}{required}{autofocus}{errors}>{pure_value}</textarea>' \
           .format(**attrs)

@register.simple_tag
def b_select(fld, *args, **kwargs):
    '''
    Select form control

    Supported options: autofocus, labeled, size, multiple and spec_class.
    '''
    attrs = _base_attrs(fld, *args, **kwargs)
    attrs.update({'size': '',
                  'multiple': (' multiple' if 'multiple' in args else ''),
                  'options': ''})
    # Changes some attributes
    # [size]
    if 'size' in kwargs:
        attrs['size'] += ' size="{0}"'.format(kwargs['size'])
    # [options]
    value = fld.value() # value of the selected option
    for option in fld.field.queryset:
        selected = (str(option.id) == value)
        attrs['options'] += '<option value="{val}"{sel}>{txt}</option>' \
                            .format(val=option.id, txt=option.name,
                                    sel=(' selected' if selected else ''))
    #
    return '{label}<select{id}{class}{name}{size}{multiple}{required}' \
           '{autofocus}{errors}>{options}</select>'.format(**attrs)

@register.simple_tag
def b_choicebox(fld, *args, **kwargs):
    '''
    Large select form control

    Supported options: autofocus, unlabeled and spec_class.
    '''
    spec_class = kwargs.get('spec_class', '')
    kwargs.update({'spec_class': ('choicebox ' + spec_class)})
    attrs = _base_attrs(fld, *args, **kwargs)
    attrs.update({'text': '', 'options': ''})
    # Changes some attributes
    # [label]
    attrs['label'] = ('' if 'unlabeled' in args else (fld.label + ' '))
    # [options] and [value]
    value = fld.value() # value of the selected option
    for option in fld.field.queryset:
        opt_val = str(option.id)
        opt_txt = option.name
        #
        if value is None:
            # Selects the first option
            attrs['value'] = ' value="{0}"'.format(opt_val)
            value = opt_val
        #
        if opt_val == value:
            attrs['text'] = '<span class="txt">{0}</span>'.format(opt_txt)
        else:
            attrs['options'] += '<li data-val="{val}">{txt}</li>' \
                                .format(val=opt_val, txt=opt_txt)
    #
    return '<div{id}{class}>' \
           '<button type="button" class="btn btn-lg btn-default btn-block"' \
           '{autofocus}{errors}><span class="caret"></span>{label}{text}' \
           '</button><ul class="list-unstyled" style="display: none;">' \
           '{options}</ul><input type="hidden"{name}{value} /></div>' \
           .format(**attrs)
