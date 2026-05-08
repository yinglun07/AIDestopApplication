import grpc
from concurrent import futures
import ai_service_pb2
import ai_service_pb2_grpc

from orchestrator import handle_query  # your existing logic


class QueryService(ai_service_pb2_grpc.QueryServiceServicer):
    def ProcessQuery(self, request, context):
        result = handle_query(request.query, request.video_path)

        return ai_service_pb2.QueryResponse(
            result=result
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    ai_service_pb2_grpc.add_QueryServiceServicer_to_server(QueryService(), server)

    server.add_insecure_port('[::]:50051')
    server.start()

    print("gRPC server running on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
