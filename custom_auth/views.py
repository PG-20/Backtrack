from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, ProductForm
from django.contrib.auth import login, authenticate
from django.views.generic.detail import DetailView
from .models import Product, CustomUser
from django.contrib.auth.views import logout_then_login, login_required
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.http import HttpResponse


@login_required
def index(request):
    return redirect('products')


@login_required
def ProductsView(request):
    user = request.user
    if user.role == 1:
        try:
            if user.developing:
                return redirect('pb', pk=user.developing.id)
            elif user.productOwned:
                return redirect('pb', pk=user.productOwned.id)
        except Product.DoesNotExist:
            return render(request, 'products.html', {'title': "Products"})

    else:
        products = Product.objects.all()
        context = {'products': products, 'title': "Products"}
        return render(request, 'products.html', context)


def SignUpView(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form, 'title': "Signup"})


@login_required
def AddProductView(request, *args, **kwargs):
    form = ProductForm(request.user, request.POST or None,
                       instance=Product.objects.get(pk=kwargs['pk']) if kwargs['pk'] else None)
    if request.method == 'POST':
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = product.owner or request.user
            product.save()
            if 'developers' in form.changed_data:
                for dev in form.cleaned_data['developers']:
                    if dev not in product.developers.all():
                        current_site = get_current_site(request)
                        mail_subject = 'You have been added to a team.'
                        print(urlsafe_base64_encode(force_bytes(dev.pk)))
                        message = render_to_string('invite_email.html', {
                            'user': dev,
                            'by': request.user,
                            'name': product.name,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(dev.pk)),
                            'token': account_activation_token.make_token(dev),
                            'pk': product.pk,
                        })
                        to_email = dev.email
                        email = EmailMessage(
                            mail_subject, message, from_email="BackTrack <admin@backtrack.com>", to=[to_email]
                        )
                        email.content_subtype = "html"
                        email.send()

            return render(request, 'updateSuccess.html',
                          {'message': 'Product successfully created. All Developers have been sent invitation emails.'})
    else:
        context = {
            'form': form,
            'label': 'Create Product' if request.path == '/products/add/' else 'Edit Product #' + request.path[-2],
            'url': request.get_full_path(),
        }
        return render(request, 'create_product.html', context)


@login_required
def AcceptInvationView(request, uidb64, token, pk):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    product = Product.objects.get(pk=pk)
    if request.user != user:
        logout(request)
        return redirect('/login/?next=' + request.path)
    if user is not None and account_activation_token.check_token(user, token):
        user.developing = product
        user.save()

        return render(request, 'products.html', {'title': "Welcome", 'welcome': True, 'product': product})
    else:
        return HttpResponse('Link seems to be invalid!')


# TODO: Add HTML to email
# TODO: Check if dev already had a product or is developing
# TODO: 404 and 500 handlers
# TODO: Add help text and error text for login/signup



class ProductDetailsView(LoginRequiredMixin, DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'product_details.html'


@login_required
def LogoutView(request):
    return logout_then_login(request)
