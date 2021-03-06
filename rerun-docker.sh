#!/bin/bash
docker_name="demo-service"
docker image prune -f
docker stop ${docker_name}
docker rm ${docker_name}
echo -e "\033[5;36mOrz 旧容器(镜像)已清理\033[0m"

docker run -itd \
	--restart unless-stopped \
	--name ${docker_name} \
	-e SERVICE_ENV=production \
	-v $(pwd):/var/app \
	-p 12899:80 \
	${docker_name}:latest
echo -e "\033[5;36mOrz 镜像启动完成\033[0m"
docker ps -a
docker logs ${docker_name} -f