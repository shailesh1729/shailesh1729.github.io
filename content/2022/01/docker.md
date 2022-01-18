---
author: Shailesh Kumar
title: Introduction to Docker
date: 2022-01-18
tags: Docker, Overview
category: Programming
---
This article is an early draft.

Docker is a technology to created isolated
environments on a host computer. 
One can compare Docker to virtual machines on one hand
and language specific virtual environments like `conda`
on the other hand.

* Virtual machines provide complete hardware virtualization.
* Tools like `conda` can provide isolated environments for individual applications
  but they are specific to a particular language (like `Python`).
* `Docker` is language independent. It provides software isolation. 
  But it doesn't provide hardware virtualization.
* It is much more light-weight than virtual machines and independent of specific programming technology.
* Virtual machines are great if you have to guarantee availability of specific amount 
  of hardware resources to each application (where different applications may not be friendly to each other).
* Docker works well if applications running on the host machine are cooperative.
* Docker can run inside virtual machines too.

Checking docker version:
```console
$docker --version
Docker version 19.03.12, build 48a66213fe
```

Checking docker version in a specific format:
```console
$docker version --format '{{.Server.Version}}'
19.03.12
```
## Concepts

The key concepts for learning docker technology are:

- Containers
- Images
- Registries
- Container Networks

### Containers

A docker container is a light-weight virtual machine.

* Each container has its own software stack.
* Containers share the global RAM, CPU, storage and network
  resources of the host computer.
* A docker image contains all the necessary software to run
  a container.
* A container is an isolated process. All child processes
  within a container process are not visible to other containers.
* Unlike virtual machines, docker containers have no
  hardware virtualization.
* Docker containers are built on top of Linux 
  `namespaces` and `cgroups` features in the kernel. 

#### Use Model

* A host machine can run multiple applications.
* Each application runs within its own docker container.
* Each application has its own software and data stack.
* The docker daemon is responsible for running individual
  applications in separate containers.
* Each application can be upgraded independently.
* Since the software stack for each container is isolated,
  hence different applications can have different versions
  of same library/language/program.
* Installing an application as a container doesn't affect
  anything in the global settings/software stack of the
  host machine.
* Application vendors can package all the dependencies
  of an application within the application docker image.
* Distribution of an application in the form of a 
  docker image becomes much simpler.
* All common images are available from a common registry
  like `Docker Hub` or `AWS ECR`.

#### Life-cycle of a Container

* A fresh container can be created from an 
  image `docker create`.
* A container can be renamed `docker rename`.
* A created container can be started `docker start`.
* A fresh container can be created and started `docker run`.
* Commands can be executed inside a running container `docker exec`.
* A running container can be stopped `docker stop`.
* A stopped container can be removed `docker rm`.
* A running container can be restarted `docker restart`.
* A running container can be paused `docker pause`.
* One can wait on a container till it stops `docker wait`.
* One can send a KILL signal to a running container `docker kill`.
* One can attach to a running container (to get terminal access)
  `docker attach`.

#### Attributes/Resources 

Every container has some key attributes/resources 
associated with it.

* ID: A unique ID is associated with each container.
* Image: The image provides the software that is run 
  inside a container.
* Command: The command to be run inside the container.
  The image should contain all the necessary software 
  and data to successfully execute the command.
* Creation time stamp: The time when container was created.
* Status: Current status of the container process.
* Ports: List of network ports that the container is using.
* Name: A container can be associated with a user friendly name.

## Conventions

In the rest of this article, following
conventions are being followed:

* `<container>` refers to either the id of
  a container or its name.
* `<image>` is the name of an image.
   Frequently, it is in a `repository/image`
   format.
* We shall be frequently using some common images from Docker Hub:
  `hello-world`, `busybox`, `ubuntu`, `alpine`, `nginx`, `httpd` in this tutorial.
  * `alpine` is a  minimal Docker image based on Alpine Linux with a complete package index.
  * `busybox` combines tiny versions of many common UNIX utilities into a single small executable.
  * `hello-world` is a minimal Docker image built from scratch.
  * `ubuntu` is an image built from official rootfs tarballs provided by Canonical for Ubuntu operating system.
  * `nginx` is the official image containing Nginx web server.
  * `httpd` is the official image containing the Apache web server.


## Running Containers

Running a container from an image:
```console
$docker run <image>
```
```console
$docker run hello-world

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

`docker run` is a shortcut for a number of activities

* Look for the image in the list of images
  installed on the host computer.
* If the image is not locally installed, then
  look for the image in the docker hub.
* Download and install the image (all its layers) 
  from docker hub.
* Create a new container from the image.
* Start the container.
* If the main command in the image is 
  a short lived one, then the container will
  stop execution as soon as the command is finished.



List of currently running containers:
```console
$docker ps
```


List of running and stopped containers:
```console
$docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                     PORTS               NAMES
e4c931fa03a8        busybox             "sh"                     6 minutes ago       Exited (0) 6 minutes ago                       competent_brahmagupta
93443e9a8c68        busybox             "sh"                     7 minutes ago       Exited (0) 7 minutes ago                       beautiful_keldysh
```

Running a container with a specific name
```console
$docker run --name <name> <image>
```
```console
$docker run --name busybee busybox
```
Note that once you create a container with a name,
you cannot create another container with the same name
till the original container has been removed.

Running a container and associate a terminal to it
```console
$docker run -it <image> 
```

* `-i` or `--interactive` means keeping STDIN open 
* `-t` or `--tty` means to allocate a pseudo terminal

```console
$docker run -it busybox echo 'shailesh'
shailesh
```

* We ran a container using the `busybox` image.
* The `busybox` image runs the Linux shell as its main command.
* We provided input to the shell running inside the container from the command-line itself `echo 'shailesh'`
* We allocated a pseudo terminal to the container
* The shell running inside the container executed the `echo 'shailesh'` command.
* Its output showed up onscreen.

Setting a working directory:

```console
$docker run -w <dir> -it <image>
```
Note that we are setting the working directory from within the file system of the container. 
A running container doesn't have direct access to the filesystem of the host computer.


A common use case is running a container as an interactive shell
and removing the container immediately after it is stopped
(i.e. as soon as we exit the shell). Let's try that with `busybox`:
```console
$docker run -it --rm busybox
/ # ls
bin   dev   etc   home  proc  root  sys   tmp   usr   var
/ # pwd
/
/ # echo 'shailesh'
shailesh
/ #
```
Note the `--rm` command-line switch. It ensures that the container
will be removed immediately after it is stopped.
The `busybox` shell shows its own prompt `/ #` during execution.
We finish execution by pressing `CTRL+D`. If we check `docker ps`
now, we won't see this container.


Running the Nginx web server in a container:
```console
docker run --detach --name web nginx:latest
Unable to find image 'nginx:latest' locally
latest: Pulling from library/nginx
a2abf6c4d29d: Pull complete
a9edb18cadd1: Pull complete
589b7251471a: Pull complete
186b1aaa4aa6: Pull complete
b4df32aa5a72: Pull complete
a0bcbecc962e: Pull complete
Digest: sha256:0d17b565c37bcbd895e9d92315a05c1c3c9a29f762b011a10c54a66cd53c9b31
Status: Downloaded newer image for nginx:latest
2cf811c887e154a7a91e16e3ad8c688ab535f345c51002761f433983af3f9ac1
```

* The `nginx` image was not available locally. 
* It was downloaded from docker hub.
* Once the image was downloaded, a container using this image was started.
* The last line shows the long container id assigned to this container `2cf811c887e154a7a91e16e3ad8c688ab535f345c51002761f433983af3f9ac1`.
* The container is going to be run in detached mode as it contains a service which doesn't require any terminal input/output. 

One can see the container in the list of running containers:
```console
$docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
2cf811c887e1        nginx:latest        "/docker-entrypoint.…"   2 minutes ago       Up 2 minutes        80/tcp              web
```
The process listing of this container shows the last 12 characters of the container id.

The web server runs on the default port 80 inside the container.
However, we haven't associated it with a port of the host machine yet. 
Let's remove this container.
```console
$docker stop web
$docker rm web
```

This time, we shall create the Nginx container by associating the container port 80 with the host port 8080.
```console
$docker run --detach --name web -p 8080:80 nginx:latest
de60c053aa91f33c792883833639ccbdfedb708f47bd06bc8a3c8eedaa347e7d```
```

We can examine the port mapping:
```console
$docker port <container>
```
```console
$docker port web
80/tcp -> 0.0.0.0:8080
```

Let's check if we can access the web-server running inside the container:
```console
$ wget -O - http://localhost:8080
--2022-01-18 19:51:07--  http://localhost:8080/
Resolving localhost (localhost)... 127.0.0.1
Connecting to localhost (localhost)|127.0.0.1|:8080... connected.
HTTP request sent, awaiting response... 200 OK
Length: 615 [text/html]
Saving to: ‘STDOUT’

-                                                             0%[                                                                                                                                         ]       0  --.-KB/s               <!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
-                                                           100%[========================================================================================================================================>]     615  --.-KB/s    in 0s

2022-01-18 19:51:07 (48.3 MB/s) - written to stdout [615/615]
```

### Inspecting a running container

Recall the `nginx` container named `web` we created above. 

Finding the IP address of a running container:
```console
$docker inspect --format='{{ .NetworkSettings.IPAddress }}' <container>
```
```console
$docker inspect --format='{{ .NetworkSettings.IPAddress }}' web
172.17.0.2
```

Associating a temporary file system 
to a docker container:
```console
$docker run -d --tmpfs  /run:rw,noexec,nosuid,size=65536k <image>
```
* `-d` means running the container in the background
  (detached from terminal) and printing container ID

Details of `--tmpfs`
* An empty temporary file system has been attached.
* Read/Write permissions
* No execution permission
* No Set UID permission
* 64MB maximum size

### More life-cycle commands

Creating a container without starting it:

```console
$docker create <image>
```

Starting a container:
```console
$docker start <container>
```

Stopping a container:
```console
$docker stop <container>
```

Restarting a container:
```console
$docker restart <container>
```

Forcefully killing a container:
```console
$docker kill <container>
```

Removing a container:
```console
$docker rm <container>
```

Identifying container ids which have exited:
```console
$docker ps --filter status=exited -q
7da1661fbba6
```

Removing all stopped containers:
```console
$docker rm $(docker ps --filter status=exited -q)
7da1661fbba6
```
It emits the ids of the containers which get removed.

Another way to remove all stopped containers is by using the `xargs` utility of Linux:
```console
$docker ps --filter status=exited -q | xargs docker rm
```

## File System


## Running Commands inside Container


Running the `ls` command inside a container:
```console
$docker exec <container> ls
```

Running an interactive bash terminal inside a container:
```console
$docker exec -it <container> /bin/bash
```

## Network Ports

## Images

Showing the list of images available on the host machine:
```console
$docker images
REPOSITORY                TAG                 IMAGE ID            CREATED             SIZE
busybox                   latest              beae173ccac6        2 weeks ago         1.24MB
nginx                     latest              605c77e624dd        2 weeks ago         141MB
openjournals/paperdraft   latest              993023e4659f        3 months ago        691MB
hello-world               latest              feb5d9fea6a5        3 months ago        13.3kB
```

#### Importing Images

Pulling/Downloading an image of 
Apache HTTP Server from `Docker Hub`:
```console
$docker pull httpd
```

Command for pulling an arbitrary image:
```console
$docker pull <image>
```

#### Creating Images from a Container

Assume that a container is running and you wish
to save an image based on its current state:
```console
$docker commit <container> <image_name>
```

#### Removing Images

Removing an image:
```console
$docker rmi <image>
```


## Building Images from Dockerfiles

A Dockerfile is a set of instructions to build an image.
It is written as a simple text file.
A docker image can be created using the `docker build` command
on a docker file.
The main instructions given in a Dockerfile are:
`FROM`, `LABEL`, `COPY`, `ADD`, `RUN`, `ENV`, `EXPOSE`, `CMD`, `ENTRYPOINT`, `WORKDIR`, `ARGS`, `VOLUME`.

#### A first docker image

We will build a simple image

* We start with the image for Alpine Linux: `alpine:latest`.
* We make sure that the package repository is updated in the image using the `apk` tool.
* We add `vim` editor to the image using the `apk` tool.


Here is the Dockerfile
```dockerfile
FROM alpine:latest

RUN apk update
RUN apk add vim
```

We put this into a file named `Dockerfile` and save it. 
Let us now build an image using this file. We shall name our new image as `shailesh1729/vim`.
```console
$docker build -t shailesh1729/vim  .
Sending build context to Docker daemon  2.048kB
Step 1/3 : FROM alpine:latest
latest: Pulling from library/alpine
59bf1c3509f3: Pull complete
Digest: sha256:21a3deaa0d32a8057914f36584b5288d2e5ecc984380bc0118285c70fa8c9300
Status: Downloaded newer image for alpine:latest
 ---> c059bfaa849c
Step 2/3 : RUN apk update
 ---> Running in ed1db3549672
fetch https://dl-cdn.alpinelinux.org/alpine/v3.15/main/x86_64/APKINDEX.tar.gz
fetch https://dl-cdn.alpinelinux.org/alpine/v3.15/community/x86_64/APKINDEX.tar.gz
v3.15.0-206-ge1064619f3 [https://dl-cdn.alpinelinux.org/alpine/v3.15/main]
v3.15.0-209-g6701dcf4a3 [https://dl-cdn.alpinelinux.org/alpine/v3.15/community]
OK: 15848 distinct packages available
Removing intermediate container ed1db3549672
 ---> ee4deb59186e
Step 3/3 : RUN apk add vim
 ---> Running in b6be0c3b0096
(1/5) Installing xxd (8.2.3650-r0)
(2/5) Installing lua5.3-libs (5.3.6-r1)
(3/5) Installing ncurses-terminfo-base (6.3_p20211120-r0)
(4/5) Installing ncurses-libs (6.3_p20211120-r0)
(5/5) Installing vim (8.2.3650-r0)
Executing busybox-1.34.1-r3.trigger
OK: 34 MiB in 19 packages
Removing intermediate container b6be0c3b0096
 ---> c90dcbb67a7a
Successfully built c90dcbb67a7a
Successfully tagged shailesh1729/vim:latest
```

Once, the building process is successfully completed, we can see the new pristine image
in the list of images:

```console
$ docker images
REPOSITORY                TAG                 IMAGE ID            CREATED             SIZE
shailesh1729/vim          latest              c90dcbb67a7a        2 minutes ago       33.7MB
busybox                   latest              beae173ccac6        2 weeks ago         1.24MB
nginx                     latest              605c77e624dd        2 weeks ago         141MB
alpine                    latest              c059bfaa849c        7 weeks ago         5.59MB
hello-world               latest              feb5d9fea6a5        3 months ago        13.3kB
```

If we run this image, we can see that we can use `vim` inside it:
```console
$docker run -it --rm  shailesh1729/vim
/ # vim
/ # abc
/bin/sh: abc: not found
/ #
```




## Docker Hub

Logging in:
```console
$docker login
```


Pushing an image to docker hub

```console
$docker push <repository>/<image_name>
```




