# Usage Reports Server

This repository holds the configuration for setting up a Django-based server to
capture usage reports sent by [Mantid](https://github.com/mantidproject/mantid).

## Mantid Configuration

### Production

The production server runs at <https://reports.mantidproject.org> and
Mantid is configured by default to send to this server.

### Development

While developing this server Mantid can be configured to send to the instance
started locally by editing `mantid_build_dir/bin/Mantid.properties` and changing

```sh
usagereports.enabled = 1
usagereports.rooturl = http://localhost:8082
```

This will require a restart of Mantid.
Note that the port number depends on the value specified by `HOST_PORT`
specified in the environment file but defaults to the above value.
See [DevelopmentSetup](DevelopmentSetup.md#creating-an-environment-env-file)
for how to setup and environment file.

## Getting Started

To get started for development please follow the instructions in [DevelopmentSetup](DevelopmentSetup.md).
