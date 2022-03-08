from django.views import generic
from .forms import CommentForm
from .models import Post
from django.shortcuts import render, get_object_or_404

"""
A Django view is just a Python function that receives a web request and returns a web response. 
We’re going to use class-based views then map URLs for each view 
and create an HTML templated for the data returned from the views.
"""

"""
The built-in ListViews which is a subclass of generic class-based-views render 
a list with the objects of the specified model we just need to mention the template, 
similarly DetailView provides a detailed view 
for a given object of the model at the provided template.
"""


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'


# We will modify the post detail view for form processing using function based view.
# POST means submitting form.
def post_detail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})
