// Encode an SVG element as a base64 data uri.
function svgToBase64Image(svgElement) {
  var div = document.createElement("div");
  div.appendChild(svgElement.cloneNode(true));
  return "data:image/svg+xml;base64," + window.btoa(div.innerHTML);
}

var svgUrls = Array.from(document.querySelectorAll("body > svg"))
  .map((svg) => 'url("' + svgToBase64Image(svg) + '")')
  .join(",");

document.querySelector("html").style.background = svgUrls;
