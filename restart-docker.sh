#!/bin/bash
docker_name="demo-service"
docker restart ${docker_name} && docker logs -f ${docker_name}
