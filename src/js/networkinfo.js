import { RUMSpeedIndex } from './rum-speedindex.js'
const connection = window.navigator.connection ||
    window.navigator.mozConnection ||
    null;


const info = new Array();
function sendToBackground(eventName, eventData) {

    console.log('test console')
    chrome.runtime.sendMessage({ type: eventName, data: eventData });
}

async function initCpu() {
    chrome.system.cpu.getInfo(function (info) {

        var cpuName = info.modelName.replace(/\(R\)/g, '®').replace(/\(TM\)/, '™');
        var cpuArch = info.archName.replace(/_/g, '-');
        var cpuFeatures = info.features.join(', ').toUpperCase().replace(/_/g, '.') || '-';
        var cpuNumOfProcessors = info.numOfProcessors;
        var cpuProcessors = info.processors;

        let cpuInformation = { cpuName: cpuName, cpuArch: cpuArch, cpuFeatures: cpuFeatures, cpuNumOfProcessors: cpuNumOfProcessors, cpuProcessors: cpuProcessors }
        sendToBackground('getCpuInfo', cpuInformation);
    })
}

function initMemory() {
    chrome.system.memory.getInfo(function (memoryInfo) {

        let systemAvailableCapacity = memoryInfo.availableCapacity / 1073741824;
        let systemCapacity = memoryInfo.capacity / 1073741824;
        let systemInfo = { systemCapacity: systemCapacity, systemAvailableCapacity: systemAvailableCapacity }
        sendToBackground('getSystemInfo', systemInfo);
    });

}

function postMetrics() {
    setTimeout(() => {
        console.log("Posting...")
        sendToBackground('postMetrics', info);
    }, 100);
}

function getSpeedIndex() { return { RUMSpeedIndex: RUMSpeedIndex(window) } }

const rumSpeedIndex = getSpeedIndex()
sendToBackground('getRUMSpeedIndex', rumSpeedIndex);

function performanceTiming() {
    let timing = performance.getEntriesByType("navigation")[0]
    let protocol = timing.nextHopProtocol; //http/1.1 h2 h3 
    let pageloadtime = Math.round(timing.duration);
    let ttfb = Math.round(timing.responseStart)
    let redirect = Math.round(timing.redirectEnd - timing.redirectStart)
    let dns = Math.round(timing.domainLookupEnd - timing.domainLookupStart)
    let connect = Math.round(timing.connectEnd - timing.connectStart)
    let request = Math.round(timing.responseEnd - timing.requestStart)
    let response = Math.round(timing.responseEnd - timing.responseStart)
    let dom = Math.round(timing.domComplete - timing.responseEnd)
    let domParse = Math.round(timing.domInteractive - timing.responseEnd)
    let domScripts = Math.round(timing.domContentLoadedEventStart - timing.domInteractive)
    let contentLoaded = Math.round(timing.domContentLoadedEventEnd - timing.domContentLoadedEventStart)
    let domSubRes = Math.round(timing.domComplete - timing.domContentLoadedEventEnd)
    let load = Math.round(timing.loadEventEnd - timing.loadEventStart)
    chrome.runtime.sendMessage({
        type: 'getWebInfo', data: {
            protocol: protocol,
            pageloadtime: pageloadtime,
            ttfb: ttfb,
            redirect: redirect,
            dns: dns,
            connect: connect,
            request: request,
            response: response,
            dom: dom,
            domParse: domParse,
            domScripts: domScripts,
            contentLoaded: contentLoaded,
            domSubRes: domSubRes,
            load: load
        }
    })
}


function getNetworkMetrics() {
    initCpu();
    initMemory();
   
    return {
        effectiveType: connection.effectiveType,
        downlink: connection.downlink,
        rtt: connection.rtt,
    }
}

chrome.tabs.query({
    active: true,               // Select active tabs
    lastFocusedWindow: true     // In the current window
}, function (array_of_Tabs) {
    chrome.scripting.executeScript({ target: { tabId: array_of_Tabs[0].id }, func: performanceTiming });
    console.log("URL");
    console.log(lastFocusedWindow.location.toString());
});

if (connection === null) {
    console.log("Not Supported")
} else {
    document.getElementById("effectiveType").innerHTML = connection.effectiveType
    document.getElementById("downlink").innerHTML = connection.downlink
    document.getElementById("rtt").innerHTML = connection.rtt
}


const networkMetrics = getNetworkMetrics();
sendToBackground('getNetworkInfo', networkMetrics);


async function getCurrentTabUrl() {
  var tabs = await chrome.tabs.query({ active: true })
  var text = tabs[0].url
  var id = text.split('?scenario=')[1]
  let scenarioInformation = { ID: id }
  sendToBackground('getID', scenarioInformation);

}

getCurrentTabUrl()

chrome.runtime.onMessage.addListener(function (message, sendResponse) {
    console.log("Received " + message.msg + ' ' + JSON.stringify(message.data));
    if (!!message.msg) info.push(message.data);
});





postMetrics();

