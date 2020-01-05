# Serverless Simple Todo App

## Backend Service

### Local Development and Testing

```bash
# build docker image
docker build -t sls-fastapi-dev -f ./backend/Dockerfile .

# run service
docker-compose -f ./backend/docker-compose.yaml up -d backend

# run test
docker-compose -f ./backend/docker-compose.yaml up test

# clean up
docker-compose -f ./backend/docker-compose.yaml down
```

### Deployment

* CloudFormation
    * Api Gateway custom domain and DNS record
    * [Edge-optimized API endpoint](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-basic-concept.html#apigateway-definition-edge-optimized-api-endpoint) configuration
        * Need ACM certificate in _us-east-1_ for the custom domain 

```bash
export CertIdentifier=<acm-certificate-identifier>
export DomainName=<domain-name>
export HostedZoneId=<hosted-zone-id> 

aws cloudformation deploy --stack-name simple-todo-custom-domain \
    --template-file ./cloudformation/custom-domain.yaml \
    --parameter-overrides \
        CertIdentifier=$CertIdentifier \
        DomainName=$DomainName \
        HostedZoneId=$HostedZoneId
```

* Serverless framework deployment
    * Deploy service built by [FastAPI](https://fastapi.tiangolo.com/)
    * Lambda handler created by [mangum](https://github.com/erm/mangum)
        * Slight modification of `Mangum` to accomodate Api Gateway base path mapping
    * Extra resources created together
        * DynamoDB table
        * Gateway responses: `DEFAULT_4XX` and `DEFAULT_5XX`
        * Base path mapping
    * Api's root resource id is exported to be referenced in the cognito stack template

```bash
cd backend && sls deploy
```

## Frontend App

### Deployment

* CloudFormation
    * Cognito User/Identity Pool and App Client

```bash
aws cloudformation deploy --stack-name simple-todo-cognito \
    --template-file ./cloudformation/cognito.yaml \
    --capabilities CAPABILITY_NAMED_IAM
```
