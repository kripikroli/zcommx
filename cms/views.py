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
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, View

from profiles.models import (
    CustomUser,
    MerchantUser,
)

from products.models import (
    Category, 
    SubCategory,
    Product,
    ProductMedia,
    ProductDetail,
    ProductAbout,
    ProductVariant,
    ProductVariantItem,
    ProductTag,
    ProductTransaction
)


class ProductListView(ListView):
    model = Product
    template_name = 'cms/product_list.html'
    paginate_by = 3

    def get_queryset(self):

        filter_val = self.request.GET.get('filter', '')
        order_by = self.request.GET.get('orderby', 'id')

        if filter_val != '':
            products = Product.objects.filter(Q(name__contains=filter_val) | Q(short_description__contains=filter_val)).order_by(order_by)
        else:
            products = Product.objects.all().order_by(order_by)
        
        product_list = []
        print(products)
        for product in products:
            product_media = ProductMedia.objects.filter(product_id=product.id, media_type=1, is_active=1).first()
            product_list.append({"product": product, "media": product_media})

        return product_list

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', '')
        context['orderby'] = self.request.GET.get('orderby', 'id')
        context['all_table_fields'] = Product._meta.get_fields()
        return context


class ProductCreateView(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.filter(is_active=1)
        category_list=[]

        for category in categories:
            sub_category = SubCategory.objects.filter(is_active=1, category_id=category.id)
            category_list.append({'category': category, 'sub_category': sub_category})

        merchant_users = MerchantUser.objects.filter(auth_user_id__is_active=True)

        context = {
            "category_list": category_list,
            "merchant_users": merchant_users
        }

        return render(request, 'cms/product_create.html', context)

    def post(self, request, *args, **kwargs):

        # Product basic details
        name = request.POST.get('product_name')
        slug = request.POST.get('product_slug')
        short_description = request.POST.get('product_short_description')
        long_description = request.POST.get('long_desc')
        brand = request.POST.get('product_brand')
        price = request.POST.get('product_price')
        subcategory_id = request.POST.get('product_sub_category')
        merchant_id = request.POST.get('product_merchant')

        # Product media
        media_types = request.POST.getlist('media_type[]')
        media_contents = request.FILES.getlist('media_content[]')

        print(media_contents)

        # Product more details
        title_title_list = request.POST.getlist('title_title[]')
        title_detail_list = request.POST.getlist('title_details[]')

        # Product abouts
        about_title_list = request.POST.getlist('about_title[]')

        # Product tags
        product_tags = request.POST.get('product_tags')

        
        # Foreignkey objects
        subcategory_obj = SubCategory.objects.get(id=subcategory_id)
        merchant_obj = MerchantUser.objects.get(id=merchant_id)

        # Saving product
        product_obj = Product(
            name=name,
            slug=slug,
            short_description=short_description,
            long_description=long_description,
            brand=brand,
            price=price,
            subcategory_id=subcategory_obj,
            merchant_id=merchant_obj
        )
        product_obj.save()

        # Saving product media
        i = 0
        for media_content in media_contents:
            # fs = FileSystemStorage()
            # fn = fs.save(media_content.name, media_content)
            # media_url = fs.url(fn)
            product_media_obj = ProductMedia(
                product_id=product_obj,
                media_type=media_types[i],
                media_content=media_content
            )
            product_media_obj.save()
            i += 1

        # Saving product more details
        j = 0
        for title_title in title_title_list:
            product_details_obj = ProductDetail(
                title=title_title,
                details=title_detail_list[j],
                product_id=product_obj
            )
            product_details_obj.save()
            j += 1

        # Saving product abouts
        for about in about_title_list:
            product_about_obj = ProductAbout(title=about, product_id=product_obj)
            product_about_obj.save()

        # Saving product tags
        product_tag_list = product_tags.split(',')
        for product_tag in product_tag_list:
            product_tag_obj = ProductTag(tag=product_tag, product_id=product_obj)
            product_tag_obj.save()

        # Saving product transaction
        product_transaction_obj = ProductTransaction(
            transaction_type=3,
            transaction_description='Added product: media-details-about-tags',
            product_id=product_obj
        )
        product_transaction_obj.save()

        # Return message
        return HttpResponse("ok")


class UserMerchantListView(SuccessMessageMixin, ListView):
    """
    UserMerchantListView
    cms:user_merchant_list_view
    """

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
    """
    UserMerchantCreateView
    cms:user_merchant_create_view
    """

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
    """
    UserMerchantUpdateView
    cms:user_merchant_update_view
    """

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


class CategoryListView(ListView):
    """
    CategoryListView
    cms:category_list_view
    """

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
    """
    CategoryCreateView
    cms:category_create_view
    """

    model = Category
    success_message = 'Category added successfully!'
    fields = '__all__'
    template_name = 'cms/category_create.html'


class CategoryUpdateView(SuccessMessageMixin, UpdateView):
    """
    CategoryUpdateView
    cms:category_update_view
    """

    model = Category
    success_message = 'Category updated successfully!'
    fields = '__all__'
    template_name = 'cms/category_update.html'


class SubCategoryListView(ListView):
    """
    SubCategoryListView
    cms:subcategory_list_view
    """

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
    """
    SubCategoryCreateView
    cms:subcategory_create_view
    """

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
    """
    SubCategoryUpdateView
    cms:subcategory_update_view
    """

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


def cms_logout_view(request):
    """
    cms_logout_view
    cms:logout_view
    """

    logout(request)
    return redirect('cms:cms_login_view')


def cms_login_view(request):
    """
    cms_login_view
    cms:login_view
    """

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


@login_required(login_url="/cms/")
def home_view(request):
    """
    home_view
    cms:home_view
    """
    return render(request, 'cms/home.html')
