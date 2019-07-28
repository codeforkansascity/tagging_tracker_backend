# Terraform Setup

Work in progress. Current code should get a single uwsgi container running on port 8000.

## TODO

- Nginx reverse proxy
    - Ideally using a file socket
- Remote state
- Finish DB setup
    - Given costs of a dedicated instance this hasn't really been worked out.
    Should be fairly easy to setup so wasn't prioritized. Considered using
    serverless service but not currently available on Terraform.
