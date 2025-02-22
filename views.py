from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import UserRegisterForm
from .forms import PassRegisterForm, Compartirform
from django.contrib import messages
from FEI.decoradores import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
import secrets
import requests
from FEI import models
import datetime
import  json
import requests





# Create your views here.

@esta_logueado
def index(request):
    passwords = Password.objects.all()
    context = { 'passwords': passwords}
    return render(request, 'social/feed.html', context)


def registro(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form=UserRegisterForm(request.POST)
            form.save()
            return redirect('/login')
    else:
        form = UserRegisterForm()
 
    context = { 'form' : form }
    return render(request, 'social/registro.html', context)

@login_required(login_url='/login')
def password(request):
    current_user = get_object_or_404(User, pk=request.user.pk)
    if request.method == 'POST':
        form = PassRegisterForm(request.POST)
        if form.is_valid():
            password = form.save(commit=False)
            password.user=current_user
            password.save()
            messages.success(request, f'Password creado')
    else:
        form = PassRegisterForm()
    return render(request, 'social/password.html', {'form' : form})
            
            
@login_required(login_url='/login')
def perfil(request, username=None):
    current_user = request.user
    if username and username == current_user.username:
        user = User.objects.get(username=username)
        passwords = user.passwords.all()
        compartidos = Compartir.objects.filter(user=user)
    else:
        passwords = current_user.passwords.all()
        user = current_user
        compartidos = Compartir.objects.filter(user=user)
        compartidosn = Compartir.objects.filter(user=user).count()
    return render(request, 'social/profile.html', {'user':user, 'passwords':passwords, 'compartidos':compartidos, 'compartidosn':compartidosn})

@login_required(login_url='/login')
def eliminarpassword(request, password_id):
    try:
        password = Password.objects.get(pk=password_id)
    except:
        messages.error(request, "Contraseña no encontrada")
        return redirect("perfil")
    if password.user != request.user:
        messages.error(request, "Acción invalida")
        return redirect("perfil")

    password.delete()
    messages.success(request, "El password ha sido eliminado!")
    return redirect("perfil")

def editarpassword(request, password_id):
    password = Password.objects.filter(pk=password_id).first()
    form = PassRegisterForm(instance=password)
    return render(request, 'social/passwordEdit.html', {'form':form, 'password':password})

def actualizaralumno(request, password_id):
    current_user = request.user
    password = Password.objects.get(pk=password_id)
    form=PassRegisterForm(request.POST, instance=password)
    if password.user != request.user:
        messages.error(request, "Acción invalida, no perteces a este grupo")
        return redirect("perfil")
    else:
        if form.is_valid():
            form.save()
            passwords = current_user.passwords.all()
            messages.success(request, "Contraseña actualizada exitosamente!")

        
    return render(request, 'social/feed.html', {'form':form, 'password':password})

def compartir(request, password_id):
    form = Compartirform()
    if request.method == 'POST':
        form = Compartirform(request.POST)
        if form.is_valid():
            password= Password.objects.get(id=password_id)
            compartir = form.save(commit=False)
            compartir.password=password
            compartir.save()
            messages.success(request, f'Password compartida')

            return redirect("perfil")
    else:
        context={
        "password":password_id, 'formulario':form,
        }
        return render(request, 'social/compartir.html', context)




####

def password_reset_request(request):
    if request.method == "POST":
        domain = request.headers['Host']
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            





def visitor_ip_address(request):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip






def diferencia_seg(tiempo):
    ahora = datetime.datetime.now(timezone.utc)
    diferencia = ahora - tiempo
    return diferencia.seconds
    


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


#@login_required(login_url='/login')
class  au():
    aux = secrets.token_hex(4)



#def au():
#    aux = secrets.token_hex(4)
#    return aux

#### obtener Chat_ID
@login_required(login_url='/login')
def paginafactor(request):
    template =  'social/paginafactor.html'
        
    if request.method == 'GET':
        return render (request,template)
    elif request.method == 'POST':
    
        ide = request.POST.get('cobi','').strip()
        chat_idd = request.POST.get('chat_idd','').strip()
        consultaID = models.User.objects.filter(first_name = chat_idd, username= ide)
        # try:
        idt = consultaID[0].first_name.strip()
        # except IndexError:
        #    idt = 0
        
        if chat_idd == idt:
            TOKEN = "1893181121:AAFWcrv1TDt43EKf3nOW8N4R3dpeZquvsr4"
            URL = "https://api.telegram.org/bot{}/".format(TOKEN)
            text = "Este es tu Token de seguridad, asegurate de no compartilo con nadie: {} ".format(au.aux)
            url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_idd)
            get_url(url)
        else:
            return  render(request, template, {'ERRORES': 'El chat id o el Usuario no existen o son incorrectos '} )
    return  redirect('doblefactor')
               
 #       return render(request,template) 
#class  au():
 #   aux = secrets.token_hex(4)
    #return au

#tok = au()



#def mandar(aux):
#    #aut = secrets.token_hex(4)
#    TOKEN = "1893181121:AAFWcrv1TDt43EKf3nOW8N4R3dpeZquvsr4"
#    URL = "https://api.telegram.org/bot{}/".format(TOKEN)
#    text = "Este es tu Token de seguridad, asegurate de no compartilo con nadie: {} ".format(aux)
#    chat_id  = '695659619'
#    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
 #   get_url(url)


def puedefactor(ip):
    ipnueva = models.doblea.objects.filter(pk=ip)
    if not ipnueva:
        registro_n = models.doblea(ip=ip, contain=1, ultima=datetime.datetime.now())
        registro_n.save()
        return True
    ipnueva = ipnueva[0]
    diferencia_tiempo  = diferencia_seg(ipnueva.ultima)
    if diferencia_tiempo > 60: # se resetea
        ipnueva.ultima = datetime.datetime.now()
        ipnueva.contain = 1
        ipnueva.save()
        return True
    else:
        if ipnueva.contain < 3:
            ipnueva.ultima = datetime.datetime.now()
            ipnueva.contain +=1
            ipnueva.save()
            return True
        else:
            ipnueva.ultima = datetime.datetime.now()
            return False

   

#@login_requerido
def logout(request):
    request.session.flush()
    return redirect('/inicio')

    

@login_required(login_url='/login')
def doblefactor(request):
    
    template = 'social/doblefactor.html'
    if request.method == 'GET':
        return render(request,template)
    elif request.method == 'POST':
        vacio = ''
        ip = visitor_ip_address(request)
        ac = request.POST.get('codigo','').strip()
        if puedefactor(ip):
            if ac == au.aux:
                return redirect('/perfil') 
            else:
                return render(request, template, {'ERRORES': 'El token   no es correcto.:'})
        else:
            request.session.flush()
            return redirect('/inicio')
       
        return render(request,template)    



