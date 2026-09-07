#!/usr/bin/env python3
"""PoC gRPC HelloService. Bind per-IP so coffee/tea/canary replies differ.

  BIND_ADDR=30.0.0.10 BIND_PORT=50051 POOL_NAME=COFFEE python3 hello_server.py
"""
from __future__ import annotations

import os
from concurrent import futures

import grpc

from hello_pb2 import HelloReply, HelloRequest
from hello_pb2_grpc import HelloServiceServicer, add_HelloServiceServicer_to_server


class Hello(HelloServiceServicer):
    def __init__(self, label: str) -> None:
        self.label = label

    def SayHello(self, request, context):
        md = dict(context.invocation_metadata())
        echo = md.get("x-poc-add") or md.get("X-PoC-Add") or ""
        if echo:
            context.set_trailing_metadata((("x-echo-x-poc-add", echo),))
        name = request.name or "world"
        print(f"rpc SayHello peer={context.peer()} name={name} md={md}", flush=True)
        return HelloReply(message=f"{self.label} hello {name}")

    def SayGoodbye(self, request, context):
        md = dict(context.invocation_metadata())
        name = request.name or "world"
        print(f"rpc SayGoodbye peer={context.peer()} name={name} md={md}", flush=True)
        return HelloReply(message=f"{self.label} goodbye {name}")


def main() -> None:
    addr = os.environ.get("BIND_ADDR", "0.0.0.0")
    port = os.environ.get("BIND_PORT", "50051")
    label = os.environ.get("POOL_NAME", "COFFEE GRPC - 30.0.0.10")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
    svc = Hello(label)
    add_HelloServiceServicer_to_server(svc, server)
    # 예전 hello_pb2_grpc.py 에도 SayGoodbye 가 붙도록 한 번 더 등록
    server.add_generic_rpc_handlers(
        (
            grpc.method_handlers_generic_handler(
                "hello.HelloService",
                {
                    "SayGoodbye": grpc.unary_unary_rpc_method_handler(
                        svc.SayGoodbye,
                        request_deserializer=HelloRequest.FromString,
                        response_serializer=HelloReply.SerializeToString,
                    ),
                },
            ),
        )
    )
    server.add_insecure_port(f"{addr}:{port}")
    server.start()
    print(f"hello gRPC on {addr}:{port} label={label}", flush=True)
    server.wait_for_termination()


if __name__ == "__main__":
    main()
