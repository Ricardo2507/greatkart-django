from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# TEMOS QUE REGISTRAR NO SETTINGS, PARA INFORMAR QUE CRIAMOS NOSSO MODELO PERSONALIZADO
#E mesmo o User estando dentro do arquivo models.py, configuramos assim:
# AbstractBaseUser --> faz menos suposições e  precisamos informar qual campo representa o 
# nome de usuário, quais campos são obrigatórios e como gerenciar esses usuários.
#AUTH_USER_MODEL = 'accounts.Account'
class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None ):
        if not email:
            raise ValueError('Usuário deve ter um endereço de e-mail!')
        
        if not username:
             raise ValueError('Usuário deve ter um username')
         
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    # normalize ---> Isso converterá o e-mail em minúsculas, removerá os pontos ( .) e os sinais de adição seguidos por strings arbitrárias 
    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin =  True
        user.is_active =  True
        user.is_staff =  True
        user.is_superadmin =  True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)
    
    #required(obrigatórios quando criamos modelo personalizado)
    data_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    objects = MyAccountManager()
    
    def __str__(self):
       # print(f'{self.email} {self.username}')
        return {self.email} 
    
    # métodos obrigatórios
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True