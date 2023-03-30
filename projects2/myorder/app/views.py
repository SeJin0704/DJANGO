from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
# Create your views here.
from .models import Order

def index(request):
    print("Index 실행됨")
    
    
    return render(request, 'myorder/index.html')

def add(request):

    if request.method == 'GET':
        return render(request, 'myorder/add.html')
    else: #요청방식이 POST일때 할일
        order_text = request.POST['order_text']
        price = request.POST['price']
        address = request.POST['address']
        Order.objects.create(
            order_text = order_text,
            price = price,
            address = address
        )
        
        return HttpResponseRedirect('/index/search/')

def search(request):
    order_list = Order.objects.all().order_by('-id')  #sql 에서는 DESC ASC 로 정렬 순서 정함
    context = {
        'order_list' : order_list
    }
    return render(request, 'myorder/search.html',context)


def search_order(request):
    order = request.POST['search_order']
    print(order)
    oList = Order.objects.filter(order_text__contais = order)
    print(oList)
    context = {'order_list' : oList}
    return render(request,'myorder/search.html',context)

def read(request,id):
    order = Order.objects.get(id = id)
    
    context = {
        'order_list' : order
    }
    return render(request, 'myorder/read.html', context)

def delete(request,id):
    Order.objects.get(id = id).delete()
    
    return HttpResponseRedirect('/index/search/')

def update(request,id):
    
    order = Order.objects.get(id = id)

     #전송 방식에 따o른 화면 표시
    if request.method == "GET":
          #id로 찾은 친구 정보를 템플릿에 표시하기 위해서
        context = {'order': order}
        return render(request,'myorder/update.html', context)
    else :
        order.order_text = request.POST['order_text']
        order.price = request.POST['price']
        order.address = request.POST['address']

        order.save()

        return HttpResponseRedirect('/index/search/')

    