项目使用Python3

# 结构

* http_server: http rest api，接收批量任务参数，任务生产者
* rpc_worker: 任务消费者，有三个服务：job1/2/3, 分别延迟1/2/3秒

# 启动方式

1. 消息队列：可以使用docker创建rabbitmq容器：`docker run -d -p 5672:5672 rabbitmq:3`
2. rpc_worker：`nameko run rpc_worker`
3. http_server：`python http_server.py`

# 测试

* job1 x 1， 约1秒
```shell script
curl --location -s -w %{time_total} --request POST 'localhost:5000/execute/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "jobs": [
        {
            "job": "job1",
            "parameters": {
                "a": 1,
                "b": 2
            }
        }
    ]
}'
```

* job1 x 2， 约1秒
```shell script
curl --location -s -w %{time_total} --request POST 'localhost:5000/execute/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "jobs": [
        {
            "job": "job1",
            "parameters": {
                "a": 1,
                "b": 2
            }
        },
        {
            "job": "job1",
            "parameters": {
                "a": 1,
                "b": 2
            }
        }
    ]
}'
```

* job1 x 1 + job2 x 3 + job3 x 1， 约3秒
```shell script
curl --location -s -w %{time_total} --request POST 'localhost:5000/execute/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "jobs": [
        {
            "job": "job1",
            "parameters": {
                "a": 1,
                "b": 2
            }
        },
        {
            "job": "job2",
            "parameters": {
                "a": 1,
                "b": 2
            }
        },
        {
            "job": "job2",
            "parameters": {
                "a": 1,
                "b": 2
            }
        },
        {
            "job": "job2",
            "parameters": {
                "a": 1,
                "b": 2
            }
        },
        {
            "job": "job3",
            "parameters": {
                "a": 1,
                "b": 2
            }
        }
    ]
}'
```
