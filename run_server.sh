#!/bin/bash


args=("$@")

if [ "external" == ${args[0]} ];then
	if [ ${args[1]} ] && [ "background" == ${args[1]} ];then
		echo "Run server with HTTP and Background runnning"
		nohup uvicorn main:app --host 0.0.0.0 --port 8001 &
	else
		echo "Run server with HTTP"
		uvicorn main:app --host 0.0.0.0 --port 8001
	fi
elif [ "https" == ${args[0]} ];then
	if [ ${args[1]} ] && [ "background" == ${args[1]} ];then
		echo "Run server with HTTPS and Background runnning"
		nohup uvicorn main:app --host 0.0.0.0 --port 8001 --ssl-keyfile ./key.pem --ssl-certfile ./cert.pem &
	else
		echo "Run server with HTTPS"
		uvicorn main:app --host 0.0.0.0 --port 8001 --ssl-keyfile ./key.pem --ssl-certfile ./cert.pem
	fi
elif [ "local" == ${args[0]} ];then
	if [ ${args[1]} ] && [ "background" == ${args[1]} ];then
		echo "Run server in Local and Background runnning"
		nohup uvicorn main:app --host 0.0.0.0 --port 8001 &
	else
		echo "Run server in Local"
		uvicorn main:app --host 0.0.0.0 --port 8001
	fi
else
	echo "invaild parameter."
fi