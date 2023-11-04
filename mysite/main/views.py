from django.shortcuts import render
from django.db.models import Q


def index(request):
  return render(request, 'main/index.html')

def search(request):
  content_list = Content.objects.all()
  search = request.GET.get('search','')
  if search:
    search_list = content_list.filter(
      Q(title__icontains = search) | #제목
      Q(body__icontains = search) | #내용
      Q(writer__username__icontains = search) #글쓴이
    )
  paginator = Paginator(search_list,5)
  page = request.GET.get('page','')
  posts = paginator.get_page(page)
  board = Board.objects.all()

  return render(request, 'search.html',{'posts':posts, 'Board':board, 'search':search})