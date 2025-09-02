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

## Useful SQL query examples

The following query will return a table containing the highest Mantid version used for each Mantid algorithm:

```sql
WITH max_versions AS (
SELECT name, MAX(CAST(SUBSTRING("mantidVersion",1,1) AS INT)) AS major
FROM "services_featureusage"
WHERE "type" = 'Algorithm' AND "mantidVersion" != ''
GROUP BY "name"
)
SELECT services_featureusage.name, MAX(CAST(SUBSTRING("mantidVersion",1,1) AS INT)) AS major, MAX(CAST(SUBSTRING("mantidVersion",3) AS INT)) AS minor
FROM services_featureusage
JOIN max_versions ON
services_featureusage.name = max_versions.name AND CAST(SUBSTRING(services_featureusage."mantidVersion",1,1) AS INT) = max_versions.major
WHERE services_featureusage."mantidVersion" != ''
GROUP BY services_featureusage.name
```

To show a summary of the system architecture for MacOS users in 6.13.* (our first release of the Arm packages), use:

```sql
SELECT "osArch", COUNT(*) AS total
FROM "services_usage"
WHERE "mantidVersion" LIKE '6.13._' AND "osName" = 'Darwin'
GROUP BY "osArch"
ORDER BY total DESC;
```sql
