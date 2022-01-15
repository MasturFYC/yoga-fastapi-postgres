docker container stop yoga-app
docker run -p 8080:8080 --rm \
	--mount source=yoga-vue-vol,destination=/home/admin/yoga,readonly \
	--mount source=yoga-host-vol,destination=/home/admin/src \
	--name yoga-app -d yoga-app-env
