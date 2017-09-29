from django import forms

class Addform(forms.Form):

    #attrs_dict = {'a':'a','b':'b'}

    macaddress = forms.IntegerField()
    vlanname = forms.ChoiceField(choices=[('vlan123','vlan123'),('vlan234','vlan234')])
    comment = forms.Field()



class Addform2(forms.Form):
    macaddress = forms.Field()


class Addform3(forms.Form):
    oldmacaddress = forms.Field()
    newmacaddress = forms.Field()

class Addform4(forms.Form):
    macaddress = forms.Field()

