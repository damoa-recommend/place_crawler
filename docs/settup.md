* 디비

```sh
$ docker run -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=password --name place_mysql mysql:5.7
```

```sh
$ docker start place_mysql
```

```sh
$ docker exec -it place_mysql /bin/bash
```

```sh
$ mysql -u root -p
```