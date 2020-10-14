customElements.define('x-frame-bypass', class extends HTMLIFrameElement {
	constructor () {
		super()
	}
	connectedCallback () {
		this.load(this.src)
		this.src = ''
		this.sandbox = '' + this.sandbox || 'allow-forms allow-modals allow-pointer-lock allow-popups allow-popups-to-escape-sandbox allow-presentation allow-same-origin allow-scripts allow-top-navigation-by-user-activation' // all except allow-top-navigation
	}
	load (url, options) {
		if (!url || !url.startsWith('http'))
			throw new Error(`X-Frame-Bypass src ${url} does not start with http(s)://`)
		console.log('X-Frame-Bypass loading:', url)
		this.srcdoc = `<html>
<head>
	<style>
	.loader {
		position: absolute;
		top: calc(50% - 25px);
		left: calc(50% - 25px);
		width: 50px;
		height: 50px;
		background-color: #333;
		border-radius: 50%;
		animation: loader 1s infinite ease-in-out;
	}
	@keyframes loader {
		0% {
		transform: scale(0);
		}
		100% {
		transform: scale(1);
		opacity: 0;
		}
	}
	</style>

</head>
<body>
	<div class="loader"></div>
</body>
</html>`
		this.fetchProxy(url, options, 0).then(res => res.text()).then(data => {
			if (data)
				this.srcdoc = data.replace(/<head([^>]*)>/i, `<head$1>
	<base href="${url}">
	<script type="text/javascript" src="http://code.jquery.com/jquery-1.7.1.min.js"></script>
	<script type="text/javascript">
	/*
	* Firebug/Web Inspector Outline Implementation using jQuery
	* Tested to work in Chrome, FF, Safari. Buggy in IE ;(
	* Andrew Childs <ac@glomerate.com>
	*
	* Example Setup:
	* var myClickHandler = function (element) { console.log('Clicked element:', element); }
	* var myDomOutline = DomOutline({ onClick: myClickHandler, filter: '.debug' });
	*
	* Public API:
	* myDomOutline.start();
	* myDomOutline.stop();
	*/
	var DomOutline = function (options) {
		options = options || {};
		var blank = '';
		var pub = {};

		var list = '';
		var self = {
				opts: {
						namespace: options.namespace || 'DomOutline',
						borderWidth: options.borderWidth || 2,
						onClick: options.onClick || false,
						filter: options.filter || false
				},
				keyCodes: {
						BACKSPACE: 8,
						ESC: 27,
						DELETE: 46
				},
				active: false,
				initialized: false,
				elements: {}
		};

		function writeStylesheet(css) {
				var element = document.createElement('style');
				element.type = 'text/css';
				document.getElementsByTagName('head')[0].appendChild(element);

				if (element.styleSheet) {
						element.styleSheet.cssText = css; // IE
				} else {
						element.innerHTML = css; // Non-IE
				}
		}

		function initStylesheet() {
				if (self.initialized !== true) {
						var css = '' +
								'.' + self.opts.namespace + ' {' +
								'    background: #09c;' +
								'    position: absolute;' +
								'    z-index: 1000000;' +
								'}' +
								'.' + self.opts.namespace + '_label {' +
								'    background: #09c;' +
								'    border-radius: 2px;' +
								'    color: #fff;' +
								'    font: bold 12px/12px Helvetica, sans-serif;' +
								'    padding: 4px 6px;' +
								'    position: absolute;' +
								'    text-shadow: 0 1px 1px rgba(0, 0, 0, 0.25);' +
								'    z-index: 1000001;' +
								'}';

						writeStylesheet(css);
						self.initialized = true;
				}
		}

		function createOutlineElements() {
				self.elements.label = jQuery('<div></div>').addClass(self.opts.namespace + '_label').appendTo('body');
				self.elements.top = jQuery('<div></div>').addClass(self.opts.namespace).appendTo('body');
				self.elements.bottom = jQuery('<div></div>').addClass(self.opts.namespace).appendTo('body');
				self.elements.left = jQuery('<div></div>').addClass(self.opts.namespace).appendTo('body');
				self.elements.right = jQuery('<div></div>').addClass(self.opts.namespace).appendTo('body');
		}

		function removeOutlineElements() {
				jQuery.each(self.elements, function(name, element) {
						element.remove();
				});
		}

		function compileLabelText(element, x, y) {
				var label = element.tagName.toLowerCase();
				if (element.id) {
						label += '#' + element.id;
				}
				if (element.className) {
						label += ('.' + jQuery.trim(element.className).replace(/ /g, '.')).replace(/\.\.+/g, '.');
				}
	var dims = ' (' + Math.round(x) + 'x' + Math.round(y) + ')'
				return dims;
		}

		function getScrollTop() {
				if (!self.elements.window) {
						self.elements.window = jQuery(window);
				}
				return self.elements.window.scrollTop();
		}

		function updateOutlinePosition(e) {
				if (e.target.className.indexOf(self.opts.namespace) !== -1) {
						return;
				}
				if (self.opts.filter) {
						if (!jQuery(e.target).is(self.opts.filter)) {
								return;
						}
				}
				pub.element = e.target;

				var b = self.opts.borderWidth;
				var scroll_top = getScrollTop();
				var pos = pub.element.getBoundingClientRect();
				var top = pos.top + scroll_top;
				var x = e.clientX;
				var y =  e.clientY;
				var label_text = compileLabelText(pub.element, x, y);
				self.list = self.list + label_text
				var label_top = Math.max(0, top - 20 - b, scroll_top);
				var label_left = Math.max(0, pos.left - b);

				self.elements.label.css({ top: label_top, left: label_left }).text(label_text);
				self.elements.top.css({ top: Math.max(0, top - b), left: pos.left - b, width: pos.width + b, height: b });
				self.elements.bottom.css({ top: top + pos.height, left: pos.left - b, width: pos.width + b, height: b });
				self.elements.left.css({ top: top - b, left: Math.max(0, pos.left - b), width: b, height: pos.height + b });
				self.elements.right.css({ top: top - b, left: pos.left + pos.width, width: b, height: pos.height + (b * 2) });

		}

		function stopOnEscape(e) {
				if (e.keyCode === self.keyCodes.ESC || e.keyCode === self.keyCodes.BACKSPACE || e.keyCode === self.keyCodes.DELETE) {
						pub.stop();
				}
				var blob = new Blob([self.list], { type: "text/plain;charset=utf-8" });
				saveAs(blob, "dynamic.txt");//server side
				return false;
		}

		function clickHandler(e) {

				self.opts.onClick(pub.element);
				return false;
		}

		pub.start = function () {
				initStylesheet();
				if (self.active !== true) {
						self.active = true;
						createOutlineElements();
						jQuery('body').on('click.' + self.opts.namespace, updateOutlinePosition);
						jQuery('body').on('keyup.' + self.opts.namespace, stopOnEscape);
						if (self.opts.onClick) {
								setTimeout(function () {
										jQuery('body').on('mousemove.' + self.opts.namespace, function(e){
												if (self.opts.filter) {
														if (!jQuery(e.target).is(self.opts.filter)) {
																return false;
														}
												}
												clickHandler.call(this, e);
										});
								}, 50);
						}
				}

		};

		pub.stop = function () {
				self.active = false;
				removeOutlineElements();
				jQuery('body').off('click.' + self.opts.namespace)
						.off('keyup.' + self.opts.namespace)
						.off('click.' + self.opts.namespace);
		};

		return pub;
	};


	$(document).ready(function() {

	console.log('in file##########***');
	var myClickHandler = function (element) { console.log('Clicked element:', element); }
	 var myDomOutline  = new DomOutline({ onClick: myDomOutline });// myClickHandler
		// Start outline:
		myDomOutline.start();
		//console.log(final)
		// Stop outline (also stopped on escape/backspace/delete keys):
		//myDomOutline.stop();


	});
	</script>
	<script>
	// X-Frame-Bypass navigation event handlers
	document.addEventListener('click', e => {
		if (frameElement && document.activeElement && document.activeElement.href) {
			e.preventDefault()
			frameElement.load(document.activeElement.href)
		}
	})
	document.addEventListener('submit', e => {
		if (frameElement && document.activeElement && document.activeElement.form && document.activeElement.form.action) {
			e.preventDefault()
			if (document.activeElement.form.method === 'post')
				frameElement.load(document.activeElement.form.action, {method: 'post', body: new FormData(document.activeElement.form)})
			else
				frameElement.load(document.activeElement.form.action + '?' + new URLSearchParams(new FormData(document.activeElement.form)))
		}
	})
	</script>`)
		}).catch(e => console.error('Cannot load X-Frame-Bypass:', e))
	}
	fetchProxy (url, options, i) {
		const proxy = [
			'https://cors.io/?',
			'https://jsonp.afeld.me/?url=',
			'https://cors-anywhere.herokuapp.com/'
		]
		return fetch(proxy[i] + url, options).then(res => {
			if (!res.ok)
				throw new Error(`${res.status} ${res.statusText} this cant be done heree`);
			return res
		}).catch(error => {
			if (i === proxy.length - 1)
				throw error
			return this.fetchProxy(url, options, i + 1)
		})
	}
}, {extends: 'iframe'})
