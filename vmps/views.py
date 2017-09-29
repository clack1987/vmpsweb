# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse
import re
from vmps.formadd import Addform
from vmps.formadd import Addform2
from vmps.formadd import Addform3
from vmps.formadd import Addform4

def index(request):
    return render(request,'index.html',locals())

def add(request):

    if request.method == 'POST':
        form1 = Addform(request.POST)

        if form1.is_valid():
          str_macaddress = form1.cleaned_data['macaddress']
          str_vlanname = form1.cleaned_data['vlanname']
          str_comment = form1.cleaned_data['comment']
          str_content = "address"+" "+str(str_macaddress)+" "+"vlan-name"+" "+str(str_vlanname)+" "+"!"+str(str_comment)

          vlandb = open("/usr/local/etc/vlan.db", 'a')
          vlandb.write("\n" + str_content)
          vlandb.close()

          return render(request, 'vmpsadd.html', locals())

        else:
          str_content = "Type is wrong!"
          return render(request, 'vmpsadd.html', locals())

    else:
        form1 = Addform()
        return render(request, 'vmpsadd.html', locals())


def show(request):
        vlandb = open("/usr/local/etc/vlan.db", 'r')
        vlandb_txt = vlandb.read()
        return render(request, 'vmpsshow.html', locals())


def search(request):
    if request.method == 'POST':
        form2 = Addform2(request.POST)
        if form2.is_valid():
          str_macaddress = form2.cleaned_data['macaddress']

          vlandb = open("/usr/local/etc/vlan.db", 'r')
          for mac_line in vlandb.readlines():
              if re.search(str_macaddress, mac_line) != None:
                  str_content = mac_line
              else:
                  str_content = "No this records!"


          return render(request, 'vmpssearch.html', locals())

        else:
             str_content = "Type is wrong!"
             return render(request, 'vmpssearch.html', locals())

    else:
        form2 = Addform2()
        return render(request, 'vmpssearch.html', locals())

def replace(file_path, old_str, new_str):
    try:
        f = open(file_path, 'r+')
        all_lines = f.readlines()
        f.seek(0)
        f.truncate()
        for line in all_lines:
            line = line.replace(old_str, new_str)
            f.write(line)
        f.close()
    except Exception, e:
        print e

def modify(request):
    if request.method == 'POST':
        form3 = Addform3(request.POST)

        if form3.is_valid():
            file_path = "/usr/local/etc/vlan.db"
            old_str = form3.cleaned_data['oldmacaddress']
            new_str = form3.cleaned_data['newmacaddress']

            replace(file_path, old_str, new_str)

            vlandb = open("/usr/local/etc/vlan.db", 'r')
            vlandb.seek(0)
            for mac_line in vlandb.readlines():
                if re.search(new_str, mac_line) != None:
                    str_content = "MACAddress is modified:" + "\n" + mac_line
                    break
                else:
                    str_content = "No this records!"

            return render(request, 'vmpsmodify.html', locals())
        else:
            str_content = "Type is wrong!"
            return render(request, 'vmpsmodify.html', locals())

    else:
        form3 = Addform3()
        return render(request, 'vmpsmodify.html', locals())


def comment(request):
    if request.method == 'POST':
        form4 = Addform4(request.POST)

        if form4.is_valid():
            file_path = "/usr/local/etc/vlan.db"
            old_str = "address" + " " + form4.cleaned_data['macaddress']
            new_str = "!address" + " " + form4.cleaned_data['macaddress']
            replace(file_path, old_str, new_str)

            vlandb = open("/usr/local/etc/vlan.db", 'r')
            for mac_line in vlandb.readlines():
                if re.search(new_str, mac_line) != None:
                    str_content = "MACAddress is commented:" + "\n" + mac_line
                    break
                else:
                    str_content = "No this records!"

            return render(request, 'vmpscomment.html', locals())
        else:
            str_content = "Type is wrong!"
            return render(request, 'vmpscomment.html', locals())

    else:
        form4 = Addform4()
        return render(request, 'vmpscomment.html', locals())
