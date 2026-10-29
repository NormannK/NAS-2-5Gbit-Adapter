# DS220j / DSM 7.4 container build (experimental)

Adapted from [chadlwilson's RTD1296 build container](https://github.com/chadlwilson/syno-driver-realtek-r8152/commit/b60f0a733747faba37ba78a0be1e6c6e680d58d1).
This tooling uses the official Synology cross-build environment. It does not
import that fork's driver or compatibility header, which are behind our source.

Status: shell syntax and CLI options reviewed; Docker image, SDK download,
SPK build and NAS installation have NOT been tested. Do not treat an artifact
from this draft as a validated release.

## Build on a development computer

Use an amd64 Linux Docker host with sufficient free space for a multi-GB SDK.
Do not run the build on the DS220j's 512 MB RAM. An ARM host needs working
amd64 emulation; that configuration is untested here.

From the repository root containing the changes you want to build:

```sh
docker build --platform linux/amd64 -t ds220j-r8152-build tools/ds220j-build
mkdir -p build
docker run --rm --privileged --platform linux/amd64 \
  --mount "type=bind,src=$PWD,dst=/input,readonly" \
  --mount "type=bind,src=$PWD/build,dst=/out" \
  ds220j-r8152-build
```

The container needs elevated access to mount/chroot for Synology's toolkit.
Use a trusted checkout on a development host. Source is mounted read-only and
copied inside the container. Toolkit, copy and chroot share a filesystem so
the toolkit's hard links work. The script deploys at runtime and fails on
deployment errors; it does not suppress them as the source fork's Dockerfile did.

Target is deliberately fixed to RTD1296 / DSM 7.4. Toolkit scripts are pinned to
`b26769cbd5f7564e5bc5e4b5e494760292025c44`. Base-image packages and SDK downloads
are not content-pinned, so this is not a claim of bit-for-bit reproducibility.
Each fresh container downloads/deploys its SDK; caching is deferred.

Output appears in a unique `build/ds220j.XXXXXX/` directory with a build log,
source checksums, toolkit revision, target metadata, and SPK checksums.
The source manifest identifies the actual copied inputs, including local edits.
The selected checkout determines which PR changes are built: this build-tool
branch alone does not contain the diagnostics or linear-TX experiment.

## Before installing

Inspect the non-debug SPK's INFO and packaged module. Confirm `arch=rtd1296`
and module vermagic matches the running NAS kernel; DSM 7.4 toolkit selection
alone does not guarantee compatibility with every DSM patch.
Retain the original matching upstream SPK and management access through built-in LAN.
No package is installed, published or uploaded automatically by this tooling.

An SPK build is not a demonstration that issue #275 is fixed. Run sustained TCP
and SMB transfers in both directions and verify checksums before relying on it.
