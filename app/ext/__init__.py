def init_ext(app):
    from app.ext.cache import cache
    cache.init_app(app)
    
