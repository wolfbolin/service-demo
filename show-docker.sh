#!/bin/bash
docker_name="demo-service"
docker ps -a | grep ${docker_name}
docker logs -f ${docker_name}