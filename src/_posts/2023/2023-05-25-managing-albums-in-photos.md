---
layout: post
date: 2023-05-25 21:02:22 +0000
title: Snippets to manage albums in Photos.app
summary: AppleScript only allows us to add photos to an album; dipping into Swift and PhotoKit lets us both add and remove photos.
tags:
  - applescript
  - swift
  - macos
  - photo management
colors:
  index_light: "#4f4f4f"
  index_dark:  "#9da3a8"
---

Recently I've been building some tools to help me manage my photo collection, and part of that involves moving photos in and out of albums.
The [tool I've built](https://github.com/alexwlchan/photo-reviewer) is very specific to my workflow and unlikely to be immediately useful to anyone else, but I thought some of the code for managing albums might be of wider use.

{% table_of_contents %}

## Local identifiers: unambiguously specify photos and albums

Inside Photos.app, everything has a unique identifier that identifies the thing -- photos, videos, albums, and more.
They aren't exposed in the user-facing portion of the app, but they're useful when writing scripts that manipulate photos.

These local identifiers sometimes appear in script output; for example in these AppleScript snippets where I'm looking up a photo (or a "media item"), an album, and the currently selected item:

```applescript
tell application "Photos" to get (first media item whose filename is "IMG_3912.HEIC")
-- media item id "01DC2841-C4EB-422B-9B44-80C774F3AE66/L0/001" of application "Photos"

tell application "Photos" to get (first album whose name is "Cross stitch")
-- album id "6C568ABA-C5D2-459B-999D-DC4C2EBEDF5C/L0/040" of application "Photos"

tell application "Photos" to get selection
-- media item id 33009721-6C81-4958-80F0-069AEDC5792F/L0/001
```

These identifiers really are *local* -- I have two Macs syncing to my iCloud Photo Library, but they've got different local identifiers for the same photo.

You can see above how to get the local identifier for a photo or an album if you know some of its properties.
Note that these properties may be ambiguous, whereas local identifiers are unambiguous -- for example, my library might have two photos called IMG_3912.HEIC, but it only has one photo with that local identifier.

In the snippets below, I'm going to assume you already know the local identifier, but if not you can adapt the code to find it first.

## Add photos to an album with AppleScript

I started by looking at the AppleScript dictionary for Photos, which includes an `add` verb.
You pass it a list of media items and an album, like so:

```applescript
tell application "Photos"
  set thePhoto to {media item id "A6A67A86-F931-4178-97E2-9F1DAD57A65C/L0/001"}
  set theAlbum to album id "6C568ABA-C5D2-459B-999D-DC4C2EBEDF5C/L0/040"
  add thePhoto to theAlbum
end tell
```

You can extend this to add multiple photos to an album, by adding to the list, for example:

```applescript
tell application "Photos"
  set thePhoto to {¬
    media item id "A6A67A86-F931-4178-97E2-9F1DAD57A65C/L0/001", ¬
    media item id "41BE6092-F40A-4CAA-91DE-9980C6196698/L0/001", ¬
    media item id ¬
      "DDFD08E2-098C-463C-9EA2-892C50E7B24B/L0/001"}
  set theAlbum to album id "6C568ABA-C5D2-459B-999D-DC4C2EBEDF5C/L0/040"
  add thePhoto to theAlbum
end tell
```

(Writing this example is also how I learnt that Applescript uses `¬` as the ["continuation character"][continuation], when you want to split a complex expression over multiple lines -- similar to backslashes in many other programming languages.)

So far, so simple.

[continuation]: https://developer.apple.com/library/archive/documentation/AppleScript/Conceptual/AppleScriptLangGuide/conceptual/ASLR_lexical_conventions.html#//apple_ref/doc/uid/TP40000983-CH214-SW9

## Remove photos from an album with AppleScript

AppleScript has the `add` verb for adding items to an album, so it must have a `remove` verb for removing them, right?

Yeah… nope.
Apparently iPhoto had [such a verb in 2009][iphoto], but that bit of the AppleScript dictionary never made it to Photos.
It's annoying if unsurprising -- AppleScript has never felt like a major priority for Apple, and there are lots of feature gaps like this.

While looking around the web, I did see people suggesting a workaround using AppleScript: create a new album, copy all-but-one-item from the old album into the new album, then delete the old album.
That's a neat trick, but I didn't want to rely on it.
It feels quite fragile, and I imagine it might be quite slow with larger albums.

Instead, I decided to look beyond AppleScript.

[iphoto]: https://stackoverflow.com/a/943106/1558022

## To PhotoKit, via Swift

AppleScript can't do it, but I know it must be possible to programatically remove photos from an album -- I've used several third-party apps that can do it.

I did some searching, and I stumbled upon [PhotoKit], which is Apple's framework for working with the Photos app.
It has a much more full-featured API, and can do plenty of things AppleScript can't.
I quickly realised that this was what I should be using.

Although most people use PhotoKit in a full-sized app, you can also use it in Swift scripts, which is more appropriate for my project.
I'm not trying to write an entire app, I'm trying to write some small automations.
Here's an example script using PhotoKit:

```swift
#!/usr/bin/env swift

import Photos

let options = PHFetchOptions()
let assets = PHAsset.fetchAssets(with: options)

print("There are \(assets.count) items in your Photos library")
```

I can run it from Terminal like so:

```console
$ swift count_photos.swift
There are 25760 items in your Photos library
```

Now let's put it to work!

[PhotoKit]: https://developer.apple.com/documentation/photokit

## Add photos to an album with Swift

This is more complicated than the AppleScript:

```swift
#!/usr/bin/env swift

import Photos

let photos =
  PHAsset
    .fetchAssets(
      withLocalIdentifiers: ["A6A67A86-F931-4178-97E2-9F1DAD57A65C/L0/001"],
      options: nil
    )

guard let album =
  PHAssetCollection
    .fetchAssetCollections(
      withLocalIdentifiers: ["6C568ABA-C5D2-459B-999D-DC4C2EBEDF5C/L0/040"],
      options: nil
    )
    .firstObject else {
      fatalError("Could not find album!")
    }

try PHPhotoLibrary.shared().performChangesAndWait {
  let changeAlbum =
    PHAssetCollectionChangeRequest(for: album)!

  changeAlbum.addAssets(photos)
}
```

First we retrieve the photo with [PHAsset.fetchAssets][fetchAssets] -- a PHAsset is any item in your Photos library, including photos and videos.
I'm only getting a single photo here, but you could get multiple photos by adding to the list of local identifiers.
This returns a PHFetchResult, which is a collection of the assets that were found.
We could extract the individual photo, but this collection is the right format for the addAssets method we're going to use further down.

Next we look up the album with [PHAssetCollection.fetchAssetCollections][fetchAssetCollections]; an asset collection is the PhotoKit term for an album.
This also returns a PHFetchResult, which is a collection of albums, and I'm just grabbing the first item.

If the album doesn't exist, then PHFetchResult.firstObject will be `nil`.
There's not a lot I can do in this case, so I'm wrapping it in a simple `guard` statement that will crash the script if the album isn't there.
This isn't especially sophisticated, but the `fatalError` allows me to provide a meaningful error message -- more than if I just force-unwrapped with `firstObject!`.

I'm then using the photo and album in a [performChangesAndWait] block.
First we create a change request for the album, then we make a single change: adding the photo.
This method blocks, and it won't complete until the photo has been added to the album.

[fetchAssets]: https://developer.apple.com/documentation/photokit/phasset/1624732-fetchassets
[fetchAssetCollections]: https://developer.apple.com/documentation/photokit/phassetcollection/1618510-fetchassetcollections
[performChangesAndWait]: https://developer.apple.com/documentation/photokit/phphotolibrary/1620747-performchangesandwait

## Remove photos from an album with Swift

This is almost identical to the code above, with just a single change: we call removeAssets instead of addAssets.

```swift
…

try PHPhotoLibrary.shared().performChangesAndWait {
  let changeAlbum =
    PHAssetCollectionChangeRequest(for: album)!

  changeAlbum.removeAssets(photos)
}
```

## Final thoughts

Unlike the AppleScript I started with, PhotoKit and Swift means I have access to a Photos API which Apple cares about -- and it'll be maintained accordingly.
I doubt the Photos–AppleScript integration will ever change again, but PhotoKit is being actively developed and improved.

This isn't the [first][appearance] [time][live_text] I've used Swift for scripting, and I doubt it'll be the last -- having easy access to Apple's frameworks makes it a very appealing choice.
I haven't seen many other people using it yet, but I think Swift could be a big thing in Mac automation.

[appearance]: /2022/changing-the-macos-accent-colour/
[live_text]: /2022/live-text-script/
