
### blog

之前实现的 blog，已不再维护，以下是简单介绍：

- 采用前后端分离的架构模式，后端使用 Python Web 框架 Flask，前端使用 Vue
- 项目拆分为博客前台和管理后台两个独立的单页面，其中管理后台使用 OAuth2 进行身份认证
- 博客使用 MySQL 存储数据并通过 ORM 操作数据库
- 为了提高服务器响应速度，使用 Redis 实现缓存
- 最后使用 Nginx + Gunicorn + Supervisor 部署在服务器上

实现 demo 详见 [Video](https://v.qq.com/x/page/u32007i3h7h.html)



### 项目架构

```python
.
├── backend       # 后端文件的根目录
├── dist          # 前端打包的最终代码，即通过 npm run build 生成的代码
└── frontend      # 前端开发环境的代码
    ├── admin       # 管理后台
    └── blog        # 博客
```

