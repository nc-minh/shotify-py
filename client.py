from __future__ import print_function
import service_shotifypy_pb2_grpc
import rpc_make_img_pb2
import grpc
import logging
import sys
sys.path.append('/pb')


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print("Starting ...")
    with grpc.insecure_channel('localhost:6060') as channel:
        stub = service_shotifypy_pb2_grpc.ShotifypyStub(channel)
        response = stub.HtmlSnapshot(
            rpc_make_img_pb2.MakeImageFromHtmlRequest(html="<h1 align='center'>Test</h1>"))
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()
