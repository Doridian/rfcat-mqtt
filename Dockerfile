FROM alpine

RUN apk --no-cache add python3 py3-yaml py3-pip py3-numpy py3-usb py3-paho-mqtt libusb libusb-compat && pip3 install rfcat

COPY . /app

WORKDIR /app
USER daemon:daemon

ENTRYPOINT [ "/app/__init__.py" ]
