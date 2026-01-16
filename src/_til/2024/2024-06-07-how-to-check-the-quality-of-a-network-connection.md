---
layout: til
date: 2024-06-07 10:26:31 +01:00
title: How to check the quality of a network connection
summary: |
  Using an `NWPathMonitor` and inspecting the value of `NWPath.status`, `NWPath.isExpensive` and `NWPath.isConstrained` can tell you what sort of connection you're running on.
tags:
  - swift
  - networking
---
A couple of times I've been listening to [ATP](https://atp.fm/) and Marco has mentioned there are APIs an app can use to check the quality of your network connection -- for example, an app might choose to download podcasts over Wi-Fi but not cellular.
These APIs have been present on iOS for a long time, but they're also available on macOS.

I became curious about this when I was installing a Homebrew package while on a train, and Homebrew started its auto-updater.
This is precisely the wrong time to do it, because I have a very unreliable connection -- I want to spend what limited bandwidth I have installing the package I'm installing, not on updating Homebrew.

I wasn't sure what API it was, so I decided to find out.

---

I struggled to find anything on Google, so I described this API to ChatGPT.
It quickly pointed me at two items in Apple's documentation:

*   [`NWPathMonitor`](https://developer.apple.com/documentation/network/nwpathmonitor), which can monitor the network connection for you, and
*   [`NWPath`](https://developer.apple.com/documentation/network/nwpath), an object that describes the properties of the current network connection.

The `NWPath` object has three attributes that are interesting:

*   `status` – essentially, is the connection working.

*   `isExpensive` – is it a connection that's considered "expensive", for example a cellular hotspot.
    This is the API I was originally thinking of.

*   `isConstrained` – has the user enabled Low Data Mode for this connection.
    This is a [user preference](https://apple.stackexchange.com/questions/449668/what-is-low-data-mode-on-macos-ventura-wlan-exactly) where you can ask the system to minimise data usage on the network.
    
    This is separate to Low Power Mode – when I enable Low Power Mode on my Mac, I don't see Low Data Mode on the connection.

I don't have an immediate use for this API so this is mostly for idle curiosity, but I did write a small script to exercise this API – it monitors the network connection for a minute, and logs whether the network is up, and whether it's expensive/constrained.

```swift
import Foundation
import Network

class NetworkStatusChecker {
    init() {
        let monitor = NWPathMonitor()
        monitor.pathUpdateHandler = { path in
            self.logCurrentStatus(path: path)
        }
        monitor.start(queue: DispatchQueue.global(qos: .background))
    }

    private func logCurrentStatus(path: NWPath) {
        if path.status == .satisfied {
            print("✅ We’re connected; isExpensive = \(path.isExpensive), isConstrained = \(path.isConstrained).")
        } else {
            print("❌ We’re not connected.")
        }
    }
}

let networkChecker = NetworkStatusChecker()

// Watch network changes for a minute
Thread.sleep(forTimeInterval: 60)
```

Now I know that "expensive" and "constrained" are the terminology that Apple uses, I can find other APIs that use it -- for example, [`allowsExpensiveNetworkAccess`](https://developer.apple.com/documentation/foundation/urlsessionconfiguration/3235752-allowsexpensivenetworkaccess) which allows you to decide whether a URL session will fetch data over an expensive connection.
