# rpc worker，job1/2/3模拟业务逻辑
import json
import time

from nameko.rpc import rpc


class ServiceJob1:
    name = "service_job_1"

    @rpc
    def execute(self, parameter: str) -> str:
        try:
            json_parameter = json.loads(parameter)
        except Exception:
            return json.dumps({'code': 'ParameterError'})
        data = {
            'parameter': json_parameter,
            'service': self.name,
        }
        print(f'service: {self.name} get job: {parameter}')
        time.sleep(1)
        return json.dumps({'code': 'Success', 'data': data})


class ServiceJob2:
    name = "service_job_2"

    @rpc
    def execute(self, parameter: str) -> str:
        try:
            json_parameter = json.loads(parameter)
        except Exception:
            return json.dumps({'code': 'ParameterError'})
        data = {
            'parameter': json_parameter,
            'service': self.name,
        }
        print(f'service: {self.name} get job: {parameter}')
        time.sleep(2)
        return json.dumps({'code': 'Success', 'data': data})


class ServiceJob3:
    name = "service_job_3"

    @rpc
    def execute(self, parameter: str) -> str:
        try:
            json_parameter = json.loads(parameter)
        except Exception:
            return json.dumps({'code': 'ParameterError'})
        data = {
            'parameter': json_parameter,
            'service': self.name,
        }
        print(f'service: {self.name} get job: {parameter}')
        time.sleep(3)
        return json.dumps({'code': 'Success', 'data': data})
