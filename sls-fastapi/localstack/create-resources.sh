#!/bin/bash
aws cloudformation create-stack \
    --stack-name simple-todo \
    --template-body file:///tmp/dyanmodb.yaml \
    --endpoint-url=http://localhost:4581
