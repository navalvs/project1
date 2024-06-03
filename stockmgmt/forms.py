from django import forms
from .models import Stock
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category' , 'item_name' , 'quantity']

class StockSearchForm(forms.ModelForm):
    # export_to_CSV = forms.BooleanField(required=False)
    class Meta:
        model = Stock
        fields = ['category', 'item_name']

# class IssueForm (forms.ModelForm):
#     class Meta:
#         model = Stock
#         fields = ['issue.quantity', 'issue_to']

# class ReceiveForm (forms.ModelForm):
#     class Meta:
#         model = Stock
#         fields = ['receive_quantity']

# class IssueForm(forms.ModelForm):
#     class Meta:
#         model = Stock
#         fields = ['quantity', 'issue_to']
class IssueForm(forms.ModelForm):
    issue_quantity = forms.IntegerField(label='Issue Quantity')
    
    class Meta:
        model = Stock
        fields = ['quantity', 'issue_to']

    def clean(self):
        cleaned_data = super().clean()
        issue_quantity = cleaned_data.get('issue_quantity')
        current_quantity = cleaned_data.get('quantity')

        if issue_quantity is not None and current_quantity is not None:
            if issue_quantity > current_quantity:
                raise forms.ValidationError("Issue quantity cannot be greater than available quantity.")

        return cleaned_data

class ReceiveForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['receive_quantity']



class ReorderLevelForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['reorder_level'] 




class MyForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(MyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))