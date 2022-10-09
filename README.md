# TP GRPC

**Author**: Sebastian Romero <sebastian.romero@imt-atlantique.net>

This repository has a folder for each microservice:

* `/booking`
* `/movie`
* `/showtime`
* `/user`

In the `docker-compose.yml` file you can see the information about the services and their exposed ports.

## What was made of the TP?

In this repository from commits you can clearly see the progress of the TP:

* Commit [docker-compose.yml](https://github.com/sebasro10/TP_GRPC/commit/00d8fbd06aea4e0264f014c85c214103c3349421) : Container names are added to perform the request using these
* Commit [tutorial gRPC](https://github.com/sebasro10/TP_GRPC/commit/f7e42e0981bd1590d1d763084d1a137b370d2f2d)
* Commit [TP vert -> 1](https://github.com/sebasro10/TP_GRPC/commit/be0e0f670fd107df9db0f620adf6e4421e3ba7b7)
* Commit [code of TP_REST for user and booking services](https://github.com/sebasro10/TP_GRPC/commit/b32a821ef2c7770802747393fb29e4fc2dc2e9d5)
* Commit [TP vert -> 2](https://github.com/sebasro10/TP_GRPC/commit/cdddccd7cf5e3925bd4cac7d3eb2b61223922d01)
* Commit [TP vert -> 3](https://github.com/sebasro10/TP_GRPC/commit/a4bc29d228e5a4081b125e47dcfd6175b1d30580)
* Commit [TP vert -> 4](https://github.com/sebasro10/TP_GRPC/commit/f8fd31ade10b5951d9385d40d96df870d715d59b)
* Commit [TP vert -> 5](https://github.com/sebasro10/TP_GRPC/commit/73ed1af4087811409f4d4af7392a2553bff0961b)
* Commit [TP bleu](https://github.com/sebasro10/TP_GRPC/commit/35be9d2f2bb41fd440a4996a196b446f954af6f2)

## Tests GRPC

To test the `movie` and  `showtime` services you can execute (on different terminals):

```bash
cd movie
python movie.py
```

```bash
cd showtime
python showtime.py
```

```bash
cd client
python client.py
```

## Run project

Build or rebuild services
```bash
docker-compose build
```

Create and start containers
```bash
docker-compose up
```

Stop and remove containers, networks
```bash
docker-compose down
```

## Tests from Postman

And you can test the `user` service from Postman by following the steps below:

* In Postman click on "Import" -> "Upload Files"
* Select the file with the contract (`user/UE-archi-distribuees-User-1.0.0-resolved.yaml`)
* Select the option "Generate collection from imported APIs" and in "Link this collection as" select "Test suite"
* Click on "Import"

Now, a collection has been created and you can test the methods.
