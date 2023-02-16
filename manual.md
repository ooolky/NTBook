## 安装
使用pip安装必要第三方库：  

`Python          3.7.0`

`Django          2.0.6`

`django-appconf  1.0.2`

`django-ckeditor 5.6.1`  

`django-imagekit 4.0.2`  

`django-redis    4.10.0`

`image           1.5.24`

`oscrypto        0.19.1`

`pip             19.0.3`

`sqlparse        0.3.0`

`uWSGI           2.0.18`

`Xadmin          2.0.1`:[ZIP下载](https://github.com/sshwsfc/xadmin/tree/django2)

### 配置
配置都是在`setting.py`中.部分配置迁移到了后台配置中。

`bin`目录是在`linux`环境中使用`Nginx`+`uWSGI`+`Redis`+`Docker`来部署的脚本和`Nginx`配置文件.


## 运行
 先生成测试sqlite
 
    `python manage.py makemigrations`
    
    `python manage.py migrate`
    
 创建超级用户
 
    `python manage.py createsuperuser`
    
 收集静态文件
 
    `python manage.py collectstatic`
    
 再runserver
 
    `python manage.py runserver 0:8000`
    

 浏览器打开: http://localhost:8000/  就可以看到效果了。

