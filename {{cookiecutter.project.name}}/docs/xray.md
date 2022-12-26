# X-Ray




## Running the X-Ray daemon in a Docker container

Build the container image with `docker build xray/.`

```$ docker build -t xray-daemon xray/.```


Run the image in a container with docker run

```commandline
$ docker run \
      --attach STDOUT \
      -v ~/.aws/:/root/.aws/:ro \
      --net=host \
      -e AWS_REGION=us-east-1 \
      --name xray-daemon \
      -p 2000:2000/udp \
      xray-daemon -o
```

This command uses the following options:

- `--attach STDOUT` – View output from the daemon in the terminal.
- `-v ~/.aws/:/root/.aws/:ro` – Give the container read-only access to the .aws directory to let it read your AWS SDK credentials.
- `AWS_REGION=us-east-1` – Set the AWS_REGION environment variable to tell the daemon which region to use.
- `--net=host` – Attach the container to the host network. Containers on the host network can communicate with each other without publishing ports.
- `-p 2000:2000/udp` – Map UDP port 2000 on your machine to the same port on the container. This is not required for containers on the same network to communicate, but it does let you send segments to the daemon from the command line or from an application not running in Docker.
- `--name xray-daemon` – Name the container xray-daemon instead of generating a random name.
- `-o` (after the image name) – Append the -o option to the entry point that runs the daemon within the container. This option tells the daemon to run in local mode to prevent it from trying to read Amazon EC2 instance metadata.

To stop the daemon, use `docker stop`. If you make changes to the `Dockerfile` and build a new image, you need to delete the existing container before you can create another one with the same name. Use `docker rm` to delete the container.

`$ docker stop xray-daemon`

`$ docker rm xray-daemon`