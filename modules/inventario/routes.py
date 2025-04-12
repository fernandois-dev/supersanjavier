from .views import producto_list, producto_form, categoria_list, categoria_form

routes = {
    '/productos': producto_list,
    '/productos/form': producto_form,
    "/categorias": categoria_list,
    "/categorias/form": categoria_form
}
