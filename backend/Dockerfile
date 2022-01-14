FROM python:3.9-alpine as base

FROM base as builder

RUN sed -i 's/http\:\/\/dl-cdn.alpinelinux.org/https\:\/\/alpine.global.ssl.fastly.net/g' /etc/apk/repositories

RUN apk add --no-cache \
    ca-certificates && \
    update-ca-certificates 

# COPY ca/* /usr/local/share/ca-certificates/

RUN apk update && \
	apk upgrade --available && \
	apk add --no-cache \
	openssl \
	curl \
	gcc \
	make \
	build-base \
	libffi-dev \
	libpq-dev \
	python3-dev

ENV PATH="/home/admin/.local/bin:${PATH}"

RUN adduser -D -s /bin/bash -g '' -h /home/admin admin

USER admin

WORKDIR /home/admin

RUN python -m pip install --upgrade pip

RUN python -m pip install --user --upgrade \
	cffi \
	setuptools

COPY --chown=admin:admin requirements.txt requirements.txt

RUN pip install --user --upgrade --no-cache-dir -r requirements.txt

ENV PATH="/home/admin/.local/bin:${PATH}"

FROM base

RUN adduser -D -s /bin/bash -g '' -h /home/admin admin

USER admin

WORKDIR /home/admin

COPY --from=builder /home/admin /home/admin/

# COPY ./src /home/admin/src
# COPY ./app.py /home/admin/
# COPY ./.env /home/admin/
# COPY ./favicon.ico /home/admin/
# COPY ./yoga /home/admin/yoga
COPY . .

ENV PATH="/home/admin/.local/bin:${PATH}"

EXPOSE 8080

CMD ["uvicorn", "app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080", "--workers", "2", "--reload"]
