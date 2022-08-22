from django import forms
from django.shortcuts import render,HttpResponse,redirect
from app01 import models

# Create your views here.
from app01.models import UserInfo


def depart_list(request):

    # 要去数据库中获取所有的部门数据
    queryset = models.Department.objects.all()

    return render(request, 'departmentlist.html', {'queryset':queryset})

def depart_add(request):
    if request.method == "GET":
        return render(request, 'departmentadd.html')

    id = request.POST.get("id")
    title = request.POST.get("title")
    if models.Department.objects.filter(id=id):
        return render(request, 'departmentadd.html', {'errormsg':"id已存在"})
    if models.Department.objects.filter(title=title):
        return render(request, 'departmentadd.html', {'errormsg':"部门已存在"})

    models.Department.objects.create(id=id, title=title)
    return redirect('/department/list/')

def depart_delete(request):
    nid = request.GET.get("nid")
    models.Department.objects.filter(id=nid).delete()
    return redirect('/department/list/')

def depart_edit(request,nid):
    if request.method == "GET":
        obj = models.Department.objects.filter(id=nid).first()
        return render(request, 'departmentedit.html', {'obj':obj})

    title = request.POST.get("title")
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect('/department/list/')

def user_list(request):
    queryset = models.UserInfo.objects.all()
    return render(request,'userlist.html',{'queryset':queryset})

class MyForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = ["id","name","password","age","gender","depart","create_time"]
        # widgets = {
        #     "name": forms.TextInput(attrs={"class":"form-control"}),
        #     "password": forms.PasswordInput(attrs={"class": "form-control"}),
        #     "age": forms.TextInput(attrs={"class": "form-control"}),
        #     "gender": forms.TextInput(attrs={"class": "form-control"}),
        #     "depart": forms.TextInput(attrs={"class": "form-control"})
        # }
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs={"class": "form-control"}

def user_add(request):
    if request.method == "GET":
        form = MyForm()
        return render(request, 'useradd.html', {"form": form})

    # POST方式提交数据，需要数据校验
    form = MyForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    else:
        return render(request, 'useradd.html', {"form": form})

def user_edit(request,nid):
    if request.method == "GET":
        obj=models.UserInfo.objects.filter(id=nid).first()
        form = MyForm(instance=obj)
        return render(request,'useredit.html',{'form':form})

    obj = models.UserInfo.objects.filter(id=nid).first()
    form=MyForm(data=request.POST,instance=obj)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    else:
        return render(request, 'useredit.html', {"form": form})

def user_delete(request,nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')