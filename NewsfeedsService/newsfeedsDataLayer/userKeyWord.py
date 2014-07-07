# -*- coding:utf-8 -*-
from django.template import Context, Template
t = Template('My name is {{ name }}.')
c = Context({'name': 'Stephane'})
t.render(c)