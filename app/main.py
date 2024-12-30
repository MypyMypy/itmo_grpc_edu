import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from concurrent import futures
import grpc
from grpc_reflection.v1alpha import reflection  # Импорт reflection
import app.glossary_pb2 as glossary_pb2
import app.glossary_pb2_grpc as glossary_pb2_grpc
from app.crud import get_all_terms, create_term, update_term, delete_term, get_term_by_name
from app.models import SessionLocal
from app.schemas import TermCreate


class GlossaryServiceServicer(glossary_pb2_grpc.GlossaryServiceServicer):
    def GetTerms(self, request, context):
        db = SessionLocal()
        terms = get_all_terms(db)
        db.close()
        return glossary_pb2.TermsList(
            terms=[
                glossary_pb2.TermResponse(id=term.id, name=term.name, description=term.description)
                for term in terms
            ]
        )

    def AddTerm(self, request, context):
        db = SessionLocal()
        if get_term_by_name(db, request.name):
            context.set_details("Term already exists")
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            db.close()
            return glossary_pb2.TermResponse()
        term = create_term(db, TermCreate(name=request.name, description=request.description))
        db.close()
        return glossary_pb2.TermResponse(id=term.id, name=term.name, description=term.description)

    def UpdateTerm(self, request, context):
        db = SessionLocal()
        existing_term = get_term_by_name(db, request.current_name)
        if not existing_term:
            context.set_details("Term not found")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            db.close()
            return glossary_pb2.TermResponse()
        updated_term = update_term(db, request.current_name, TermCreate(
            name=request.updated_term.name,
            description=request.updated_term.description
        ))
        db.close()
        return glossary_pb2.TermResponse(
            id=updated_term.id, name=updated_term.name, description=updated_term.description
        )

    def DeleteTerm(self, request, context):
        db = SessionLocal()
        existing_term = get_term_by_name(db, request.name)
        if not existing_term:
            context.set_details("Term not found")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            db.close()
            return glossary_pb2.DeleteResponse(message="Term not found")
        delete_term(db, request.name)
        db.close()
        return glossary_pb2.DeleteResponse(message="Term deleted successfully")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    glossary_pb2_grpc.add_GlossaryServiceServicer_to_server(GlossaryServiceServicer(), server)

    service_names = [glossary_pb2_grpc.GlossaryService.__name__]

    reflection.enable_server_reflection(service_names, server)

    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server started on port 50051 with reflection enabled...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
