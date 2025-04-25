from .views import server_config, server_home_page, server_sync_page

routes = {
    "/config": server_config,
    "/": server_home_page,
    "/sync": server_sync_page,
    
}
