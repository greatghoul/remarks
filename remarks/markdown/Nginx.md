title: Nginx
description: Introduce Nginx.
name: dongliang.ma
layout: true
class: center, middle, inverse

---
# Nginx基础介绍
## 马冬亮
## 2014-05-19

---

layout: false
.left-column[
### Nginx简介
]

.right-column[
### 什么是Nginx
* 一个高性能的HTTP和反向代理服务器
* 一个IMAP/POP3/SMTP代理服务器
* 由Igor Sysoev为俄罗斯访问量第二的Rambler.ru站点开发
* 源代码以类BSD许可证的形式发布
* 以稳定性、丰富的功能集、示例配置文件和低系统资源的消耗而闻名

### 为什么选择Nginx
* 在高连接并发的情况下，Nginx是Apache服务器不错的替代品
* Nginx作为负载均衡服务器
* 作为邮件代理服务器
* Nginx是一个安装非常的简单，配置文件非常简洁，Bug非常少的服务器

]

---

.left-column[
### Nginx简介
### 市场份额
]

.right-column[
### 市场份额

![市场份额](/static/wpid-graph1.png)

]

---

.left-column[
### Nginx简介
### 市场份额
]

.right-column[

![市场份额](/static/wpid-graph2.png)

![市场份额](/static/wpid-graph3.png)
]

---

.left-column[
### Nginx简介
### 市场份额
### Nginx架构
]

.right-column[
### Nginx架构

* 一个master进程和多个worker进程
* master进程用于管理worker进程
* worker进程处理基本网络事件
* worker进程是对等的，同等竞争来自客户端的请求
* worker进程互相无影响，无需加锁，且崩溃后可以快速重启
* Nginx采用异步非阻塞方式处理请求(高并发的关键)
* 模块静态编译

![Nginx架构图](/static/nginx-arch.png)
]

---

.left-column[
### Nginx简介
### Nginx架构
### 模块化
]

.right-column[
### 模块化体系结构

* 核心 + 扩展
* KISS(Keep it simple, stupid)
* 更好的扩展性

### 模块分类
* event module — 独立于OS的事件处理机制的框架，及提供了各具体事件的处理
* phase handler — 也称handler模块，负责处理客户端请求并产生待响应内容
* output filter — 也称filter模块，负责对输出的内容进行处理
* upstream — 实现反向代理的功能，将真正的请求转发到后端服务器上，并从后端服务器上读取响应，发回客户端
* load-balancer — 负载均衡模块
]

---

layout: false
.left-column[
### 基本控制
]

.right-column[

### 启动
```bash
nginx -c /path/to/nginx.conf
```

### 测试配置文件
```bash
nginx -c /path/to/nginx.conf -t
```

### 其他控制指令
```bash
nginx -s signal
```

* stop — 立即停止守护进程(SIGTERM)
* quit — 优雅地停止守护进程(SIGQUIT)
* reload — 重新载入配置文件
* reopen — 重新打开日志文件

.footnote[.black[qunar.com]]
]

---

.left-column[
### 基本控制
### 配置文件
]

.right-column[
### 注释
```http
# 以#开头的行为注释行
```

### 指令
#### 简单指令
> 由空白分割的指令名、参数以及结尾的 `;` 组成

> 示例:
```http
worker_processes 1;
```

#### 指令块
> 以 `{` 和 `}` 组成的区块，里面包含简单指令，支持嵌套
> 
> (main, events, http, server, location)

> 示例:
```http
http {
    server {
    }
}
```

]

---

.left-column[
### 基本控制
### 配置文件
]

.right-column[
### 组织和包含

将另一个文件或者符合模式的文件引入当前配置文件中
```bash
syntax:  include file | mask;
default: -
context: any
```

示例:
```http
include mime.types;
include vhosts/*.conf;
```

#### 常用的配置文件名称及含义
| 标准名称 | 描述 |
| :------ | :-- |
| nginx.conf | 基本配置文件 |
| mime.types | 一个文件扩展列表文件，他们与MIME类型关联 |
| fastcgi.conf | 与FastCGI相关的配置文件 |
| proxy.conf | 与Proxy相关的配置文件 |
| sites.conf | 配置Nginx提供的网站 |

]

---

.left-column[
### 基本控制
### 配置文件
]

.right-column[
### 指令值的单位
Nginx配置中支持单位，可以增强可读性

| 缩写 | 说明 |
| :-- | :-- |
| ms | milliseconds |
| s | seconds |
| m | minutes |
| h | hours |
| d | days |
| w | weeks |
| M | months, 30 days |
| y | years, 365 days |

### 变量
在Nginx配置中，变量只能存放一种类型的值，即字符串类型

示例:
```http
location ^~ /qunar/ {
    log_format main '$pid - $server_name - $remote_addr'
}
```

[Nginx变量列表](http://nginx.org/en/docs/varindex.html)

]

---


.left-column[
### 基本控制
### 配置文件
### 常用指令
]

.right-column[
### daemon
启用或禁用守护进程模式

```bash
syntax:  daemon on | off;
default: daemon on;
context: main
```

### error_log
配置错误日志位置及级别

```bash
syntax:  error_log file|stderr|syslog:server=address[,parameter=value] 
         [debug | info | notice | warn | error |crit | alert | emerg];
default: error_log logs/error.log error;
context: main, http, server, location
```

示例:
```http
error_log /dev/null debug;
```

### user
设置运行Nginx进程的用户和组，如果不指定组，则其与user同名

```bash
syntax:  user user [group];
default: user nobody nobody;
context: main
```

]

---

.left-column[
### 基本控制
### 配置文件
### 常用指令
]

.right-column[

### log_not_found
开启或禁用404记录

```bash
syntax:  log_not_found on | off;
default: log_not_found on;
context: http, server, location
```

### worker_processes
定义worker进程的数量

```bash
syntax:  worker_processes number | auto;
default: worker_processes 1;
context: main
```

### worker_connections
定义一个worker进程的最大连接数

```bash
syntax:  worker_connections number;
default: worker_connections 512;
context: events
```

]

---

.left-column[
### HTTP核心模块
]

.right-column[
### 区块结构

* http — 为HTTP服务器提供配置上下文
* server — 表示开始设置虚拟主机的配置
* location — 为某个请求URI（路径）建立配置

嵌套关系
```http
http {
    server {
        listen 8001;
        server_name server1.qunar.com;
        location /foo {
            echo "$host";
        }
        location /bar {
            echo "$host";
        }
    }
    server {
        listen 8002;
        server_name server2.qunar.com;
        location / {
            echo "$host";
        }
    }
}
http {
    server {
        listen 8003;
        server_name server3.qunar.com;
        location / {
            echo "$host";
        }
    }
}
```

]

---

.left-column[
### HTTP核心模块
]

.right-column[
## server区块常用指令

### listen
设置Web服务监听套接字的IP地址/端口号

```bash
syntax:  listen address[:port] [other];
         listen port [other];
default: listen *:80 | *:8000;
context: server
```

示例:
```http
listen 127.0.0.1:8000;
listen 127.0.0.1;
listen 8000;
listen *:8000;
listen localhost:8000;
# For IPv6
listen [::]:8000;
listen [::1];
```

]

---

.left-column[
### HTTP核心模块
]

.right-column[
### server_name
设置虚拟主机的名称

```bash
syntax:  server_name name ...;
default: server_name "";
context: server
```

示例:
```http
server_name example.com www.example.com;
server_name example.com *.example.com www.example.*;
server_name .example.com; # example.com *.example.com
server_name www.example.com ~^www\d+\.example\.com$;
```

#### 匹配规则

Nginx检查请求的 `Host	` 头来决定处理此请求的虚拟主机，如果 `Host` 头没有匹配任何一个虚拟主机，或者没有包含 `Host` 头，则将请求分发到此端口的默认虚拟主机。如果没有显示使用 `default_server` 选项，则第一个被列出的虚拟主机被认为是默认虚拟主机

#### 优先级

1. 确切的名字；
1. 最长的以星号起始的通配符名字，比如“*.example.com”
1. 最长的以星号结束的通配符名字，比如“mail.*”；
1. 第一个匹配的正则表达式名字（按在配置文件中出现的顺序）
]

---

.left-column[
### HTTP核心模块
]

.right-column[
### 测试

.pull-left[
```http
server {
    listen       80 default_server;
    server_name  _;
    location / {
        echo "$server_name";
        echo "$host";
    }
}
server {
    listen       80;
    server_name  example.org
                 www.example.org;
    ...
}
server {
    listen       80;
    server_name  *.example.org;
    ...
}
server {
    listen       80;
    server_name  mail.*;
    ...
}
server {
    listen       80;
    server_name  
    ~^(?<user>mdl.+)\.example\.net$;
    ...
}
server {
    listen       80;
    server_name 
    ~^(?<user>.+)\.example\.net$;
    ...
}
```
]


.pull-right[
```bash
➜  ~  curl 'http://localhost:80/' \
-H 'Host: xxxx.example.cn'
_
xxxx.example.cn

➜  ~  curl 'http://localhost:80/' \
-H 'Host: example.org'
example.org
example.org

➜  ~  curl 'http://localhost:80/' \
-H 'Host: www.example.org'
example.org
www.example.org

➜  ~  curl 'http://localhost:80/' \
-H 'Host: mdl.example.org'
*.example.org
mdl.example.org

➜  ~  curl 'http://localhost:80/' \
-H 'Host: mail.qunar.org'
mail.*
mail.qunar.org

➜  ~  curl 'http://localhost:80/' \
-H 'Host: mdl.example.net'
~^(?<user>.+)\.example\.net$
mdl.example.net

➜  ~  curl 'http://localhost:80/' \
-H 'Host: mdl1.example.net'
~^(?<user>mdl.+)\.example\.net$
mdl1.example.net
```
]

]

---

.left-column[
### HTTP核心模块
]

.right-column[
### location
为某个请求URI建立配置

```bash
syntax:  location [ = | ~ | ~* | ^~ ] uri { ... }
         location @name { ... }
default: —
context: server, location
```

#### `=` 修饰符
URI的定位必须与指定的模式精确匹配（不能使用正则表达式）

```http
server {
    listen       80;
    location = /foo {
        echo "$uri";
    }
}
```

* `http://localhost:80/foo` 可用（严格匹配）
* `http://localhost:80/FOO` 取决于操作系统是否区分大小写
* `http://localhost:80/foo?x=1&y=2` 可用（忽略参数）
* `http://localhost:80/foo/` 不可用（结尾有斜杠）
* `http://localhost:80/foobar` 不可用（指定模式后有额外字符）

]

---

.left-column[
### HTTP核心模块
]

.right-column[
#### 无修饰符
URI必须以指定模式开始，不可以使用正则表达式

```http
server {
    listen       80;
    location /foo {
        echo "$uri";
    }
}
```

* `http://localhost:80/foo` 可用（严格匹配）
* `http://localhost:80/FOO` 取决于操作系统是否区分大小写
* `http://localhost:80/foo?x=1&y=2` 可用（忽略参数）
* `http://localhost:80/foo/` 可用
* `http://localhost:80/foobar` 可用

#### `～` 修饰符
客户端请求的URI与指定的正则表达式匹配必须区分大小写

```http
server {
    listen       80;
    location ~ ^/foo$ {
        echo "$uri";
    }
}
```

* `http://localhost:80/foo` 可用（严格匹配）
* `http://localhost:80/FOO` 不可用（区分大小写）
* `http://localhost:80/foo?x=1&y=2` 可用（忽略参数）
* `http://localhost:80/foo/` 不可用（结尾有斜杠）
* `http://localhost:80/foobar` 不可用

]

---

.left-column[
### HTTP核心模块
]

.right-column[
#### `～*` 修饰符
客户端请求的URI与指定的正则表达式匹配，不区分大小写

```http
server {
    listen       80;
    location ~* ^/foo$ {
        echo "$uri";
    }
}
```

* `http://localhost:80/foo` 可用（严格匹配）
* `http://localhost:80/FOO` 可用（不区分大小写）
* `http://localhost:80/foo?x=1&y=2` 可用（忽略参数）
* `http://localhost:80/foo/` 不可用（结尾有斜杠）
* `http://localhost:80/foobar` 不可用

#### `^~` 修饰符
如果最大前缀匹配的路径以 `^~` 开始，那么Nginx不再检查正则表达式

#### `@` 修饰符
定义命名 `location` 区段，这些区段客户端不能访问，只能由内部产生的请求访问
]

---

.left-column[
### HTTP核心模块
]

.right-column[
#### 优先级

1. 带有 `=` 修饰符的 `location` 区段
1. 没有修饰符的 `location` 区段（满足精确匹配）
1. 带有 `^~` 修饰的 `location` 区段
1. 带有 `~` 或 `~*` 修饰的 `location` 区段
1. 没有修饰符的 `location` 区段（满足以指定模式开始的匹配）

#### 一个例子
```
location = / {
    echo "= /";
}
location / {
    echo "/";
}
location /documents/ {
    echo "/documents/";
}
location ^~ /images/ {
    echo "^~ /images/";
}
location ~* \.(gif|jpg|jpeg)$ {
    echo "~* \.(gif|jpg|jpeg)";
}
```

```
➜  ~  curl http://localhost:80/
= /
➜  ~  curl http://localhost:80/index.html
/
➜  ~  curl http://localhost:80/documents/document.html
/documents/
➜  ~  curl http://localhost:80/images/1.gif
^~ /images/
➜  ~  curl http://localhost:80//documents/1.jpg
~* \.(gif|jpg|jpeg)
```
]

---

.left-column[
### HTTP核心模块
]

.right-column[
#### `~*` 修饰符 vs 无修饰符

```http
server {
    listen       80;
    location ~* ^/document$ {
        echo "~* ^/document";
    }
    location /doc {
        echo "/doc";
    }
}
```

```bash
➜  ~  curl http://localhost:80/doc
/doc
➜  ~  curl http://localhost:80/docu
/doc
➜  ~  curl http://localhost:80/document
~* ^/document
➜  ~  curl http://localhost:80/document/
/doc
```

```http
server {
    listen       80;
    location /document {
        echo "/document";
    }
    location ~* ^/document$ {
        echo "~* ^/document";
    }
}
```

```bash
➜  ~  curl http://localhost:80/document
~* ^/document
➜  ~  curl http://localhost:80/document/
/document
```
]

---

.left-column[
### HTTP核心模块
]

.right-column[

#### `~^` 修饰符 vs `~*` 修饰符

```http
# ~^ 在配置文件中先出现
server {
    listen       80;
    location ^~ /doc {
        echo "^~ /doc";
    }
    location ~* ^/document$ {
        echo "~* ^/document";
    }
}
# ~^ 在配置文件中后出现
server {
    listen       80;
    location ~* ^/document$ {
        echo "~* ^/document";
    }
    location ^~ /doc {
        echo "^~ /doc";
    }
}
```

```bash
# ~^ 在配置文件中先出现
➜  ~  curl http://localhost:80/document
^~ /doc
➜  ~  curl http://localhost:80/document/
^~ /doc
# ~^ 在配置文件中后出现
➜  ~  curl http://localhost:80/document
^~ /doc
➜  ~  curl http://localhost:80/document/
^~ /doc
```
]

---

.left-column[
### HTTP核心模块
]

.right-column[
#### `~` 修饰符 vs `~*` 修饰符
```http
# ~ 在配置文件中先出现
server {
    listen       80;
    location ~ /a.txt {
        echo "/a.txt";
    }
    location ~* /a.txt {
        echo "~* /a.txt";
    }
}

# ~ 在配置文件中后出现
server {
    listen       80;
    location ~* /a.txt {
        echo "~* /a.txt";
    }
    location ~ /a.txt {
        echo "/a.txt";
    }
}
```

```bash
# ~ 在配置文件中先出现
➜  ~  curl http://localhost:80/a.txt
/a.txt
➜  ~  curl http://localhost:80/A.txt
~* /a.txt
# ~ 在配置文件中后出现
➜  ~  curl http://localhost:80/a.txt
~* /a.txt
➜  ~  curl http://localhost:80/A.txt
~* /a.txt
```
]

---

.left-column[
### HTTP核心模块
### Rewrite模块
]

.right-column[
### Rewrite模块
Rewrite模块允许正则替换URI，返回页面重定向，和按条件选择配置

#### 处理顺序

* 处理在server级别中定义的模块指令
* 为请求查找location
* 处理在选中的location中定义的模块指令。如果指令改变了URI，按新的URI查找location。这个循环至多重复10次，之后nginx返回错误500

#### break
停止处理当前这一轮的Rewrote指令集

```bash
syntax:  break;
default: —
context: server, location, if
```

#### return
停止处理并返回指定code给客户端

```bash
syntax:  return code [text];
         return code URL;
         return URL;
default: —
context: server, location, if
```
]

---

.left-column[
### HTTP核心模块
### Rewrite模块
]

.right-column[


#### set
为指定变量variable设置变量值value

```bash
syntax:  set $variable value;
default: —
context: server, location, if
```

#### if
条件判断语句，跟通用编程语言一致

```bash
syntax:  if (condition) { ... }
default: —
context: server, location
```

条件可以是下列任意一种：

* 变量名；如果变量值为空或者是以"0"开始的字符串，则条件为假；
* 使用"="和"!="运算符比较变量和字符串；
* 使用"~"和"~*"运算符匹配变量和正则表达式
* 使用"-f"和"!-f"运算符检查文件是否存在；
* 使用"-d"和"!-d"运算符检查目录是否存在；
* 使用"-e"和"!-e"运算符检查文件、目录或符号链接是否存在；
* 使用"-x"和"!-x"运算符检查可执行文件；

示例:
```http
if ($http_cookie ~* "id=([^;]+)(?:;|$)") {
    set $id $1;
}
if ($request_method = POST) {
    return 405;
}
```
]

---

.left-column[
### HTTP核心模块
### Rewrite模块
]

.right-column[
#### rewrite
如果指定的正则表达式能匹配URI，此URI将被replacement参数定义的字符串改写。rewrite指令按其在配置文件中出现的顺序执行。flag可以终止后续指令的执行。如果replacement的字符串以 `http://` 或 `https://` 开头，Nginx将结束执行过程，并返回给客户端一个重定向。

```bash
syntax:  rewrite regex replacement [flag];
default: —
context: server, location, if
```

可选的flag参数可以是其中之一:

* last — 停止执行当前的Rewrite指令集，然后查找匹配改变后URI的新location；
* break — 停止执行当前这一轮的Rewrite指令集；
* redirect — 在replacement字符串未以 `http://` 或 `https://` 开头时，使用返回状态码为302的临时重定向；
* permanent — 返回状态码为301的永久重定向。

示例:
```http
server {
    listen       80;
    rewrite ^/info/(.*)$ /user_info?username=$1;
    location /user_info {
        echo "$uri";
        echo "$args";
    }
}
```
```bash
➜  ~  curl http://localhost:80/info/dongliang.ma
/user_info
username=dongliang.ma
```
]

---

.left-column[
### HTTP核心模块
### Rewrite模块
### Index
]

.right-column[
### Index模块
ngx_http_index_module处理以斜线字符(‘/’)结尾的请求

#### index
定义将要被作为默认页的文件

```bash
syntax:  index file ...;
default: index index.html;
context: http, server, location
```

示例（内部重定向）:
```http
server {
    listen       80;
    location = / {
        index index.html;
    }
    location / {
        echo "redirect";
    }
}
```

```bash
➜  ~  curl http://localhost:80/
redirect
```
]

---

.left-column[
### HTTP核心模块
### Rewrite模块
### Index
]

.right-column[
### AutoIndex模块
ngx_http_autoindex_module模块可以列出目录中的文件(一般当ngx_http_index_module模块找不到默认主页的时候，会把请求转给 ngx_http_autoindex_module模块去处理)

#### autoindex
开启或者关闭列出目录中文件的功能

```bash
syntax:  autoindex on | off;
default: autoindex off;
context: http, server, location
```

示例:
```http
location / {
    index foobar.html;
    autoindex on;
}
```

```bash
➜  ~  curl http://localhost:80/
<html>
<head><title>Index of /</title></head>
<body bgcolor="white">
<h1>Index of /</h1><hr><pre><a href="../">../</a>
<a href="50x.html">50x.html</a>     22-Nov-2013 04:19  383
<a href="index.html">index.html</a> 22-Nov-2013 04:19  151
</pre><hr></body>
</html>
```

#### note
如果只是想提供文件下载，不需要开启 `autoindex`，直接用 `root` 指令指定目录即可.
]

---

.left-column[
### HTTP核心模块
### Rewrite模块
### Index
### Upstream
]

.right-column[
### Upstream模块
该模块为后端服务器提供简单的负载均衡

#### upstream
定义一组服务器。这些服务器可以监听不同的端口

```bash
syntax:  upstream name { ... }
default: —
context: http
```

示例:

```http
upstream backend {
    server l-ngab1.ops.cn8.qunar.com weight=5;
    server 127.0.0.1:8001       max_fails=3 fail_timeout=30s;
    server 127.0.0.1:8002;
}
```

默认情况下，Nginx按加权轮转的方式将请求分发到各服务器。在上面的例子中，每7个请求会通过以下方式分发：

* 5个请求分到l-ngab1.ops.cn8.qunar.com
* 1个请求分到第二个服务器
* 1个请求分到第三个服务器

与服务器通信的时候，如果出现错误，请求会被传给下一个服务器，直到所有可用的服务器都被尝试过。 如果所有服务器都返回失败，客户端将会得到最后通信的那个服务器的（失败）响应结果。

]

---

.left-column[
### HTTP核心模块
### Rewrite模块
### Index
### Upstream
]

.right-column[
#### server
定义服务器的地址和其他参数

```bash
syntax:  server address [parameters];
default: —
context: upstream
```

可选参数:

* weight=number — 设定服务器的权重，默认是1
* max_fails=number — 设定Nginx与服务器通信的尝试失败的次数
* fail_timeout=time — 设定统计失败尝试次数的时间段
* backup — 标记为备用服务器。当主服务器不可用后，请求会被传给这些服务器
* down — 标记服务器永久不可用，可以跟ip_hash指令一起使用

#### ip_hash
指定服务器组的负载均衡方法，请求基于客户端的IP地址在服务器间进行分发

```bash
syntax:  ip_hash;
default: —
context: upstream
```

#### least_conn
指定服务器组的负载均衡方法，根据权重值，将请求发到活跃连接数最少的那台服务器

```bash
syntax:  least_conn;
default: —
context: upstream
```
]

---

.left-column[
### HTTP核心模块
### Rewrite模块
### Index
### Upstream
### Proxy模块
]

.right-column[
### Proxy模块
ngx_http_proxy_module模块允许传送请求到其它服务器

#### proxy_pass
设置后端服务器的协议和地址，也可以设置本地location

```bash
syntax:  proxy_pass URL;
default: —
context: location, if in location, limit_except
```

示例:

```http
server {
    listen       80;
    location /frontend/ {
        proxy_pass       http://l-ngab1.ops.cn8.qunar.com:8002/backend/;
    }
}
```

```http
server {
    listen       8002;
    location / {
        echo "$uri";
    }
}
```

```bash
➜  ~  curl http://l-dongliang.ops.dev.cn6.qunar.com:80/frontend/
/backend/
➜  ~  curl http://l-dongliang.ops.dev.cn6.qunar.com:80/frontend/mdl/13412
/backend/mdl/13412
```
]

---

.left-column[
### HTTP核心模块
### Rewrite模块
### Index
### Upstream
### Proxy模块
]

.right-column[
#### proxy_set_header
允许重新定义或者添加发往后端服务器的请求头

```bash
syntax:  proxy_set_header field value;
default: proxy_set_header Host $proxy_host;
         proxy_set_header Connection close;
context: http, server, location
```

#### proxy_http_version
设置代理使用的HTTP协议版本。默认使用的版本是1.0，而1.1版本则推荐在使用keepalive连接时一起使用

```bash
syntax:  proxy_http_version 1.0 | 1.1;
default: proxy_http_version 1.0;
context: http, server, location
```
]

---

.left-column[
### HTTP核心模块
### Rewrite模块
### Index
### Upstream
### Proxy模块
### RealIP模块
]

.right-column[
### RealIP模块
这个模块允许从请求Headers里更改客户端的IP地址值

#### set_real_ip_from
描述了值得信赖的地址，这可以让nginx更准确的替换地址

```bash
syntax:  set_real_ip_from address | CIDR | unix:;
default: —
context: http, server, location
```

#### real_ip_header
```bash
syntax:  real_ip_header field | X-Real-IP | X-Forwarded-For | proxy_protocol;
default: real_ip_header X-Real-IP;
context: http, server, location
```

]

---

.left-column[
### HTTP核心模块
### Rewrite模块
### Index
### Upstream
### Proxy模块
### RealIP模块
]

.right-column[
示例:

```xml
location /real_ip {
    proxy_pass       http://l-ngab1.ops.cn8.qunar.com:8000;
    proxy_set_header Host      $host;
    proxy_set_header X-Real-IP $remote_addr;
}
location /no_real_ip {
    proxy_pass       http://l-ngab1.ops.cn8.qunar.com:8001;
    proxy_set_header Host      $host;
}
```

```xml
server {
    listen       8001;
    server_name  localhost;
    location / {
        set_real_ip_from   192.168.237.110;
        real_ip_header     X-Real-IP;
        echo "real_ip: $host $http_x_real_ip";
    }
}

server {
    listen       8000;
    server_name  localhost;
    location / {
        echo "no_real_ip: $host $http_x_real_ip";
    }
}
```

```bash
➜  ~  curl http://l-dongliang.ops.dev.cn6.qunar.com:80/no_real_ip
real_ip: l-dongliang.ops.dev.cn6.qunar.com
➜  ~  curl http://l-dongliang.ops.dev.cn6.qunar.com:80/real_ip
no_real_ip: l-dongliang.ops.dev.cn6.qunar.com 192.168.127.182
```
]

---

.left-column[
### HTTP核心模块
### Rewrite模块
### Index
### Upstream
### Proxy模块
### RealIP模块
### Gzip模块
]

.right-column[
### Gzip模块
对输出的数据流进行实时压缩

#### gzip
开启或者关闭gzip模块

```bash
syntax:  gzip on | off;
default: gzip off;
context: http, server, location, if in location
```

#### gzip_comp_level
gzip压缩比，1 压缩比最小处理速度最快，9 压缩比最大但处理最慢

```bash
syntax:  gzip_comp_level level;
default: gzip_comp_level 1;
context: http, server, location
```

#### gzip_min_length
设置允许压缩的页面最小字节数，页面字节数从header头中的Content-Length中进行获取

```bash
syntax:  gzip_min_length length;
default: gzip_min_length 20;
context: http, server, location
```
]

---

.left-column[
### HTTP核心模块
### Rewrite模块
### Index
### Upstream
### Proxy模块
### RealIP模块
### Gzip模块
]

.right-column[
#### gzip_http_version
设置使用gzip的最低HTTP版本

```bash
syntax:  gzip_http_version 1.0 | 1.1;
default: gzip_http_version 1.1;
context: http, server, location
```

#### gzip_types
匹配MIME类型进行压缩

```bash
syntax:  gzip_types mime-type ...;
default: gzip_types text/html;
context: http, server, location
```

示例:

```http
server {
    listen       80;
    location /gzip {
        gzip            on;
        gzip_min_length 10;
        gzip_types      text/plain application/xml application/octet-stream;
        echo "abcdefghijklmnopqrstuvwxyz";
    }
    location /no_gzip {
        echo "abcdefghijklmnopqrstuvwxyz";
    }
}
```

]

---

.left-column[
### Nginx&Python
]

.right-column[
### FastCGI模块
这个模块允许Nginx与FastCGI进程交互，并通过传递参数来控制FastCGI进程工作

#### fastcgi_pass
设置FastCGI服务器的地址

```bash
syntax:  fastcgi_pass address;
default: —
context: location, if in location
```

#### fastcgi_param
该指令指定的参数,将被传递给FastCGI-server

```bash
syntax:  fastcgi_param parameter value [if_not_empty];
default: —
context: http, server, location
```

#### fastcgi_split_path_info
该指令的参数是一个正则表达式

* 分组一为 `$fastcgi_script_name`
* 分组二为 `$fastcgi_path_info`

```bash
syntax:  fastcgi_split_path_info regex;
default: —
context: location
```

]

---

.left-column[
### Nginx&Python
]

.right-column[
### opsdb上的配置
```http
server {
    listen       443;
    server_name  opsdb.corp.qunar.com;
    client_max_body_size 20M;
    charset utf-8;
    # SSL conf...

    location /busi_report.html {
	root /var/www/html/;
    }
    location ~ ^/static/extjs/.*$ {
        root /home/q/opsdb/www/opsdb;
        expires 3d;
        gzip  on;
        gzip_min_length  1000;
        gzip_types       text/plain application/x-javascript 
                         text/css application/xml;
        gzip_disable     "MSIE [1-6]\.";
    }
    location ~ ^/static/.*(js|css|jpg|jpeg|gif|png|bmp)$ {
        root /home/q/opsdb/www/opsdb;
    }
    location / {
            root /home/q/opsdb/www;
            include fastcgi_params;
            fastcgi_split_path_info ^(/)(.*)$;
            fastcgi_param PATH_INFO $fastcgi_path_info;
            fastcgi_param SCRIPT_NAME $fastcgi_script_name;
            fastcgi_pass 127.0.0.1:9010;
            fastcgi_read_timeout 180;
            fastcgi_send_timeout 180;
    }
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   html;
    }

}
```
]

---

### 一些资源

* [Nginx官网](http://nginx.org/)
* [Tengine](http://tengine.taobao.org/)
* [OpenResty](http://www.openresty.org/)
* [Nginx开发从入门到精通](https://github.com/taobao/nginx-book)
* [NginxChs](http://wiki.nginx.org/NginxChs)
* [NginxModuleDevGuide_CHN](https://code.google.com/p/emillers-guide-to-nginx-module-chn/wiki/NginxModuleDevGuide_CHN)
* [agentzh的Nginx教程](http://openresty.org/download/agentzh-nginx-tutorials-zhcn.html)
