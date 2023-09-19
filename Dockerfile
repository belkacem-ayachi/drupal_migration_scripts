FROM php:8.1-apache-bullseye
# Copy the Code folder to the container
COPY ./ /var/www/html/<PROJECT-NAME>/
COPY ./apache-config/ /etc/apache2/sites-available/
RUN ln -s /etc/apache2/sites-available/<PROJECT-NAME>.conf /etc/apache2/sites-enabled/
EXPOSE 80
EXPOSE 443


# Debian Buster configuration
RUN apt update -y --fix-missing
RUN apt upgrade -y
RUN apt install -y apt-utils nano wget dialog software-properties-common build-essential git curl openssl

# PHP Module: zip
RUN apt install -y libzip-dev unzip
RUN docker-php-ext-install zip

# PHP Module: intl
RUN apt install -y libicu-dev
RUN docker-php-ext-install -j$(nproc) intl

# PHP Module: gd
RUN apt install -y libfreetype6-dev libjpeg62-turbo-dev libpng-dev
RUN docker-php-ext-install -j$(nproc) gd

# PHP Module: bcmath
RUN docker-php-ext-install bcmath

# PHP Module: imap
RUN apt install -y libc-client-dev libkrb5-dev
RUN docker-php-ext-configure imap --with-kerberos --with-imap-ssl
RUN docker-php-ext-install imap

# PHP Module: opcache
RUN docker-php-ext-enable opcache

# # PHP Module: redis
# RUN apt install -y redis-tools
# RUN pecl install redis-5.3.7
# RUN docker-php-ext-enable redis

# Enable apache modules
RUN a2enmod rewrite headers

# Composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer