# FastAPI + SQLAlchemy 2.0 튜토리얼
FastAPI로 구현한 API에 SQLAlchemy 2.0 버전을 사용하기 위해 필요한 과정을 설명하는 튜토리얼

# 사용 기술
- FastAPI, SQLAlchemy2.0, MariaDB, Docker

# 튜토리얼 설명 (블로그 원고 작업중)
SQLAlchemy는 Python ORM 라이브러리 중 가장 널리 쓰이는 라이브러리 중 하나로, 2.0 버전이 업데이트 되면서 사용 방식이 이전 버전과 많이 달라졌다. 하지만 FastAPI 공식 튜토리얼에서는 아직 1.0 버전을 다루고 있어, FastAPI와 SQLAlchemy 2.0 버전을 같이 사용하는 튜토리얼을 만들어 보기로 했다.

## 다루는 내용
- 이미 스키마 정의가 끝난 MySQL 데이터베이스와 FastAPI를 사용한 RestAPI 구현 방법

## 다루지 않는 내용
- API 보안
- MariaDB, Docker 관련 설명 (Dockerfile, docker-compose.yaml, SQL 스크립트는 제공함)
- Alembic 라이브러리를 사용한 동적 데이터베이스 동기화 (데이터베이스 스키마는 변하지 않는다고 가정)

# 사용 스키마

![SQLAlchemy ERD](https://github.com/jsh318900/fastapi_sqlalchemy_2_tutorial/assets/22267053/ab2a6dfb-d6ab-4d40-822b-44ceda1d3d5a)

# 주요 파일들
- [Dockerfile](./Dockerfile): FastAPI 어플리케이션 도커 이미지 생성 스크립트
- [docker-compose.yaml](./docker-compose.yaml): FastAPI와 MariaDB 서비스를 같이 실행하기 위한 docker compose 스크립트
- [db_init.sql](./sql/db_init.sql): 실습에 사용한 데이터베이스 생성 스크립트

# 실행 방법

**최신버전 도커가 이미 설치되어 있고 docker daemon이 실행 중이라고 가정**
```
# 소스코드 다운로드
git clone git@github.com/jsh318900/fastapi_sqlalchemy_2_tutorial
cd fastapi_sqlalchemy_2_tutorial
# docker image 생성
docker build -t tutorial .
# 데이터베이스용 docker volume 생성
docker volume create database_volume
# 데이터베이스, API 실행
docker compose up -d
```
실행된 API는 [http://localhost:8080/docs](http://localhost:8080/docs)에서 확인 및 테스트할 수 있다.
