> 记录如何在`python`中进行`nacos`的相关操作

# 接口调用
* 欢迎界面
  ```
   http://127.0.0.1:5000/
  ```
* 获取`Nacos`配置
    ```
    http://127.0.0.1:5000/config
    ```
* 获取`Nacos`实例
  ```bash
    http://127.0.0.1:5000/instances?service_name=spring-mybatis-app
  ```
* 服务调用
    ```bash
    http://127.0.0.1:5000/invoke?service=spring-mybatis-app&method=user/queryAll
    ```
