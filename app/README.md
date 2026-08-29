# Realizer V1 App

This directory contains the lightweight browser gateway.

## Browser test
Open `browser-test.html` from the deployed GitHub Pages site to verify frontend runtime, image upload/preview, generation-input validation, and backend health connectivity.

## Main app integration
`image-upload.js` is the reusable image input controller. `generation-contract.js` defines supported generation modes. The main gateway should import these modules rather than duplicating upload validation.

Never put provider secrets in this directory.