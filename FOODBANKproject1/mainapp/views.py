from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse,JsonResponse
from django.template import loader

from .models import Board, recommend

def home(request):
    context = {}
    if 'user' in request.session:
        context['user_name'] = request.session.get('user')
        return render(request, 'home.html', context)
    else:
        return render(request, 'home.html', context)

def logout(request):
    if 'user' in request.session:
        del request.session['user']

        if request.GET['next'] == "/mainapp/mypage/":
            return redirect("/mainapp/home/")
        else:
            return redirect(request.GET['next'])

def test(request) :
    template = loader.get_template('test.html')
    return HttpResponse(template.render(None, request))

def board(request):
    context={}
    if 'user' in request.session:
        context['user_name']=request.session.get('user')
    if 'error' in request.session:
        context['error']=request.session.get('error')
        del request.session['error']

    if request.method == "POST":
        title=request.POST['title']
        content=request.POST['content']
        if 'user' in request.session:
            writer=request.session['email']
            board=Board(writer_id=writer,title=title,content=content)
            board.save()
            return redirect('board')
        else:
            return redirect('/mainapp/board/?err='+"먼저 로그인을 해주세요.")
    else:
        page = int(request.GET.get('page', 1))
        board=Board.objects.all()
        board=board.order_by('-writedate')
        paginator = Paginator(board, 10)
        pagelist = paginator.get_page(page)
        position = page - 1
        # visible_page: Pagination에 보여질 개수
        visible_page = 5
        R = position // visible_page
        visible_list = []
        for i in range((R * visible_page) + 1, ((R + 1) * visible_page) + 1):
            if i > paginator.num_pages: break
            visible_list.append(i)

        context['Board']=pagelist
        context['total']=visible_list
        context['current']=page
        return render(request,'board.html',context)

def board_write(request):
    context={}
    id=request.GET.get('id',None)

    if id:
        if 'user' in request.session:
            context['user_name']=request.session.get('user')
        view=Board.objects.get(id=id)
        context["view"]=view
        return render(request,'board_write.html',context)
    else:
        if 'user' in request.session:
            context['user_name']=request.session.get('user')
            return render(request,'board_write.html',context)
        else:
            request.session['error']="먼저 로그인을 해주세요."
            return redirect("/mainapp/board/")

def view(request):
    context={}
    id = request.GET['view']

    context['update']=request.GET.get('update',None)

    if 'error' in request.session:
        context['error'] = request.session.get('error')
        del request.session['error']

    if 'user' in request.session:
        context['user_name']=request.session.get('user')
        context['user_email']=request.session.get('email')
        try:
            like=recommend.objects.filter(useremail_id=request.session.get('email'))
        except recommend.DoesNotExist:
            pass
        else:
            if int(id) in list(map(lambda x:x.post_id,like)):
                context['islike']=True
            else:
                context['islike']=False

    view=Board.objects.get(pk=id)
    context['view']=view
    return render(request,'view.html',context)

def notlike(request):
    post_id=request.GET['post_id']
    user_id=request.GET['user_id']

    if 'user' not in request.session:
        jsonContent={"error":"먼저 로그인을 해주세요."}
        return JsonResponse(jsonContent, json_dumps_params={'ensure_ascii': False})

    view = Board.objects.get(pk=post_id)
    view.up_like
    recom=recommend(post_id=post_id,useremail_id=user_id)
    recom.save()
    return JsonResponse({}, json_dumps_params={'ensure_ascii':False})

def islike(request):
    post_id = request.GET['post_id']
    user_id = request.GET['user_id']
    view=Board.objects.get(pk=post_id)
    view.down_like
    recom=recommend.objects.filter(post_id=post_id,useremail_id=user_id)
    recom.delete()
    return JsonResponse({}, json_dumps_params={'ensure_ascii':False})

def update_cnt(request):
    post_id=request.GET['id']
    loc=request.GET['loc']
    view=Board.objects.get(pk=post_id)
    view.update_counter
    return redirect(loc)

def mypage(request):
    context={}

    if 'user' in request.session:
        context['user_name']=request.session['user']
        context['user_email']=request.session['email']
        email=request.session['email']
        user_post = Board.objects.filter(writer_id=email)
        user_post=user_post.order_by('-writedate')
        context['Board']=user_post

    return render(request,'mypage.html',context)

def userpost(request):
    email=request.GET['email']
    user_post=Board.objects.filter(writer_id=email)
    jsonContent={"Board":user_post}
    return JsonResponse(jsonContent,json_dumps_params={'ensure_ascii':False})

def remove(request):
    id=request.GET['id']
    view=Board.objects.get(id=id)
    view.delete()
    return redirect("/mainapp/mypage/")

def update(request):
    id=request.GET.get('id')
    view=Board.objects.get(id=id)
    view.title=request.POST['title']
    view.content=request.POST['content']
    view.save()
    return redirect("/mainapp/mypage/")

def foodBankMap(request):
    context = {}
    if 'user' in request.session:
        context['user_name'] = request.session.get('user')
        return render(request, 'foodBankMap.html', context)
    else:
        return render(request, 'foodBankMap.html', context)

def centerItem(request):
    context = {}
    if 'user' in request.session:
        context['user_name'] = request.session.get('user')
        return render(request, 'centerItem.html', context)
    else:
        return render(request, 'centerItem.html', context)

def idx(request):
    context = {}
    if 'user' in request.session:
        context['user_name'] = request.session.get('user')
        return render(request, 'idx.html', context)
    else:
        return render(request, 'idx.html', context)

