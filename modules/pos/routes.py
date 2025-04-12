from .views import pos, pos_config

routes = {
    "/": pos,
    "/config": pos_config,
}
