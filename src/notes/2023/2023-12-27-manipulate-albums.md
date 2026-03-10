---
layout: note
title: How to delete albums
date: 2023-12-27 23:15:50 +00:00
topics:
  - Photo management
  - Swift
---
You can delete albums with the [deleteAssetCollections] API, for example:

```swift {"names":{"1":"Photos","2":"deleteAlbum","3":"album"}}
import Photos

func deleteAlbum(_ album: PHAssetCollection) -> Void {
    try! PHPhotoLibrary.shared().performChangesAndWait({
        PHAssetCollectionChangeRequest
            .deleteAssetCollections([album] as NSFastEnumeration)
    })
}
```

There are lots of ways to find instances of `PHAssetCollection` to pass to this function; for example, you could use [fetchTopLevelUserCollections] and filter for albums with a particular name or which are empty:

```swift {"names":{"1":"Photos","5":"collection","6":"index","7":"stop","9":"album"}}
import Photos

PHCollectionList
    .fetchTopLevelUserCollections(with: PHFetchOptions())
    .enumerateObjects({ (collection, index, stop) in
        if collection is PHAssetCollection {
            let album = collection as! PHAssetCollection

            if album.localizedTitle == "Empty" && album.estimatedAssetCount == 0 {
                print(album)
                deleteAlbum(album)
            }
        }
    })
```

[deleteAssetCollections]: https://developer.apple.com/documentation/photokit/phassetcollectionchangerequest/1619453-deleteassetcollections
[fetchTopLevelUserCollections]: https://developer.apple.com/documentation/photokit/phcollection/1618513-fetchtoplevelusercollections
