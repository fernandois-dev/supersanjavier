from .views import ProductoListView

routes = {
    '/api/productos/': ProductoListView.as_view()
}