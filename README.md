# Bitbucket Pipelines Pipe: bitbucket-pipe

Custom pipe to run SCA and SAST security scans

## YAML Definition

Add the following snippet to the script section of your `bitbucket-pipelines.yml` file:

```yaml
script:
  - pipe: docker://j1209/bitbucket-pipe:1.0.0          
    variables:
      PRODUCT: 'blackduck' # mandatory
      BLACKDUCK_URL: $url
      BLACKDUCK_TOKEN: $token
      BITBUCKET_APP_PASSWORD: $BITBUCKET_APP_PASSWORD # mandatory for SARIF/diagnostics upload
      BITBUCKET_USERNAME: $username # mandatory for SARIF/diagnostics upload
      # DEBUG: "<boolean>" # Optional
```
## Variables

| Variable | Usage                                              |
|----------|----------------------------------------------------|
| PRODUCT (1) | The specified scan you want to run          |
| BLACKDUCK_URL (2) | The Blackduck Hub URL          |
| BLACKDUCK_TOKEN (2) | The token to establish connection with the Blackduck Hub          |
| BITBUCKET_APP_PASSWORD (3) | Bitbucket App password with repository write access          |
| BITBUCKET_USERNAME (3) | Bitbucket user name with which you push commit          |
| DEBUG    | Turn on extra debug information. Default: `false`. |

_(1) = required variable in all cases._

_(2) = required variable for Blackduck scan._

_(3) = required variable for SARIF/diagnostics upload_

## Prerequisites

## Examples

Basic example:

```yaml
script:
  - pipe: docker://j1209/bitbucket-pipe:1.0.0          
    variables:
      PRODUCT: 'blackduck'
      BLACKDUCK_URL: $url
      BLACKDUCK_TOKEN: $token
```

Advanced example (for SARIF and diagnostics upload):

```yaml
script:
  - pipe: docker://j1209/bitbucket-pipe:1.0.0          
    variables:
      PRODUCT: 'blackduck'
      BLACKDUCK_URL: $url
      BLACKDUCK_TOKEN: $token
      BITBUCKET_APP_PASSWORD: $BITBUCKET_APP_PASSWORD 
      BITBUCKET_USERNAME: $username
```

## Support
If you’d like help with this pipe, or you have an issue or feature request, let us know.
The pipe is maintained by Jahid.

If you’re reporting an issue, please include:

- the version of the pipe
- relevant logs and error messages
- steps to reproduce

## License
Copyright (c) 2019 Atlassian and others.
Apache 2.0 licensed, see [LICENSE](LICENSE.txt) file.
