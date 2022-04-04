# Performance Test

|                | 최대 동시 접속자 수 | 응답시간 측정     | 단위시간당 최대 처리량 |
| -------------- | ------------------- | ----------------- | ---------------------- |
| EC2 - db read  | 80                  | 100명 기준 240ms  | 425개                  |
| EC2 - db write | 10                  | 10명 기준 900ms   | 10개                   |
| ECS - db read  | 100                 | 100명 기준 1000ms | 150개                  |
| ECS - db write | 1                   | 10명 기준 1000ms  | 20개                   |

## 1. EC2 (DB-READ) Performance

![](ec2-read.png)

- 80명까지는 큰 무리없이 전부 처리 가능
- 80명 시점부터 spiking 현상이 일어남. DB에 read operation이 너무 쌓여 병목 발생.
- 100명 기준 평균적으로 240ms 안에 응답 돌아옴.

## 2. EC2 (DB-WRITE) Performance

![](ec2-write.png)

- 3명부터 바로 failure 발생
- 3명부터 response time이 급격히 증가하며 10명 기준 거의 1초에 가까운 시간이 걸림.
- 단위시간당 처리량은 read에 비해 압도적으로 적음.

## 3. ECS (DB-READ) Performance

![](ecs-read.png)

- RPS를 봤을 때 성능 자체는 EC2보다 좋지 않으나 spiking현상은 일어나지 않음
- 단위시간당 최대 처리량도 EC2과 비교하여 현저하게 적음

## 4. ECS (DB-WRITE) Performance

![](ecs-write.png)

- 1명이 넘어가면 제대로 쓰지 못하고 SRT가 폭등함
- ECS가 EC2보다 안 좋은 이유: FARGATE 기본이 0.25vCPU, 메모리 0.5GB 이므로 1vCPU, 메모리 1GB인 EC2보다 현저하게 성능이 낮다.
