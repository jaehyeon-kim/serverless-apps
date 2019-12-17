# serverless-apps

### Build Docker Image

```bash
docker build -t sls-fastapi-dev -f ./backend/Dockerfile .
# testing multi stage build
docker build --target sls-fastapi-build \
    -t sls-fastapi-build -f ./backend/Dockerfile-ms . \
    && docker build --target sls-fastapi \
        -t sls-fastapi -f ./backend/Dockerfile-ms . \
    && docker build --target sls-fastapi-dev \
        -t sls-fastapi-dev -f ./backend/Dockerfile-ms .
```
### Run Service

```bash
# if image is built
docker-compose up -d backend
# if not
docker-compose up -b --build backend
```

### Run Test

```bash
# if image is built
docker-compose up -d test && docker-compose down
# if not
docker-compose up -b --build test && docker-compose down
```
