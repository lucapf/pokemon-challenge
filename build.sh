#!/bin/bash
docker buildx build -f Dockerfile.backend -o type=docker -t pokemon-backend:0.0.1 . 
docker buildx build -f Dockerfile.database -o type=docker -t pokemon-database:0.0.1 .
docker-compose up
