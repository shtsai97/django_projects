from cats.models import Cat, Comment

from django.views import View
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin


from cats.util import CatsListView, CatsDetailView, CatsCreateView, CatsUpdateView, CatsDeleteView

from cats.forms import CommentForm
from cats.forms import CreateForm

class CatListView(CatsListView):
    model = Cat
    template_name = "cats/cat_list.html"

class CatDetailView(CatsDetailView):
    model = Cat
    template_name = "cats/cat_detail.html"

    def get(self, request, pk) :
        cat = Cat.objects.get(id=pk)
        comments = Comment.objects.filter(cat=cat).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'cat' : cat, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)


class CatCreateView(CatsCreateView):
    model = Cat
    fields = ['name', 'foods', 'weight']
    template = 'cats/cat_form.html'

class CatUpadteView(CatsUpdateView):
    model = Cat
    fields = ['name', 'foods', 'weight']
    template = 'cats/cat_form.html'


class CatDeleteView(CatsDeleteView):
    model = Cat
    template_name = "cats/cat_delete.html"

class CatFormView(LoginRequiredMixin, View):
    template = 'cats/cat_form.html'
    success_url = reverse_lazy('cats')
    def get(self, request, pk=None) :
        if not pk :
            form = CreateForm()
        else:
            cat = get_object_or_404(Cat, id=pk, owner=self.request.user)
            form = CreateForm(instance=cat)
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        if not pk:
            form = CreateForm(request.POST, request.FILES or None)
        else:
            cat = get_object_or_404(Cat, id=pk, owner=self.request.user)
            form = CreateForm(request.POST, request.FILES or None, instance=cat)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        # Adjust the model owner before saving
        cat = form.save(commit=False)
        cat.owner = self.request.user
        cat.save()
        return redirect(self.success_url)

def stream_file(request, pk) :
    cat = get_object_or_404(Cat, id=pk)
    response = HttpResponse()
    response['Content-Type'] = cat.content_type
    response['Content-Length'] = len(cat.picture)
    response.write(cat.picture)
    return response

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        f = get_object_or_404(Cat, id=pk)
        comment_form = CommentForm(request.POST)

        comment = Comment(text=request.POST['comment'], owner=request.user, cat=f)
        comment.save()
        return redirect(reverse_lazy('cat_detail', args=[pk]))

class CommentDeleteView(CatsDeleteView):
    model = Comment
    template_name = "cats/comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        cat = self.object.cat
        return reverse_lazy('cat_detail', args=[cat.id])




