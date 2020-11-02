# -*- coding: utf-8 -*-
'''
入口文件及自定义 Flask 命令
'''

import os
from dotenv import load_dotenv
from myapp import create_app


load_dotenv()    # 从 .env 中加载敏感配置
app = create_app(os.getenv('FLASK_CONFIG', 'development'))    # 从环境变量中读取程序环境，默认为开发环境


'''
=================================================
自定义 Flask 命令
flask initdb: 初始化数据库，清除数据及缓存
flask test: 运行测试
flask fake: 生成博客虚拟数据
flask ishell: 运行flask上下文的IPython shell
=================================================
'''

import sys

import IPython
from IPython.terminal.ipapp import load_default_config
from traitlets.config.loader import Config
from flask.cli import with_appcontext, click
from flask_migrate import Migrate

from myapp.libs.ext import db
from myapp.libs.mc import rdb
from myapp.models import Post, Tag, PostTag, AdminUser, Files


migrate = Migrate(app, db)


@app.cli.command('initdb', short_help='初始化数据库，清除数据及缓存')
def initdb():
    db.session.commit()
    db.drop_all()
    db.create_all()
    try:
        rdb.delete(*rdb.keys('*'))
    except:
        pass
    click.echo(u'初始化成功')


@app.cli.command('test', short_help='运行测试')
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.cli.command('fake', short_help='生成虚拟数据')
def fake():
    from fake import fake
    fake()
    click.echo(u'虚拟数据生成完毕')


@app.cli.command('ishell', short_help='Runs a IPython shell in the app context')
@click.argument('ipython_args', nargs=-1, type=click.UNPROCESSED)
@with_appcontext
def ishell(ipython_args):
    if 'IPYTHON_CONFIG' in app.config:
        config = Config(app.config['IPYTHON_CONFIG'])
    else:
        config = load_default_config()
    user_ns = app.make_shell_context()
    user_ns.update(dict(db=db, rdb=rdb, Post=Post, Tag=Tag, PostTag=PostTag,
                        AdminUser=AdminUser, Files=Files))
    config.TerminalInteractiveShell.banner1 = '''Python %s on %s
IPython: %s
App: %s%s
Instance: %s''' % (sys.version,
                   sys.platform,
                   IPython.__version__,
                   app.import_name,
                   app.debug and ' [debug]' or '',
                   app.instance_path)

    IPython.start_ipython(user_ns=user_ns, config=config, argv=ipython_args)
