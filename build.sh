#!/bin/bash
docker build -f Dockerfile.backend -t pokemon-backend:0.0.1 .
docker build -f Dockerfile.database -t pokemon-database:0.0.1 .