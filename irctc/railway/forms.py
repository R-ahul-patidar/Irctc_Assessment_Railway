# forms.py
from django import forms
from .models import Booking, Seat

# class BookingForm(forms.ModelForm):
#     # seat = forms.ModelChoiceField(queryset=Seat.objects.filter(is_booked=False), 
#     #                             empty_label="Choose a seat",
#     #                             widget=forms.Select(attrs={'class': 'form-control'})
#     #                         )

#     class Meta:
#         model = Booking
#         fields = ['train', 'date']

#     def __init__(self, *args, **kwargs):
#         train_id = kwargs.pop('train_id', None)
#         super().__init__(*args, **kwargs)
#         if train_id:
#             self.fields['seat'].queryset = Seat.objects.filter(train_id=train_id, is_booked=False)

class BookingForm(forms.Form):
    # Add fields if necessary
    # Example:
    # name = forms.CharField(max_length=100)
    pass