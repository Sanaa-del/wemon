

chrome.runtime.onMessage.addListener(function (message, sendResponse) {
    switch (message.type) {
        case 'getNetworkInfo':
            console.log('Getting Network Info...');
            console.log('Getting 2...');
            chrome.runtime.sendMessage({
                msg: "networkInfo",
                data: message.data
            });
            return true;
        case 'getCpuInfo':
            console.log('Getting CPU Info...')
            chrome.runtime.sendMessage({
                msg: "cpuInfo",
                data: message.data
            });
            return true
        case 'getSystemInfo':
            console.log('Getting System Info...')
            chrome.runtime.sendMessage({
                msg: "systemInfo",
                data: message.data
            });
            return true
        case 'getRUMSpeedIndex':
            console.log('Getting RUMSpeedIndex...')
            chrome.runtime.sendMessage({
                msg: "RUMSpeedIndex",
                data: message.data
            });
            return true
        case 'getWebInfo':
            console.log('Getting Web Info...')
            chrome.runtime.sendMessage({
                msg: "webInfo",
                data: message.data
            });
            return true
             case 'getID':
            console.log('Getting Scenario ID...')
            chrome.runtime.sendMessage({
                msg: "scenarioID",
                data: message.data
            }); 
            return true
        case 'postMetrics':
            postMetrics('POST', 'http://localhost:8000/metrics', message.data)
            return true
          
        default:
            return true
    }
});

async function postMetrics(type, path, data) {
    fetch(path, {
        method: type,
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    }).then(function (response) {
        return response.text();
    })
}
