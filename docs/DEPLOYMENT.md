# Deployment

## GitHub Pages

The `app/index.html` browser gateway can be published as a static site. GitHub Pages only serves the frontend; it does not execute Python or AI video inference.

## Backend

Run the Python backend on a machine or hosted service that can reach the selected video-generation engine.

## Low-power devices

A lightweight device such as a 4 GB Celeron tablet should use the browser gateway while generation runs on a remote GPU or hosted provider.
