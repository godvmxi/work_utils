# coding: UTF-8
import os

import sae
import web
app_root = os.path.dirname(__file__)

from weixinInterface import WeixinInterface,IndexClass

urls = (
'/weixin','WeixinInterface',
'/','IndexClass'

)


templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)

app = web.application(urls, globals()).wsgifunc()
application = sae.create_wsgi_app(app)