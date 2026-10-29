# Adapted from chadlwilson/syno-driver-realtek-r8152
# b60f0a733747faba37ba78a0be1e6c6e680d58d1 (GPL-2.0).
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates git curl wget python3 python3-pkg-resources cpio bc \
    xz-utils tar file rsync kmod build-essential \
    && rm -rf /var/lib/apt/lists/*
# Pin the reviewed DSM7.4 toolkit source, not a moving default branch.
RUN mkdir -p /toolkit/pkgscripts-ng /toolkit/source /toolkit/result_spk \
    && git -C /toolkit/pkgscripts-ng init \
    && git -C /toolkit/pkgscripts-ng remote add origin https://github.com/SynologyOpenSource/pkgscripts-ng.git \
    && git -C /toolkit/pkgscripts-ng fetch --depth 1 origin b26769cbd5f7564e5bc5e4b5e494760292025c44 \
    && git -C /toolkit/pkgscripts-ng checkout --detach FETCH_HEAD
COPY build-package.sh /usr/local/bin/build-ds220j
RUN chmod 0755 /usr/local/bin/build-ds220j
WORKDIR /toolkit/pkgscripts-ng
ENTRYPOINT ["/usr/local/bin/build-ds220j"]
