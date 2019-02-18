RUN apt-get -y update && \
    apt-get install --no-install-recommends -y \
        build-essential \
        ca-certificates \
        checkinstall \
        libbz2-dev \
        libc6-dev \
        libffi-dev \
        libgdbm-dev \
        libncursesw5-dev \
        libreadline-gplv2-dev \
        libsqlite3-dev \
        libssl-dev \
        tk-dev \
        uuid-dev \
        wget && \
    rm -rf /var/lib/apt/lists/*

# Based loosely on https://github.com/rust-lang/docker-rust
# With sccache configured to output dep artifacts to a cacheable directory

ENV RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    PATH=/usr/local/cargo/bin:$PATH \
    SCCACHE_DIR=/opt/sccache

RUN set -ex \
    && wget https://static.rust-lang.org/rustup/archive/1.16.0/x86_64-unknown-linux-gnu/rustup-init \
    && chmod +x rustup-init \
    && ./rustup-init -y --no-modify-path \
    && rm rustup-init \
    && chmod -R a+w $RUSTUP_HOME $CARGO_HOME \
    && rustup --version \
    && cargo --version \
    && rustc --version \
    && cargo install --vers 0.2.8 --root /usr/local --no-default-features sccache \
    && mkdir -p $SCCACHE_DIR \
    && rm -rf /usr/local/cargo/registry

# Using sccache to force build artifacts to use a cacheable directory
# Mounting volume for /opt/sccache will allow reusing previously build dependencies
# Mounting volume for /usr/local/cargo/registry will speed up dependency resolution
ENV RUSTC_WRAPPER=/usr/local/bin/sccache
VOLUME ["/usr/local/cargo/registry", "/opt/sccache"]

