from .models import Category

# deve ser incluído no settings  em TEMPLATES
# cria dicionário com todas as categorias e passa para template
# retorna dicionário como contexto
def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)