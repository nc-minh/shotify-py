proto:
	rm -f pb/*.py
	python3 -m grpc_tools.protoc -I protos --python_out=. --grpc_python_out=. ./protos/*.proto
server:
	python3 server.py
client:
	python3 client.py

.PHONY: proto server-py
