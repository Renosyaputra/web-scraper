from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'courses/index.html')

def new_search(request):
    keyword = request.POST.get('keyword')
    search_keyword = {
        'keyword' : keyword,
    }
    return render(request, 'courses/new_search.html', search_keyword)
