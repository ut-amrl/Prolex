# syntax=docker/dockerfile:1
FROM php:8.2.8
RUN docker-php-ext-install opcache

# Remove depricated warnings -- messes with XML schema learning parsing
RUN echo 'display_errors = Off' > /usr/local/etc/php/conf.d/error-logging.ini

# Copy Directory
COPY . .

#####################
FROM racket/racket:8.7-full
COPY --from=0 . .
FROM nvidia/cuda:12.0.0-base-ubuntu20.04
COPY --from=1 . .
####################

# Update and get miniconda
RUN apt-get update \
	&& apt-get install -y wget \
	&& wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# Install Miniconda
ENV PATH="/root/miniconda3/bin:$PATH"
RUN mkdir /root/.conda && bash Miniconda3-latest-Linux-x86_64.sh -b

# Init Conda
RUN conda init bash

# Make conda and php setup run automatically upon entry
RUN echo "source setup.sh" >> ~/.bashrc

# Extra Docker setup
COPY docker_entrypoint.sh /docker_entrypoint.sh
ENTRYPOINT [ "/docker_entrypoint.sh" ]
