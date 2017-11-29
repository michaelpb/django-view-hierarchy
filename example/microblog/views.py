from django_view_hierarchy.decorators import breadcrumb
from django.shortcuts import redirect, render
from microblog.forms import AuthorForm, FollowForm, MicroPostForm
from microblog.models import Author, MicroPost

@breadcrumb('Home page')
def home(request):
    return render(request, 'home.html')

@breadcrumb('About', groups=('title',))
def about(request):
    return render(request, 'home.html', {'content': 'about page: <a href="contact">contact page</a>'})

@breadcrumb('Contact', groups=('title',))
def about_contact(request):
    return render(request, 'home.html', {'content': 'about contact page'})


def creation(request):
    return render(request, 'index.html', {
        'author_form': AuthorForm(),
        'follow_form': FollowForm(),
        'micro_post_form': MicroPostForm(),
        'authors': Author.objects.all(),
    })


def new_author(request):
    AuthorForm(request.POST).save()
    return redirect('/')


def new_post(request):
    inst = MicroPostForm(request.POST).save()
    return redirect('/posts/%s/' % inst.author.name)


def new_follow(request):
    FollowForm(request.POST).save()
    return redirect('/')


@breadcrumb(
    lambda request, username: Author.objects.get(name=username).name
)
def view_posts(request, username):
    author = Author.objects.get(name=username)
    if request.method == 'POST':
        AuthorForm(request.POST, instance=author).save()
        return redirect(author.get_absolute_url())
    return render(request, 'posts.html', {
        'posts': MicroPost.objects.filter(author__name=username),
        'micro_post_form': MicroPostForm(initial={'author': author}),
        'username': username,
    })

@breadcrumb('All authors')
def all_authors(request):
    return render(request, 'all_authors.html', {
        'authors': Author.objects.all(),
    })
