---
date: 2023-10-14 11:27:00 +00:00
layout: post
date: 2023-10-15 16:12:21 +00:00
title: Finding the biggest items in my Photos Library
summary: A quick script to help move the biggest items out of my main Photos Library.
tags:
  - photo management
  - swift
colors:
  index_light: "#816958"
  index_dark:  "#b2978a"
---

{#
  Cover photo from https://www.pexels.com/photo/rusty-set-of-iron-weights-for-scale-in-close-up-view-8545561/
#}

I'm approaching the limit of my current iCloud storage tier, and most of that is my Photos Library.
I don't really want to pay for the next iCloud storage tier -- I'd be tripling my bill, but I'd barely use the extra space.
(My library grows pretty slowly – I've only added ~6GB of photos this year.)

What I'd rather do is move some big items out of my library, and get some space back.
I've got [a pretty good workflow][blink] for reviewing new photos, but what about ones from before I had my reviewing tool?

I wrote a short Swift script which prints a list of all the largest files in my Photos Library.
The key part is two methods in PhotoKit: [PHAsset.fetchAssets][fetchAssets] to enumerate all the files, and [PHAssetResource.assetResources][assetResources] to retrieve the original filename and file size.
The rest of the script takes the data and does some sorting and pretty-printing.

```swift {"names":{"1":"Photos","2":"AssetData","4":"localIdentifier","6":"originalFilename","8":"fileSize","10":"getAssetsBySize","12":"allAssets","14":"options","19":"asset","20":"resource","23":"data","45":"String","46":"leftPadding","47":"toLength","49":"withPad","62":"bcf","64":"photo","66":"size"}}
#!/usr/bin/env swift

import Photos

struct AssetData: Codable {
  var localIdentifier: String
  var originalFilename: String
  var fileSize: Int64
}

/// Returns a list of assets in the Photos Library.
///
/// The list is sorted by file size, from largest to smallest.
func getAssetsBySize() -> [AssetData] {
  var allAssets: [AssetData] = []

  let options: PHFetchOptions? = nil

  PHAsset.fetchAssets(with: options)
    .enumerateObjects({ (asset, _, _) in
      let resource = PHAssetResource.assetResources(for: asset)[0]

      let data = AssetData(
        localIdentifier: asset.localIdentifier,
        originalFilename: resource.originalFilename,
        fileSize: resource.value(forKey: "fileSize") as! Int64
      )

      allAssets.append(data)
    })

  allAssets.sort { $0.fileSize > $1.fileSize }

  return allAssets
}

/// Quick extension to allow left-padding a string in Swift
///
/// By user2878850 on Stack Overflow:
/// https://stackoverflow.com/a/69859859/1558022
extension String {
  func leftPadding(toLength: Int, withPad: String) -> String {
    String(
      String(reversed())
        .padding(toLength: toLength, withPad: withPad, startingAt: 0)
        .reversed()
    )
  }
}

let bcf = ByteCountFormatter()

for photo in getAssetsBySize() {
  let size =
    bcf
      .string(fromByteCount: photo.fileSize)
      .leftPadding(toLength: 8, withPad: " ")
  print("\(size)  \(photo.originalFilename)")
}
```

When I run the script, I combine it with [`head`][head] to get a list of the top N files:

```console
$ swift get_photo_sizes.swift | head -n 5
   578 MB  IMG_3607.MOV
 518.5 MB  IMG_0794.MOV
 494.1 MB  IMG_9858.MOV
 373.6 MB  IMG_1933.MOV
 372.5 MB  IMG_3751.MOV
```

In my library of 26k items, the script takes about about a minute or so to run.

I went through the first 50 or so items, one-by-one.
I moved about 30 videos out of my photos library and on to an external disk, and I deleted a few more – in total I recovered about 7GB of space.
It's not a lot, but it gives me some more breathing room.

Pretty much all these files were video messages I'd made for friends and family, and sent as soon as they were recorded.
Honestly, I think it's unlikely I'll ever watch these again -- I'm keeping them just-in-case, but I definitely don't need them in my synced-everywhere photo library.

I don't know if I'll use this exact script again, but it was a good opportunity to practice using Swift and PhotoKit.
I'm gradually building a little collection of scripts and tools I can use to do stuff with photos, and this is another pebble on that pile.

[blink]: /2023/blink/
[fetchAssets]: https://developer.apple.com/documentation/photokit/phasset/1624783-fetchassets
[assetResources]: https://developer.apple.com/documentation/photokit/phassetresource/1623988-assetresources
[head]: https://en.wikipedia.org/wiki/Head_(Unix)
