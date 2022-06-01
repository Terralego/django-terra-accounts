FROM makinacorpus/geodjango:bionic-3.6

RUN apt-get update -qq && apt-get install -y -qq\
    # python basic libs
    python3.8 python3.8-dev python3.8-venv python3-distutils &&\
    apt-get clean all && rm -rf /var/apt/lists/* && rm -rf /var/cache/apt/*

# Install python3.10 on bionic \o/
RUN wget https://www.python.org/ftp/python/3.10.3/Python-3.10.3.tgz
RUN tar -xf Python-3.10.*.tgz
RUN cd Python-3.10.*/ && ./configure --enable-optimizations
RUN cd Python-3.10.*/ && make -j $(nproc)
RUN cd Python-3.10.*/ && make altinstall

RUN mkdir -p /code/src

RUN useradd -ms /bin/bash django
RUN chown -R django:django /code

# USER django

RUN python3.6 -m venv /code/venv
RUN  /code/venv/bin/pip install --no-cache-dir pip setuptools wheel -U

COPY . /code/src
WORKDIR /code/src

# Install dev requirements
RUN /code/venv/bin/pip3 install --no-cache-dir -e .[dev] -U
RUN . /code/venv/bin/activate
