FROM continuumio/miniconda3

# Set the ENTRYPOINT to use bash
# (this is also where you’d set SHELL,
# if your version of docker supports this)
ENTRYPOINT [ "/bin/bash”, “-c” ]

EXPOSE 5000

# Conda supports delegating to pip to install dependencies
# that aren’t available in anaconda or need to be compiled
# for other reasons. In our case, we need psycopg compiled
# with SSL support. These commands install prereqs necessary
# to build psycopg.
RUN apt-get update && apt-get install -y \
 libpq-dev \
 build-essential \
&& rm -rf /var/lib/apt/lists/*


RUN mkdir /app


ADD environment.yml /tmp/environment.yml
WORKDIR /tmp
RUN ["conda","env","create", "--file", "environment.yml"]

WORKDIR /app
COPY . /app

# We set ENTRYPOINT, so while we still use exec mode, we don’t
# explicitly call /bin/bash
CMD ["source activate nexradaws"]
