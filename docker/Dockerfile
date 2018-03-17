# Use the official Docker Hub python:3.6.3-alpine base image
FROM python:3.6.3-alpine

ENV LANG=en_US.UTF-8

# Add aliyun mirror to acclerate download speed
RUN set -e && \
	sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories && \
        apk update && \
	    apk add --no-cache --virtual .build-deps \
		    gcc \
		    libc-dev \
		    linux-headers \
		    musl-dev \
		    openssl-dev \
		    libffi-dev\
		    build-base\
		&& \
		apk add --no-cache \
		    tzdata \
            pcre \
            pcre-dev \
            libuuid \
            postgresql-dev \
            libxml2-dev \
            libxslt-dev \
            curl \
            openssl \
        && \
	    cp -r -f /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

# Use Pip install Sketch
ADD . /tmp/sketch
RUN pip install /tmp/sketch --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple

# Copy the App configuration file into /etc
RUN cp /usr/local/share/sketch/sketch.conf /etc


# Clean tmp file to reduce image size
RUN apk del .build-deps && \
    rm -rf /tmp/*

# Copy the entrypoint script into the container
COPY docker/docker-entrypoint.sh /
COPY docker/uwsgi.ini /
RUN chmod a+x /docker-entrypoint.sh

# Expose the port used by Sketch
EXPOSE 8001

# Create Log Folder
RUN mkdir -p /logs

# Load the entrypoint script to be run later
ENTRYPOINT ["/docker-entrypoint.sh"]

# Invoke the entrypoint script
CMD ["sketch"]

