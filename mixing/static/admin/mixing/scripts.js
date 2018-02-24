(function($) {

$(document).ready(function() {
	// Click handler to toggle the "active" class
	var $togglers = $('.field-track_browser [data-target]');
	$togglers.on('click', function toggle() {
		// The selector stored in data-target will have the 'active' class toggled
		$(this.dataset.target).toggleClass('active');
	});
});

})(django.jQuery);
