from stars.models import Star, Comment

from django.views import View
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin


from stars.util import StarsListView, StarsDetailView, StarsCreateView, StarsUpdateView, StarsDeleteView

from stars.forms import CommentForm
from stars.forms import CreateForm

class StarListView(StarsListView):
    model = Star
    template_name = "stars/star_list.html"

class StarDetailView(StarsDetailView):
    model = Star
    template_name = "stars/star_detail.html"

    def get(self, request, pk) :
        star = Star.objects.get(id=pk)
        comments = Comment.objects.filter(star=star).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'star' : star, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)


class StarCreateView(StarsCreateView):
    model = Star
    fields = ['name', 'distance', 'diameter']
    template = 'stars/star_form.html'

class StarUpadteView(StarsUpdateView):
    model = Star
    fields = ['name', 'distance', 'diameter']
    template = 'stars/star_form.html'


class StarDeleteView(StarsDeleteView):
    model = Star
    template_name = "stars/star_delete.html"

class StarFormView(LoginRequiredMixin, View):
    template = 'stars/star_form.html'
    success_url = reverse_lazy('stars')
    def get(self, request, pk=None) :
        if not pk :
            form = CreateForm()
        else:
            star = get_object_or_404(Star, id=pk, owner=self.request.user)
            form = CreateForm(instance=star)
        ctx = { 'form': form }
        return render(request, self.template, ctx)

    def post(self, request, pk=None) :
        if not pk:
            form = CreateForm(request.POST, request.FILES or None)
        else:
            star = get_object_or_404(Star, id=pk, owner=self.request.user)
            form = CreateForm(request.POST, request.FILES or None, instance=star)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template, ctx)

        # Adjust the model owner before saving
        star = form.save(commit=False)
        star.owner = self.request.user
        star.save()
        return redirect(self.success_url)

def stream_file(request, pk) :
    star = get_object_or_404(Star, id=pk)
    response = HttpResponse()
    response['Content-Type'] = star.content_type
    response['Content-Length'] = len(star.picture)
    response.write(star.picture)
    return response

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        f = get_object_or_404(Star, id=pk)
        comment_form = CommentForm(request.POST)

        comment = Comment(text=request.POST['comment'], owner=request.user, star=f)
        comment.save()
        return redirect(reverse_lazy('star_detail', args=[pk]))

class CommentDeleteView(StarsDeleteView):
    model = Comment
    template_name = "stars/comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        star = self.object.star
        return reverse_lazy('star_detail', args=[star.id])




