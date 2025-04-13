from .views import server_config, server_home_page

routes = {
    "/config": server_config,
    "/": server_home_page,
}
