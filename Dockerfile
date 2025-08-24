# 베이스: AWS Lambda Python 3.12
FROM public.ecr.aws/lambda/python:3.12

# 작업 디렉토리
WORKDIR /var/task

# 의존성 설치
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 소스 복사
COPY . .

# Lambda 핸들러 지정: 모듈.파일.함수
# aws/lambda_handler.py 안의 lambda_handler()를 실행
CMD ["aws.lambda_handler.lambda_handler"]
