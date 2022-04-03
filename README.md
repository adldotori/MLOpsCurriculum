# MLOpsCurriculum

I’m an MLOps Engineer at Corca.

## Usage

In local environment

```
$ pip install -r requirements.txt
$ export FLASK_APP=api/app.py; flask run
```

In docker container

```
$ docker-compose up
```

## Deploy to ECS

```
$ docker context create ecs mlopscurriculum
$ docker context use mlopscurriculum
$ docker compose -f docker-compose.ecs.yml up
```

You can view services create for the Compose appliciation on Amazon ECS and their state using the `docker compose ps` command.

## API

0. Health Check - `GET /`
1. Get All Users - `GET /users`
2. Get User - `GET /users/<id:int>`
3. Create User - `POST /users`
4. Update User - `PUT /users/<id:int>`
5. Delete User - `DELETE /users/<id:int>`

---

## Phase1.

- EC2 endpoint: http://3.37.129.150:5000/
- ECS endpoint: http://3.34.201.203:5000/

### Summary

> **이름, 나이 정보를 갖는 사용자를 Create, Read, Update, Delete 할 수 있는 API 서버 개발 및 배포**

- MVC패턴을 이용한 CRUD API 개발
- ORM을 활용하여 controller와 DB 연결
- API 서버 dockerize
- EC2, ECS 로 배포

### Review

- SRP, OCP 고려 여부는 프로젝트 크기에 따라 결정할 것
- 항상 비효율적인 부분을 개선하려 노력할 것
- 디버깅할 때 근본적인 이유를 찾을 것
- 디자인 패턴, 코드 퀄리티는 몸에 익숙해질 때까지 항상 신경쓰자

### Feedback

- 처음이다 보니 중간에 커리큘럼이 조금씩 바꼈다. 다음 번에는 좀 더 안정적인 운영을 할 수 있도록 해야겠다.
