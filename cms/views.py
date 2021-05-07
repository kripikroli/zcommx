from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin

from products.models import Category, SubCategory

"""
Category Views
cms:category_list
cms:category_create
cms:category_update
"""
class CategoryListView(ListView):
    model = Category
    template_name = 'cms/category_list.html'

class CategoryCreateView(SuccessMessageMixin, CreateView):
    model = Category
    success_message = 'Category added successfully!'
    fields = '__all__'
    template_name = 'cms/category_create.html'

class CategoryUpdateView(SuccessMessageMixin, UpdateView):
    model = Category
    success_message = 'Category updated successfully!'
    fields = '__all__'
    template_name = 'cms/category_update.html'


"""
SubCategory Views
cms:sub_category_list
cms:sub_category_create
cms:sub_category_update
"""
class SubCategoryListView(ListView):
    model = SubCategory
    template_name = 'cms/sub_category_list.html'

class SubCategoryCreateView(SuccessMessageMixin, CreateView):
    model = SubCategory
    success_message = 'SubCategory added successfully!'
    fields = fields = (
        'id',
        'category_id',
        'name',
        'slug',
        'thumbnail',
        'description',
        'is_active',
    )
    template_name = 'cms/sub_category_create.html'

class SubCategoryUpdateView(SuccessMessageMixin, UpdateView):
    model = SubCategory
    success_message = 'SubCategory updated successfully!'
    fields = (
        'id',
        'category_id',
        'name',
        'slug',
        'thumbnail',
        'description',
        'is_active',
    )
    template_name = 'cms/sub_category_update.html'



"""
Authentication Views
login
logout
"""
def cms_logout_view(request):
    logout(request)
    return redirect('cms:cms_login_view')

def cms_login_view(request):
    error_message = None
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('cms:cms_home')

        else:
            error_message = 'Oppsss... something went wrong'

    context = {
        'form': form,
        'error_message': error_message
    }
    return render(request, 'cms/login.html', context)



"""
Home View
home
"""
@login_required(login_url="/cms/")
def home_view(request):
    return render(request, 'cms/home.html')
