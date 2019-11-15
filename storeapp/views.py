from django.views.generic import ListView, DetailView
from django.views.generic.list import MultipleObjectMixin
from .models import Post, Comment
from django.contrib.postgres.search import SearchVector
from django.core.mail import send_mail
from django.views.generic.edit import CreateView, FormView
from .forms import CommentForm, EmailPostForm, SearchForm
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy, reverse
from taggit.models import Tag 
from django.db.models import Count
from django.shortcuts import render 




def my_profile(request):
    return render(request, 'storeapp/dashboard/profile.html')
    
class PostListView(ListView):
    # queryset = Post.published.all() 
    # context_object_name = 'posts'
    paginate_by = 3
    template_name = 'storeapp/post/list.html'
    model = Post

 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['posts']  = self.get_object()
        context['posts']  = self.get_queryset()
        return context



    def get_queryset(self, tag_slug=None ):
        object_list = Post.published.all()
        tag = None 
        if 'tag_slug' in self.kwargs :
            tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
            object_list = object_list.filter(tags__name__in=[tag])
            return object_list
        else:
            return object_list

    


class PostDetailView(FormMixin, DetailView):
    form_class = CommentForm
    template_name = 'storeapp/post/detail.html'

    def get_object(self, queryset=None,):
        self.objects = get_object_or_404(
            Post,
            slug=self.kwargs["slug"],
            status="published",
            publish__year=self.kwargs["year"],
            publish__month=self.kwargs["month"],
            publish__day=self.kwargs["day"],
            
        )
        
        return self.objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(
            Post,
            slug=self.kwargs["slug"],
            status="published",
            publish__year=self.kwargs["year"],
            publish__month=self.kwargs["month"],
            publish__day=self.kwargs["day"],
            
        )
        post_tags_ids = post.tags.values_list('id', flat=True)

        similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)

        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]


        context.update( 
            {
                "post": self.object,
                "comments": self.object.comments.filter(active=True),
                "new_comment": getattr(self, 'new_comment', None),
                "comment_form": self.get_form(),
                "similar_posts":similar_posts
                
            }
        )
        return context
       

    def form_valid(self, form):
        self.new_comment = form.save(commit=False)
        self.new_comment.post = self.object
        self.new_comment.save()
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
    
        form = self.get_form()
        if form.is_valid():
            self.form_valid(form)
            
        context = self.get_context_data(object = self.object)
        return self.render_to_response(context)
    

class PostShareView(FormView):
    form_class = EmailPostForm
    template_name = 'storeapp/post/share.html'
    success_url = reverse_lazy('storeapp:post_list')
    
    def form_valid(self, form):
        # form.send_email()
        message = "{name} / {email}/ {post_url} said: ".format(
        name=form.cleaned_data.get('name'),
        email=form.cleaned_data.get('email'),
        post_url = self.request.build_absolute_uri(),
        )
        message += "\n\n{0}".format(form.cleaned_data.get('comments'))
        send_mail(subject=form.cleaned_data.get('name').strip(),message=message,
        from_email='mohamed.khaled.33388@gmail.com',
        recipient_list=['mohamed.khaled.33388@gmail.com']
        )
        return super().form_valid(form)



class PostSearch(FormView):
    form_class = SearchForm
    def get(self, request, *args, **kwargs):
        query = None 
        results = []
        form = SearchForm(request.GET)
        if form.is_valid():
            print("Thank you ")
            query =  form.cleaned_data['query']
            results = Post.objects.annotate(search=SearchVector('title', 'body'),).filter(search=query)
      
        else:
            print("hello world")
        return render(request, 'storeapp/post/search.html', {'form':form, 'results':results, 'query':query})
