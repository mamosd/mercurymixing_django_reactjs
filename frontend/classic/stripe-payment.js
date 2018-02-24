/* globals StripeCheckout */

/**
 * Gathers payment info using Stripe's checkout.js and submits the generated
 * token to the server via a form. The form must have an input with id
 * 'id_stripe_token' to receive the token. The 'working' class will be added
 * to the form while the popup is open.
 *
 * YOU MUST INCLUDE checkout.js BEFORE CALLING THIS FUNCTION
 *
 * @param {HTMLElement} form - Will be submitted after payment details are captured
 * @param {Object} stripeConfig - Configuration object for checkout.js
 *
 * @example
 * <form id="my-form" method="POST">
 *  <input type="hidden" id="id_stripe_token" />
 * </form>
 *
 * <script src="https://checkout.stripe.com/checkout.js"></script>
 * <script>
 *  config = {key: 'STRIPE PUBLIC KEY', amount: 1000};
 *  payAndSubmit(document.querySelector('#my-form'), config);
 * </script>
 *
 * In the example the user will be shown the popup with a charge of $10.00.
 */
export default function payAndSubmit(form, stripeConfig) {
	const tokenInput = form.querySelector('#id_stripe_token');
	let paymentComplete = false;

	// We can't do anything without StripeCheckout
	if (typeof StripeCheckout === 'undefined') {
		// eslint-disable-next-line no-alert
		alert('Error: Could not connect to our payment processor.');
		return;
	}

	// Indicate the form is being processed
	form.classList.add('working');

	StripeCheckout.open({
		...stripeConfig,

		// Executed after the user fills the payment details
		// Performs the actual form submission
		token: function onTokenReady(token) {
			tokenInput.value = token.id;
			paymentComplete = true;
			form.submit();
		},

		// Executed whenever the payment dialog is closed
		// either after token() is called, or the user closes it
		closed: function cleanUp() {
			// If the user dismissed the popup...
			if (!paymentComplete) {
				form.classList.remove('working');
			}
		},
	});
}
