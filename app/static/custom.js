// ###### FIX FOR LINKS TO API DOCS FROM API ENDPOINT PARAMETERS  ######
// Within the Swagger UI that is generated for each API endpoint, the descriptions/help docs for various
// request parameters include links to the API docs on the same page. However, since each section for the
// API docs is implemented as a details element that is originally collapsed, links to any top-level section
// (e.g., Pagination, Search, etc) and links to any sub-section within the Core Rersources sections
// (e.g., Unicode Characters > Verbosity) will fail to navigate to the intended location unless the target
// details element or parent details element is expanded.

PROP_GROUP_LINK_SELECTOR = '[data-param-name="show_props"] a[href*="#"]:not([href*="loose"])';
LOOSE_MATCHING_LINK_SELECTOR = 'a[href$="#loose-matching"]';
SEARCH_LINK_SELECTOR = 'a[href$="#search"]';
VERBOSITY_LINK_SELECTOR = 'a[href$="#verbosity"]';
BLOCK_OBJ_LINK_SELECTOR = 'a[href="#the-unicodeblock-object"]';

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// To ensure that links from the Swagger UI to the API docs work as intended, the addClickHandlersAfterDelay
// function below is called after the page has finished loading. However, to ensure that the Swagger JS
// script has finished rendering the UI for all endpoints, this function waits for one second before
// actually doing anything.

// Next, the top-level DOM element that contains each API endpoint is retrieved. These are the expandable/
// collapsable blue blocks with a darker blue "GET" block on the left-hand side. For each API endpoint, a
// handler for the click event is added, which only runs once.

async function addClickHandlersAfterDelay() {
	await sleep(1000);
	document.querySelectorAll('.opblock').forEach((el) =>
		el.addEventListener('click', () => addClickHandlers(el), {
			once: true
		})
	);
}

// The function below is called the first time a user clicks to expand one of the API endpoint
// Swagger UI components. The addClickHandlers function finds any links to the API docs within the
// API endpoint component and adds click handlers to each link.

// The process of rendering the API endpoint parameters, help documentation, and UI to send 
// requests and inspect responses is reasonably fast, but it is not instantaneous. To ensure
// that the entire API endoint UI has loaded, the click handler waits for half of one second
// before proceeding.

async function addClickHandlers(parent) {
	await sleep(500);
	addClickHandlersWithinCharacterDetailsElement(parent);
	addClickHandlersWithinBlockDetailsElement(parent);
	addClickHandlersForLinksAtTopLevel(parent, LOOSE_MATCHING_LINK_SELECTOR);
	addClickHandlersForLinksAtTopLevel(parent, SEARCH_LINK_SELECTOR);
	addClickHandlersForLinksAtTopLevel(parent, VERBOSITY_LINK_SELECTOR);
}

// For links within the Unicode Characters section, the following event handler is added that
// expands the Unicode Characters details element before navigating to the section indicated
// in the hash link.

const addClickHandlersWithinCharacterDetailsElement = (parent) =>
	parent.querySelectorAll(PROP_GROUP_LINK_SELECTOR).forEach((a) => {
		a.addEventListener('click', (e) => {
			openDetailsElementById(e, '#unicode-characters');
			openDetailsElementById(e, a.hash);
		});
	});

// For links within the Unicode Blocks section, the following event handler is added that
// expands the Unicode Blocks details element before navigating to the section indicated
// in the hash link.

const addClickHandlersWithinBlockDetailsElement = (parent) =>
	parent.querySelectorAll(BLOCK_OBJ_LINK_SELECTOR).forEach((a) => {
		a.addEventListener('click', (e) => {
			openDetailsElementById(e, '#unicode-blocks');
			openDetailsElementById(e, a.hash);
		});
	});

// For links to the Pagination, Search or Loose Matching sections, the following event handler
// expands the matching details elementto ensure that the content is viewable by the user.

const addClickHandlersForLinksAtTopLevel = (parent, selector) =>
	parent
		.querySelectorAll(selector)
		.forEach((a) => a.addEventListener('click', (e) => openDetailsElementById(e, a.hash)));

// All of these event handlers utilize the function below which takes the section id from the
// hash link and locates the heading element matching that id, then locates the details element
// that is closest to the heading and expands it to reveal the section content.

function openDetailsElementById(event, id) {
	const headingElement = document.querySelector(`${id}`);
	if (headingElement) {
		const detailsElement = headingElement.closest('details');
		if (detailsElement) {
			detailsElement.open = true;
		}
	}
	event.stopPropagation();
}

// ###### SET PAGE BACKGROUND USING SVG BASE64 URLS ######
// The page background is created by converting SVG elements to base64 strings. The SVGs are
// defined in the function that creates the HTML for the API docs:
// (get_swagger_ui_html in app.docs.api_docs.swagger_ui)

// The base64 strings are used as the value of the background property for the root html element,
// which is accessed through the style property of the HTMLElement interface.

document.querySelector('html').style.background = Array.from(document.querySelectorAll('body > svg'))
	.map((svg) => 'url("' + svgToBase64Image(svg) + '")')
	.join(',');

function svgToBase64Image(svgElement) {
	var div = document.createElement('div');
	div.appendChild(svgElement.cloneNode(true));
	return 'data:image/svg+xml;base64,' + window.btoa(div.innerHTML);
}

window.addEventListener('load', addClickHandlersAfterDelay);
