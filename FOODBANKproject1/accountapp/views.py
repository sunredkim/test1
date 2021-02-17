from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect

# Create your views here.
from accountapp.models import Users


def login(request):
    context = {}
    if 'next' not in request.session:
        request.session['next'] = request.GET.get('next', None)

    if request.method == 'POST':  # POST방식으로 요청받으면, useremail에는 POST방식으로 받아온 input name이 email인 value값을 가져오고,
        # 그 값이 없으면 오류가 아니라 None으로 처리한다.(하지만 input 방식이 required이기 때문에 입력 받은 값이 없을 수는 없다.)
        useremail = request.POST.get('email', None)
        password = request.POST.get('password', None)
        try:
            user = Users.objects.get(useremail=useremail)
        # Users 클래스에 저장된 useremail 객체를 가져오는데, 그 useremail은 위에서 정의한 useremail이다.
        # Users 클래스의 모든 객체를 가져오려면 Users.objects.all()
        except Users.DoesNotExist:
            context['error'] = '아이디 또는 비밀번호가 일치하지 않습니다.'
            return render(request, 'login.html', context)
        # 예외처리문 : get한 useremail이 Users 클래스에 저장된 객체가 아니라면, error 메세지를 login.html 파일과 함께 랜더링한다.(딕셔너리형태)
        else:
            user_name = user.username
            if check_password(password, user.password):
                # 입력한 비밀번호와 db에 등록된 user.password를 비교해서 같다면,
                request.session['email'] = useremail
                request.session['user'] = user_name
                context['next'] = request.session['next']
                del request.session['next']

                if 'error' in request.session:
                    del request.session['error']

                # session에 user키의 value를 위에서 정의한 user_name으로 저장한다.
                return redirect(context['next'])
            # 로그인에 성공했으면 /mainapp/home/으로 redirect
            else:
                context['error'] = '아이디 또는 비밀번호가 일치하지 않습니다.'
                # 먄약 입력한 비밀번호와 db에 등록된 password가 다르면 error메세지와 함께 다시 login.html을 랜더링한다.
                return render(request, 'login.html', context)
    else:
        return render(request, 'login.html', context)
    # get방식일때는 login.html을 랜더링한다. 맨 처음 로그인 페이지에 접근했을 때 보여지는 화면.


def register(request):
    if request.method =='GET':
        return render(request, 'register.html')
    #get방식이면 register.html을 렌더링한다. 처음 보여지는 등록 화면.
    elif request.method == 'POST':
        useremail = request.POST.get('email', None)
        #POST방식으로 받아온 input name이 email인 value를 useremail에 저장한다.
        username = request.POST.get('name', None)
        #POST방식으로 받아온 input name이 name인 value를 username에 저장한다.
        password = request.POST.get('password', None)
        # POST방식으로 받아온 input name이 password인 value를 password에 저장한다.
        re_password = request.POST.get('re-password', None)
        res_data={}
        if password != re_password:
            res_data['error']='비밀번호가 다릅니다.'
            return render(request, 'register.html', res_data)
        #password가 re_paassword와 다르면, 비어있던 res_data 딕셔너리에 key는 error, value는 비번이 다릅니다를 저장하고,
        #그 res_data를 담아서 register.html로 전달한다.
        else:
            users = Users(
                useremail=useremail,
                username=username,
                password=make_password(password)
            )
            users.save()
            return render(request,'login.html')
        #비밀번호와 재입력한 비밀번호가 일치하면, 상단에 정의된 useremail, username, password를 각각 Users 클래스에 저장한다.
        #그리고 save를 해주고, login.html 렌더한다.

def forgot(request):
    if request.method == "POST":
        useremail=request.POST.get("email")
        try:
            user = Users.objects.get(useremail=useremail)
        except Users.DoesNotExist:
            context = {'error': '없는 이메일 주소입니다.'}
            return render(request,'forgot.html',context)
        else:
            request.session['email']=useremail
            return redirect('/accountapp/pwreset/?email='+useremail)
    else:
        return render(request, 'forgot.html')

def pwreset(request):
    if request.method == "POST":
        password=request.POST.get("password")
        re_password=request.POST.get("re-password")
        e = request.GET.get('email', "NotFound")
        if password != re_password:
            return render(request,'pwreset.html',context={"error":"비밀번호가 일치하지 않습니다.",'email':e})
        else:
            if e == "NotFound": return render(request,'/accountapp/forgot/',{'error':"변경할 이메일을 입력해 주세요."})
            user=Users.objects.get(useremail=e)
            user.password=make_password(password)
            user.save()
            return redirect("login")
    else:
        e=request.GET.get('email',"NotFound")
        if e == "NotFound": return render(request, 'forgot.html', {'error': "변경할 이메일을 입력해 주세요."})
        return render(request, 'pwreset.html',{'email':request.GET['email']})
