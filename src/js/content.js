// This script will be injected into every page that matches the patterns defined in the manifest.json

// Function to extract query parameters from the current tab's URL
function getQueryParams() {
    const params = {};
    const searchParams = new URLSearchParams(window.location.search);
    searchParams.forEach((value, key) => {
        params[key] = value;
    });
    console.log(params);
    return params;
}

// Retrieve the scenario ID from the URL parameters
const queryParams = getQueryParams();
const scenarioId = queryParams['scenario'];

// Optionally, you might want to send this scenario ID to the background script or use it within this script
console.log("Scenario ID extracted:", scenarioId);

// If you need to send this data to the background script
chrome.runtime.sendMessage({scenarioId: scenarioId}, function(response) {
    console.log("Response from background:", response);
});

// Ensure you have the appropriate listeners in the background.js to handle this message.

