from fastapi import Request

def get_minio_client(request: Request):
    return request.app.state.minio_client