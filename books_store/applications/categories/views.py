from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
#
from applications.books.mixins import AdminPermissionMixin
from .forms import CreateCategoryForm
from .models import Category

class AllCategories(ListView):

    template_name = 'categories/all_categories.html'
    paginate_by = 6
    context_object_name = 'categories'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kword = self.request.GET.get('kword')
        if kword is not None:
            context['kword'] = kword
        else:
            context['kword'] = ''
        return context

    def get_queryset(self):

        kword = self.request.GET.get('kword')
        if kword is not None:
            return Category.objects.get_categories_by_kword(kword)
        
        return Category.objects.all()

class AllCategoriesAdmin(View):

    template_name = 'categories/all_categories_admin.html'

    def get(self, request, *args, **kwargs):

        if(self.request.user.is_anonymous or self.request.user.ocupation != '0'):
            return redirect('home_app:home')
        
        categories = Category.objects.get_all_categories()
        paginator = Paginator(categories, 6)
        page = self.request.GET.get('page')
        obj_page = paginator.get_page(page)

        return render(request, self.template_name,{
            'page_obj':obj_page
        })
    
class DeleteCategory(View):

    def post(self, request, *args, **kwargs):
        if(self.request.user.is_anonymous or self.request.user.ocupation != '0'):
            return redirect('home_app:home')
        
        category_id = self.request.POST.get('category_id')

        Category.objects.filter(id=category_id).delete()

        return redirect('categories:all-categories-admin')

class CreateCategoryView(AdminPermissionMixin, CreateView):
    success_url = reverse_lazy('categories:all-categories-admin')
    form_class = CreateCategoryForm
    template_name = 'categories/create_category.html'

class UpdateCategoryView(AdminPermissionMixin, UpdateView):
    success_url = reverse_lazy('categories:all-categories-admin')
    form_class = CreateCategoryForm
    template_name = 'categories/update_category.html'
    model = Category





