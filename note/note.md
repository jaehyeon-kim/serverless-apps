```bash
# testing multi stage build
docker build --target sls-fastapi-build \
    -t sls-fastapi-build -f ./backend/Dockerfile-ms . \
    && docker build --target sls-fastapi \
        -t sls-fastapi -f ./backend/Dockerfile-ms . \
    && docker build --target sls-fastapi-dev \
        -t sls-fastapi-dev -f ./backend/Dockerfile-ms .
```