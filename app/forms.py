from django import forms

from .utils import get_ip_and_agent


class RequestModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def get_ip_and_agent(self):
        ip_and_agent = get_ip_and_agent(self.request)
        return {'ip': ip_and_agent.get('ip'), 'agent': ip_and_agent.get('agent')}
