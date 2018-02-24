/* Classic bundle
   Includes all site-wide scripts and utilities
   Also includes the global stylesheet. */

import '../style/main.scss';

import payAndSubmit from './stripe-payment';

// Required for live reloading
if (module.hot) module.hot.accept();

// Attach to window to make accessible to inline scripts
window.payAndSubmit = payAndSubmit;
