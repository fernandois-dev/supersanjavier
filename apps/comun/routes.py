from .views import usuario_form, usuario_list

routes = {
    '/usuarios': usuario_list,
    '/usuarios/form': usuario_form,
}
