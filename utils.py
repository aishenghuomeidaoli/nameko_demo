# 并发调用
import json
from multiprocessing.pool import ThreadPool

from nameko.standalone.rpc import ClusterRpcProxy


def call_rpc(**kwargs):
    config = {
        'AMQP_URI': kwargs.get('amqp_uri')
    }
    with ClusterRpcProxy(config) as cluster_rpc:
        service = getattr(cluster_rpc, kwargs.get('service'))
        method = getattr(service, kwargs.get('method'))
        return json.loads(method(json.dumps(kwargs.get('parameters', {}))))


def call_all_rpc(*workers) -> list:
    pool = ThreadPool(len(workers))
    results = []
    for worker in workers:
        results.append(pool.apply_async(call_rpc, kwds=worker))

    pool.close()
    pool.join()
    results = [r.get() for r in results]
    return results
