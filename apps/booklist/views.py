from django.shortcuts import render
from django.views.generic.base import View
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from pure_pagination import PageNotAnInteger, Paginator, EmptyPage

# Create your views here.
from .models import BookList, BookListDetail
from .forms import BookListForm
from commoditys.models import Commodity


class MyBookListView(View):
    """我的书单功能"""

    def get(self,request):
        booklists = BookList.objects.filter(user=request.user)
        booklists = booklists.order_by('-add_time')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(booklists, 12, request=request)

        booklists = p.page(page)

        return render(request,'usercenter-booklist-my.html',dict(booklists=booklists))

class DelBookListView(View):

    def get(self,request,booklist_id):
        booklist = BookList.objects.get(id=booklist_id)
        booklist.delete()
        from django.urls import reverse
        return HttpResponseRedirect(reverse('booklist:mybooklist'))



class EditBookListView(View):
    """书单添加修改操作"""

    def get(self, request, booklist_id):
        if booklist_id == 0:
            return render(request, 'usercenter-booklist-new.html', dict(booklist_id=booklist_id))
        else:
            booklist = BookList.objects.get(id=booklist_id)
            return render(request, 'usercenter-booklist-new.html', dict(booklist=booklist, booklist_id=booklist_id))

    def post(self, request, booklist_id):
        booklist_form = BookListForm(request.POST, request.FILES)
        if booklist_form.is_valid():
            if booklist_id == 0:
                booklist = BookList()
                booklist.user = request.user
                booklist.cover = request.FILES.get('cover')
                booklist.title = booklist_form.cleaned_data['title']
                booklist.tag1 = booklist_form.cleaned_data['tag1']
                booklist.tag2 = request.POST.get('tag2')
                booklist.desc = request.POST.get('desc')
                if request.POST.get('is_pub'):
                    booklist.is_pub = False
                booklist.save()
                from django.urls import reverse
                return HttpResponseRedirect(reverse('booklist:mybooklist'))
            else:
                booklist = BookList.objects.get(id=booklist_id)
                if request.FILES.get('cover'):
                    booklist.cover = request.FILES.get('cover')
                booklist.title = booklist_form.cleaned_data['title']
                booklist.tag1 = booklist_form.cleaned_data['tag1']
                booklist.tag2 = request.POST.get('tag2')
                booklist.desc = request.POST.get('desc')
                if request.POST.get('is_pub'):
                    booklist.is_pub = False
                booklist.save()
                from django.urls import reverse
                return HttpResponseRedirect(reverse('booklist:mybooklist'))
        else:
            return render(request, 'usercenter-booklist-new.html', dict(msg='缺少信息', booklist_id=booklist_id))


class AddBookView(View):
    """书单添加书籍"""

    def get(self,request):
        booklist_id = request.GET.get('booklist_id')
        commodity_id = request.GET.get('commodity_id')
        booklist = BookList.objects.get(id=booklist_id)
        commodity = Commodity.objects.get(id=commodity_id)
        if BookListDetail.objects.filter(booklist=booklist,commodity=commodity):
            return HttpResponse('{"status":"fail"}', content_type='application/json')
        else:
            item = BookListDetail()
            item.commodity = commodity
            item.booklist = booklist
            item.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')


class SearchBookListView(View):
    """搜索书单"""

    def get(self,request):
        keyword = request.GET.get('keyword','')
        if keyword:
            booklists = BookList.objects.filter(Q(title__icontains=keyword)|Q(tag1__icontains=keyword)|Q(tag2__icontains=keyword)|Q(user__nickname=keyword))
        else:
            booklists = BookList.objects.all()
        recomend = booklists.order_by('-click_nums')[:5]
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(booklists, 12, request=request)

        booklists = p.page(page)
        return render(request,'booklists.html',dict(keyword=keyword,recomend=recomend,booklists=booklists))


