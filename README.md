# DLSS5 Gaming Guide

Production repository for the DLSS5 installation and tuning guide for GeForce RTX 5080.

## Production

- Target host: `gaming.ramsu.ru`
- Web root: `/home/mainuser/web/gaming.ramsu.ru/public_html`
- Production file: `index.html`
- Deployment: GitHub Actions on every push to `main` that changes `index.html`, plus manual `workflow_dispatch`.

## Deployment secrets

The repository workflow expects these GitHub Actions secrets:

- `SSH_HOST` — SSH host or IP of the VPS
- `SSH_PORT` — SSH port, normally `22`
- `SSH_USER` — deployment user, initially `mainuser`
- `SSH_PRIVATE_KEY` — private Ed25519 deploy key

Never commit the private key to the repository.

## Update policy

`index.html` is the canonical production artifact. Changes to the DLSS5 guide should update this file; the deployment workflow publishes it atomically to the VPS.
