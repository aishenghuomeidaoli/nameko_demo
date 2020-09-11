# http server 接收任务，并发调用worker
from flask import Flask, request

from utils import call_all_rpc


class Config:
    # rpc worker 配置
    WORKERS = {
        # 任务code，客户端调用时传递
        'job1': {
            # worker 消息中间件、服务名称、方法名称
            'amqp_uri': 'pyamqp://guest:guest@localhost',
            'service': 'service_job_1',
            'method': 'execute',
        },
        'job2': {
            'amqp_uri': 'pyamqp://guest:guest@localhost',
            'service': 'service_job_2',
            'method': 'execute',
        },
        'job3': {
            'amqp_uri': 'pyamqp://guest:guest@localhost',
            'service': 'service_job_3',
            'method': 'execute',
        },
    }


app = Flask(__name__)
app.config.from_object(Config)


@app.route('/execute/', methods=['POST'])
def execute():
    """执行任务
    调用方式：
    curl --location --request POST 'localhost:5000/execute/' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "jobs": [
            {
                "code": "job1",
                "parameters": {
                    "a": 1,
                    "b": 2
                }
            },
            {
                "code": "job2",
                "parameters": {
                    "a": 3,
                    "b": 4
                }
            }
        ]
    }'

    :return:
    """
    data = request.json  # type: dict
    if not data:
        return {'code': 'ParameterError', 'message': 'Json required.'}
    jobs = data.get('jobs', [])
    workers = []
    for job in jobs:
        code = job.get('job')
        # 根据客户端任务类型找到worker
        worker = app.config.get('WORKERS').get(code)
        if not worker:
            return {'code': 'ParameterError', 'message': 'Invalid job code.'}
        # 将任务参数传入worker中
        worker['parameters'] = job.get('parameters', {})
        workers.append(worker)
    results = call_all_rpc(*workers)
    return {'code': 'Success', 'data': results}


if __name__ == '__main__':
    app.run(debug=True)
