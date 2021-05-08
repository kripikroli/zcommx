from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.messages.views import messages
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from profiles.models import (
    CustomUser,
    MerchantUser,
)

from products.models import (
    Category, 
    SubCategory,
)


"""
User Merchant Views
cms:user_merchant_list
cms:user_merchant_create
cms:user_merchant_update
"""
class UserMerchantListView(SuccessMessageMixin, ListView):
    model = MerchantUser
    success_message = 'Merchant added successfully!'
    fields = '__all__'
    template_name = 'cms/user_merchant_list.html'

    # Number of subcategories to paginate
    paginate_by = 4

    def get_queryset(self):

        filter_val = self.request.GET.get('filter', '')
        order_by = self.request.GET.get('orderby', 'id')

        if filter_val != '':
            result = MerchantUser.objects.filter(Q(company_name__contains=filter_val) | Q(auth_user_id__first_name__icontains=filter_val) | Q(auth_user_id__last_name__icontains=filter_val) | Q(bio__contains=filter_val)).order_by(order_by)
        else:
            result = MerchantUser.objects.all().order_by(order_by)

        return result

    def get_context_data(self, **kwargs):

        context = super(UserMerchantListView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', '')
        context['orderby'] = self.request.GET.get('orderby', 'id')
        context['all_table_fields'] = MerchantUser._meta.get_fields()

        return context


class UserMerchantCreateView(SuccessMessageMixin, CreateView):
    model = CustomUser
    template_name = 'cms/user_merchant_create.html'
    success_message = 'Merchant added successfully!'
    fields = (
        'first_name',
        'last_name',
        'email',
        'username',
        'password',
    )

    def form_valid(self, form):

        # Saving CustomUser object for MerchantUser
        user = form.save(commit=False)
        user.is_active = True
        user.user_type = 3
        user.set_password(form.cleaned_data['password'])
        user.save()

        # Saving MerchantUser
        merchantuser.profile_pic = self.request.FILES['profile_pic']
        merchantuser.company_name = self.request.POST.get('company_name')
        merchantuser.gst_details = self.request.POST.get('gst_details')
        merchantuser.bio = self.request.POST.get('bio')
        merchantuser.address_line_1 = self.request.POST.get('address_line_1')
        merchantuser.address_town = self.request.POST.get('address_town')
        merchantuser.address_region = self.request.POST.get('address_region')
        merchantuser.address_country = self.request.POST.get('address_country')
        merchantuser.address_zip_code = self.request.POST.get('address_zip_code')

        is_added_by_admin = False

        if self.request.POST.get('is_added_by_admin') == 'on':
            is_added_by_admin = True

        merchantuser.is_added_by_admin = is_added_by_admin
        user.save()

        messages.success(self.request, 'Merchant user created')

        return HttpResponseRedirect(reverse('cms:user_merchant_list_view'))


class UserMerchantUpdateView(SuccessMessageMixin, UpdateView):
    model = CustomUser
    template_name = 'cms/user_merchant_update.html'
    success_message = 'Merchant updated successfully!'
    fields = (
        'first_name',
        'last_name',
        'email',
        'username',
        'password',
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['merchantuser'] = MerchantUser.objects.get(auth_user_id=self.object.pk)
        return context

    def form_valid(self, form):

        # Saving CustomUser object for MerchantUser
        user = form.save(commit=False)
        user.is_active = True
        user.user_type = 3
        user.set_password(form.cleaned_data['password'])
        user.save()

        # Saving MerchantUser
        merchantuser = MerchantUser.objects.get(auth_user_id=user.id)
        if self.request.FILES.get('profile_pic', False):
            merchantuser.profile_pic = self.request.FILES['profile_pic']
            
        merchantuser.company_name = self.request.POST.get('company_name')
        merchantuser.gst_details = self.request.POST.get('gst_details')
        merchantuser.bio = self.request.POST.get('bio')
        merchantuser.address_line_1 = self.request.POST.get('address_line_1')
        merchantuser.address_town = self.request.POST.get('address_town')
        merchantuser.address_region = self.request.POST.get('address_region')
        merchantuser.address_country = self.request.POST.get('address_country')
        merchantuser.address_zip_code = self.request.POST.get('address_zip_code')

        is_added_by_admin = False

        if self.request.POST.get('is_added_by_admin') == 'on':
            is_added_by_admin = True

        merchantuser.is_added_by_admin = is_added_by_admin
        merchantuser.save()

        messages.success(self.request, 'Merchant user updated')

        return HttpResponseRedirect(reverse('cms:user_merchant_list_view'))


"""
Category Views
cms:category_list
cms:category_create
cms:category_update
"""
class CategoryListView(ListView):
    model = Category
    template_name = 'cms/category_list.html'

    # Number of categories to paginate
    paginate_by = 8

    def get_queryset(self):

        filter_val = self.request.GET.get('filter', '')
        order_by = self.request.GET.get('orderby', 'id')

        if filter_val != '':
            result = Category.objects.filter(Q(name__contains=filter_val) | Q(description__contains=filter_val)).order_by(order_by)
        else:
            result = Category.objects.all().order_by(order_by)

        return result

    def get_context_data(self, **kwargs):

        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', '')
        context['orderby'] = self.request.GET.get('orderby', 'id')
        context['all_table_fields'] = Category._meta.get_fields()

        return context


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

    # Number of subcategories to paginate
    paginate_by = 2

    def get_queryset(self):

        filter_val = self.request.GET.get('filter', '')
        order_by = self.request.GET.get('orderby', 'id')

        if filter_val != '':
            result = SubCategory.objects.filter(Q(name__contains=filter_val) | Q(description__contains=filter_val)).order_by(order_by)
        else:
            result = SubCategory.objects.all().order_by(order_by)

        return result

    def get_context_data(self, **kwargs):

        context = super(SubCategoryListView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', '')
        context['orderby'] = self.request.GET.get('orderby', 'id')
        context['all_table_fields'] = SubCategory._meta.get_fields()

        return context


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
