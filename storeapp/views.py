from django.core.paginator import Paginator , PageNotAnInteger, EmptyPage
from django.views.generic import ListView, DetailView
from .models import Post, Comment
from django.views.generic.edit import CreateView
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from taggit.models import Tag 




class PostListView(ListView):
    # queryset = Post.published.all() 
    # context_object_name = 'posts'
    paginate_by = 3
    template_name = 'storeapp/post/list.html'
    page_kwarg ='pages'
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts']  = self.get_object()
        context['tag']  = self.get_object()
        return context
    
    def get_object(self, tag_slug=None ):
        object_list = Post.published.all()
        tag = None 
        if 'tag_slug' in self.kwargs :
            tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
            object_list = self.object_list.filter(tags__name__in=[tag])
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

        context.update(
            {
                "post": self.object,
                "comments": self.object.comments.filter(active=True),
                "new_comment": getattr(self, 'new_comment', None),
                "comment_form": self.get_form(),
                
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
    
