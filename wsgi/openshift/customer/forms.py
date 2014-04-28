from django import forms
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
#from django.utils.translation import ugettext_lazy as _

from customer import models

class Form(forms.Form):
    def has_field_errors(self):
        has_non_field_errors = bool(self.non_field_errors())
        return (len(self.errors) > int(has_non_field_errors))

class Register(Form):
    first_name = forms.CharField(max_length=30, label='Имя')
    last_name = forms.CharField(max_length=30, label='Фамилия')
    email = forms.EmailField(label='Электронная почта')
    password = forms.CharField(widget=forms.PasswordInput,
                               label='Придумайте пароль')
    password_confirm = forms.CharField(widget=forms.PasswordInput,
                                       label='Повторите пароль')
    phone = forms.RegexField(regex=r'^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}' \
                                    '[\s.-]\d{4}$',
                             error_messages={
                                 'invalid': 'Допускаются следующие формы ' \
                                            'номера телефона: ' \
                                            '123-456-7890, ' \
                                            '(123) 456-7890, ' \
                                            '123 456 7890, ' \
                                            '123.456.7890, ' \
                                            '+91 (123) 456-7890.'},
                             required=False, max_length=30,
                             label='Номер телефона')
    """
    username = forms.RegexField(regex=r'^[\w.@+-]+$', max_length=30,
                                error_messages={
                                    'invalid': 'This value may contain ' \
                                               'only letters, numbers and ' \
                                               '@/./+/-/_ characters.'})
    human_test = forms.ChoiceField(label='Are you human?')
    """

    def clean_email(self):
        '''
        Checks that the supplied email address is unique for the site
        '''
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email):
            raise forms.ValidationError('Этот адрес электронной почты уже ' \
                                        'используется. Пожалуйста, введите ' \
                                        'другой адрес.')
        return email

    """
    def clean_username(self):
        '''
        Checks that the username is not already in use
        '''
        if User.objects.filter(username__iexact=self.cleaned_data['username']):
            raise forms.ValidationError('A user with that username already ' \
                                        'exists.')
        return self.cleaned_data['username']
    """

    """
    def clean_human_test(self):
        '''
        Checks that the user is human
        '''
        if not self.cleaned_data['human_test']:
            raise forms.ValidationError('Robot shall not pass! Try again.')
        return self.cleaned_data['human_test']
    """

    def clean(self):
        '''
        Checks that the two password entries match
        '''
        data = self.cleaned_data
        first = data['password']
        second = data['password_confirm']
        if first and second and (first != second):
            raise forms.ValidationError('Подтверждение не совпадает с ' \
                                        'паролем.')
        return data

    def create_profile(self, email_user=True):
        data = self.cleaned_data
        fields = {
            'username': data['email'],
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'],
            'password': data['password']
        }
        phone = data['phone']
        # Creates new user and profile
        user = User.objects.create_user(**fields)
        models.Profile.objects.create(user=user, phone=phone)
        # Notifies the user
        if email_user:
            subject = 'Welcome to Cargo Trek'
            message = 'Hello, {0}!\n\n' \
                      'Thank you for registering.\n\n' \
                      'Here bellow you can find your credentials.\n\n' \
                      'E-mail: {1}\n' \
                      'Password: Your Set Password\n\n' \
                      'Regards,\n\n' \
                      '-- Cargo Trek\n'.format(user.first_name, user.email)
            user.email_user(subject, message)

    def validate_auth(self):
        data = self.cleaned_data
        return authenticate(username=data['email'], password=data['password'])

class Login(Form):
    email = forms.EmailField(label='Электронная почта')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

    auth_user = None # authenticated user

    def clean_email(self):
        '''
        Checks that some user has the supplied email address
        '''
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email):
            raise forms.ValidationError('Учётной записи с таким адресом ' \
                                        'электронной почты не существует.')
        return email

    def clean_password(self):
        '''
        Authenticates the user with email address as username
        '''
        data = self.cleaned_data
        if 'email' not in data:
            return None
        #
        self.auth_user = authenticate(username=data['email'],
                                      password=data['password'])
        if not self.auth_user:
            raise forms.ValidationError('Неправильный пароль. Попробуйте ' \
                                        'ввести еще раз.')
        #
        return data['password']

    def clean(self):
        if not self.auth_user:
            return None
        # Checks other things
        if not self.auth_user.is_active:
            raise forms.ValidationError('Учетная запись заблокирована.')
        return self.cleaned_data

class Hotline(Form):
    subject = forms.CharField(required=False, max_length=100,
                              label='Тема вашего сообщения')
    email = forms.EmailField(label='Электронная почта (для ответа на ' \
                                   'сообщение)')
    text = forms.CharField(widget=forms.Textarea,
                           label='Ваш вопрос, предложения или замечания')

    """
    auth_user = None # authenticated user

    def __init__(self, *args, **kwargs):
        self.auth_user = kwargs.pop('request').user
        super().__init__(*args, **kwargs)
    """

    """
    def clean_email(self):
        '''
        Checks that the supplied email address is unique for the site
        '''
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email):
            raise forms.ValidationError('This email address is already in ' \
                                        'use. Please supply a different ' \
                                        'email address.')
        return email
    """

    def clean_text(self):
        text = self.cleaned_data['text']
        num_words = len(text.split())
        if num_words < 4:
            raise forms.ValidationError('Напишите, пожалуйста, больше слов.')
        return text

    def send(self, request, email_user=False):
        data = self.cleaned_data
        subject = data.get('subject', 'Hotline')
        text = data['text']
        email = data['email']
        # Sends the question to operator
        #send_mail(subject, message=text, from_email=email,
        #          recipient_list=['hotline@cargotrek.net'])
        # Sends copy of the question to user
        if email_user:
            subject = 'Question to Cargo Trek: {0}'.format(subject)
            user = request.user
            if user:
                message = 'Hello, {0}!\n\nYour message:\n{1}' \
                          .format(user.first_name, text)
                user.email_user(subject, message)
            else:
                message = 'Hello!\n\nYour message:\n{1}'.format(text)
                send_mail(subject, message, from_email='hotline@cargotrek.net',
                          recipient_list=[email])

class Question(Form):
    kind = forms.ModelChoiceField(queryset=models.QuestionKind.objects.all(),
                                  empty_label='(Нет данных)',
                                  label='Тип задачи&nbsp;&mdash;')
    text = forms.CharField(widget=forms.Textarea,
                           label='Ваша проблема, описание задачи, условия ' \
                                 'и сроки')

    def clean_text(self):
        text = self.cleaned_data['text']
        num_words = len(text.split())
        if num_words < 8:
            raise forms.ValidationError('Опишите вашу проблему подробнее, ' \
                                        'укажите по возможности условия и ' \
                                        'сроки выполнения задач.')
        return text

    def send(self, request, email_user=False):
        kind = self.cleaned_data['kind']
        text = self.cleaned_data['text']
        status = models.QuestionStatus.objects.get(pk=1)
        # Creates the question
        user = request.user
        profile = models.Profile.objects.get(user=user)
        models.Question.objects.create(profile=profile, number=0, kind=kind,
                                       text=text, status=status)
        # Sends the question to expert
        #send_mail(subject='Question to expert: {0}'.format(kind.name),
        #          message=text, from_email=user.email,
        #          recipient_list=['expert@cargotrek.net'])
        # Sends copy of the question to user
        if email_user:
            subject = 'Question to expert of Cargo Trek: {0}'.format(kind.name)
            message = 'Hello, {0}!\n\nYour question:\n{1}' \
                      .format(user.first_name, text)
            user.email_user(subject, message)

class CargoMixin(Form):
    number_of_units = forms.IntegerField(min_value=1, label='ед. товара')
    number_of_boxes = forms.IntegerField(min_value=1, label='коробок')
    weight_nett = forms.FloatField(min_value=0.1, label='нетто')
    weight_gross = forms.FloatField(min_value=0.1, label='брутто')
    length = forms.FloatField(min_value=0.1, label='толщина')
    width = forms.FloatField(min_value=0.1, label='ширина')
    height = forms.FloatField(min_value=0.1, label='высота')
    description = forms.CharField(widget=forms.Textarea, required=False,
                                  label='Характеристики товара, ' \
                                        'дополнительные сведения о грузе')
    danger_category = \
        forms.ModelChoiceField(queryset=models.DangerCategory.objects.all(),
                               empty_label='(Нет данных)',
                               label='Класс опасности груза&nbsp;&mdash;')

    def add_cargo(self, order):
        data = self.cleaned_data
        fields = {
            'order': order,
            'number': 1,
            'number_of_units': data['number_of_units'],
            'number_of_boxes': data['number_of_boxes'],
            'weight_nett': data['weight_nett'],
            'weight_gross': data['weight_gross'],
            'length': data['length'],
            'width': data['width'],
            'height': data['height'],
            'description': data['description'],
            'danger_category': data['danger_category']
        }
        return models.Cargo.objects.create(**fields)

class Order(CargoMixin, Form):
    kind = forms.ModelChoiceField(queryset=models.OrderKind.objects.all(),
                                  empty_label='(Нет данных)',
                                  label='Тип заказа&nbsp;&mdash;')
    dispatch_address = forms.CharField(max_length=500, label='откуда')
    delivery_address = forms.CharField(max_length=500, label='куда')
    note = forms.CharField(widget=forms.Textarea, required=False,
                           label='Уточнения к заказу, если необходимы')

    def send(self, request, email_user=False):
        data = self.cleaned_data
        user = request.user
        profile = models.Profile.objects.get(user=user)
        status = models.OrderStatus.objects.get(pk=1)
        # Creates the order
        fields = {
            'profile': profile,
            'number': 1,
            'kind': data['kind'],
            'dispatch_address': data['dispatch_address'],
            'delivery_address': data['delivery_address'],
            'note': data['note'],
            'status': status
        }
        order = models.Order.objects.create(**fields)
        # Adds the cargo for current order
        cargo = self.add_cargo(order)
        # Notifies the operator
        #send_mail(subject='Order in Cargo Trek: {0}'.format(kind.name),
        #          message=cargo.name, from_email=user.email,
        #          recipient_list=['operator@cargotrek.net'])
        # Notifies the user
        if email_user:
            subject = 'Order in Cargo Trek: {0}'.format(kind.name)
            message = 'Hello, {0}!\n\nYour order:\n{1}' \
                      .format(user.first_name, order)
            user.email_user(subject, message)
