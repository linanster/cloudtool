def init_ext(app):
    from app.ext.cache import cache
    from app.ext.cors import cors
    cache.init_app(app)
    cors.init_app(app)
    
