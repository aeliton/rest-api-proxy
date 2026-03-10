FROM alpine:latest

WORKDIR /test

RUN apk add --no-cache shunit2 curl netcat-openbsd

COPY test_cipher_e2e.sh .

CMD ["/bin/sh", "test_cipher_e2e.sh"]
