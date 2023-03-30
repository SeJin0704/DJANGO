from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect, JsonResponse

from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core import serializers

from json import loads

from .models import Board, Reply
# Create your views here.

#게시판 목록보기
def index(request):
    print('index() 실행')
    board_list = Board.objects.all().order_by('-id')  #sql 에서는 DESC ASC 로 정렬 순서 정함
    context = {}

    if 'searchType' in request.GET and 'searchWord' in request.GET:
        search_type = request.GET['searchType']
        search_word = request.GET['searchWord']

        print("search_type: {}, search_word : {}".format(search_type, search_word))

        # match : java의 switch랑 비슷한
        match search_type:
            case 'title': #검색기준이 제목일때
                result = Board.objects.filter(title__contains = search_word)
            case 'writer': #검색기준이 글쓴이일때
                result = Board.objects.filter(writer__contains = search_word)
            case 'context' : #검색 기준이 내용일 때
                result = Board.objects.filter(context__contains = search_word)
        #검색을 했을때만 검색 기준과 키워드를 context에 넣는다

        context['searchWord'] = search_word
        context['searchType'] = search_type
    else : #QueryDict에 검색 조건과 키워드가 없을때
        result = Board.objects.all()

    result = result.order_by('-id')   

    #페이징 넣기
    #Paginator(목록,목록에 보여줄 개수)
    paginator = Paginator(result, 10)
    
    #paginator 클래스를 이용해서 자른 목록의 단위에서
    #몇번째 단위를 보여줄 것인지 정한다
    page_obj = paginator.get_page(request.GET.get('page'))
    
    
    # context['board_list'] = result
    #페이징한 일부 목록을 반환
    context['page_obj'] = page_obj

    return render(request, 'board/index.html', context)

def read(request,id):
    board = Board.objects.get(id = id)
    reply_list = Reply.objects.filter(board_obj = id).order_by('-id')
    board.view_count += 1
    board.save()
    context = {
        'board' : board,
        #'replyList' : reply_list
    }
    return render(request, 'board/read.html', context)

def home(request):
    return HttpResponseRedirect('/board/')

@login_required(login_url = 'common:login')
def write(request) :
    if request.method == 'GET':
        return render(request, 'board/board_form.html')
    else: #요청방식이 POST일때 할일
        title = request.POST['title']
       
        context = request.POST['context']
        author = request.user #요청에 들어있는 User 객체
        print(request.user)
        #현재 세션정보의 writer라는 키를 가진 데이터 취득
        # session_writer = request.session.get('writer')
        # if not session_writer: #세션의 정보가 없는 경우
        #     request.session['writer'] = request.POST['writer']
        # print(session_writer)

        # board = Board(
        #     title = title,
        #     wirter = writer,
        #     context = context
        # )
        # board.save() #db에 insert
        #객체.save
        Board.objects.create(
            title = title,
            author = author,
            context = context
        )
        return HttpResponseRedirect('/board/')
        #모델.objects.create(값)

@login_required(login_url = 'common:login')
def update(request, id):

    board = Board.objects.get(id = id)   ##데이터 출력
    if board.author.username != request.user.username:
        return HttpResponseRedirect('/board/')
    if request.method == "GET":
          #id로 찾은 친구 정보를 템플릿에 표시하기 위해서
          context = {'board': board}
          return render(request,'board/board_update.html', context)
    

    elif board.author.username == request.user.username:
          #id로 찾은 객체에 대해서 폼의 값으로 원래 객체의 값 덮어쓰기
          board.title = request.POST['title']
          
          board.context = request.POST['context']

          board.save()
    return HttpResponseRedirect('/board/')

@login_required(login_url = 'common:login')
def delete(request, id):
    print(id)
    #해당 객체를 가져와서 삭제
    board = Board.objects.get(id = id)

    #글 작성자의 id와 접속한 사람의 id가 같을때
    if board.author.username == request.user.username:
        board.delete()
    #다를 떄
    return HttpResponseRedirect('/board/')

    

def write_reply(request, id):
    print(request.POST)
    
    user = request.user
    reply_text = request.POST['replyText']

    # Reply.objects.create(
    #     user = user,
    #     reply_content = reply_text,
    #     board_obj = Board.objects.get(id = id)
    # )

    #queryset을 이용해 만들기
    board = Board.objects.get(id=id)
    board.reply_set.create(
        reply_content = reply_text,
        user = user
    )

    return HttpResponseRedirect('/board/'+str(id))

def delete_reply(request, id, rid):
    print(f'id: {id} rid: {rid}')

    Board.objects.get(id=id).reply_set.get(id=rid).delete()
    # response = (f'id: {id} rid: {rid}')
    #Reply.objects.get(id = rid).delete()
    return JsonResponse()
    

def update_reply(request,id):
    if request.method == 'GET':
        rid = request.GET['rid']
        board = Board.objects.get(id = id)
        context ={
            'update' : 'update',
            'board' : board, #id에 해당하는 Board 객체
            'reply' : board.reply_set.get(id = rid) #rid에 해당하는 Reply객체
        }
        return render(request, 'board/read.html', context)
    else:
        rid = request.POST['rid']

        reply = Board.objects.get(id=id).reply_set.get(id=rid)

        #폼에 들어있던 새로운 댓글 텍스트로 갱신
        reply.reply_content = request.POST['replyText']

        reply.save()
        
        return HttpResponseRedirect('/board/'+str(id))
        
        
def call_ajax(request):
    print("성공한것같읍니다?")
    print(request.POST)
    #JSON.stringify 하면 아래 표현은 사용 할 수 없음
    #print(request.POST['txt'])


    data = loads(request.body)
    print('템플릿에서 보낸 데이터',data)
    print(data['txt'])
    print(type(data))
    return JsonResponse({'result' : 'ㅊㅋㅊㅋ'})
    

def load_reply(request):

    id = request.POST['id']
    print(id)

    #해당하는 board id에 달려있는 모든 Reply가져오기

    #1번째 방법
    #Reply.objects.filter(board = id)

    #2번째 방법
    reply_list = Board.objects.get(id = id).reply_set.all()
    
    serialized_list = serializers.serialize("json", reply_list)

    response = {'response' : serialized_list}

    return JsonResponse(response)
