// Encode an SVG element as a base64 data uri.
function svgToBase64Image(svgElement) {
  var div = document.createElement("div");
  div.appendChild(svgElement.cloneNode(true));
  return "data:image/svg+xml;base64," + window.btoa(div.innerHTML);
}

// Encode SVG elements that are direct descendants of the body component as base64 strings
var svgUrls = Array.from(document.querySelectorAll("body > svg"))
  .map((svg) => 'url("' + svgToBase64Image(svg) + '")')
  .join(",");

// Set page background to SVG base64 string values to create repeating pattern effect
document.querySelector("html").style.background = svgUrls;

// Add click handlers to expand details element in API docs containing the link target
// Without this, hash links within nested areas of API docs do not work
PROP_GROUP_LINK_SELECTOR =
  '[data-param-name="show_props"] a[href*="#"]:not([href*="loose"])';
LOOSE_MATCHING_LINK_SELECTOR = 'a[href$="#loose-matching"]';
SEARCH_LINK_SELECTOR = 'a[href$="#search"]';
BLOCK_DOC_LINK_SELECTOR = 'a[href="#the-unicodeblock-object"]';

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function addClickHandlersAfterDelay() {
  await sleep(1000);
  const apiEndpoints = document.querySelectorAll(".opblock");
  apiEndpoints.forEach((el) =>
    el.addEventListener("click", () => addClickHandlers(el), {
      once: true,
    })
  );
}

async function addClickHandlers(parent) {
  await sleep(500);
  addPropGroupClickHandlers(parent);
  addBlockDocLinks(parent);
  addLinkClickHandlers(parent, LOOSE_MATCHING_LINK_SELECTOR);
  addLinkClickHandlers(parent, SEARCH_LINK_SELECTOR);
}

const addPropGroupClickHandlers = (parent) =>
  parent.querySelectorAll(PROP_GROUP_LINK_SELECTOR).forEach((a) => {
    a.addEventListener("click", (e) => {
      openDetailsElementById(e, "#unicode-characters");
      openDetailsElementById(e, a.hash);
    });
  });

const addBlockDocLinks = (parent) => 
  parent.querySelectorAll(BLOCK_DOC_LINK_SELECTOR).forEach((a) => {
    a.addEventListener("click", (e) => {
      openDetailsElementById(e, "#unicode-blocks");
      openDetailsElementById(e, a.hash);
    });
  });

const addLinkClickHandlers = (parent, selector) =>
  parent
    .querySelectorAll(selector)
    .forEach((a) =>
      a.addEventListener("click", (e) => openDetailsElementById(e, a.hash))
    );

function openDetailsElementById(event, id) {
  const headingElement = document.querySelector(`${id}`);
  if (headingElement) {
    const detailsElement = headingElement.closest("details");
    if (detailsElement) {
      detailsElement.open = true;
    }
  }
  event.stopPropagation();
}

window.addEventListener("load", addClickHandlersAfterDelay);
