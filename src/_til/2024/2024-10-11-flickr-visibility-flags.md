---
layout: til
title: How do the `ispublic`, `isfriend` and `isfamily` flags work in the Flickr API?
date: 2024-10-11 13:14:21 +01:00
tags:
  - flickr
---
When you look up a photo in the Flickr API, you get a `visibility` object with three booleans.
For example, this is from a `flickr.photos.getInfo` response:

```
<visibility ispublic="1" isfriend="0" isfamily="0"/>
```

You get similar attributes in the APIs that return a collection of photos.
For example, this is from a `flickr.people.getPhotos` response:

```
<photo id="52559406969" ispublic="1" isfriend="0" isfamily="0" […]/>
```

I wanted to understand when and how these flags are set, so I ran an experiment with different configurations.

## Methodology

I used two photos in the Flickr Foundation account:

*   Photo 53866697336 is public
*   Photo 53972588159 is not public, and I tried a variety of privacy settings

Then I looked up these photos in the API with seven configurations:

*   As a member of the public (i.e. only with API authentication)
*   As the Flickr Foundation account (i.e. the photo owner)
*   As another Flickr member:

    * with no social connection
    * who was marked as "friend"
    * who was marked as "family"
    * who was marked as "friend" and "family"
    * who was blocked

For the "other Flickr member", I used my personal account.

## Conclusions

*   If a photo is public, the visibility is always:

    ```
    <visibility ispublic="1" isfriend="0" isfamily="0"/>
    ```

    This is true even if the photo viewer and photo owner are marked as friend/family.

*   If a photo is not-public (friends and/or family), the visibility is one of:

    ```
    <visibility ispublic="0" isfriend="1" isfamily="0"/>
    <visibility ispublic="0" isfriend="0" isfamily="1"/>
    <visibility ispublic="0" isfriend="1" isfamily="1"/>
    ```

    depending on whether the photo is visible to friends only, family only, or friends and family.

    These `visibility` values are the same for the photo's owner.

*   If a photo is private, the visibility is:

    ```
    <visibility ispublic="0" isfriend="0" isfamily="0"/>
    ```

    This is only visible to the photo's owner.

## Results

In case they're helpful, here's my complete list of results for all combinations of privacy setting and viewer.

<details>
  <summary>Results</summary>

<pre><code>looking up as photo owner
  private:
    {'id': 'private', 'ispublic': '0', 'isfriend': '0', 'isfamily': '0'}
    {'id': 'public',  'ispublic': '1', 'isfriend': '0', 'isfamily': '0'}

  friends:
    {'id': 'private', 'ispublic': '0', 'isfriend': '1', 'isfamily': '0'}
    {'id': 'public',  'ispublic': '1', 'isfriend': '0', 'isfamily': '0'}

  family:
    {'id': 'private', 'ispublic': '0', 'isfriend': '0', 'isfamily': '1'}
    {'id': 'public',  'ispublic': '1', 'isfriend': '0', 'isfamily': '0'}

  friends and family:
    {'id': 'private', 'ispublic': '0', 'isfriend': '1', 'isfamily': '1'}
    {'id': 'public',  'ispublic': '1', 'isfriend': '0', 'isfamily': '0'}

looking up as public:
  private:
    {'id': 'public',  'ispublic': '1', 'isfriend': '0', 'isfamily': '0'}

  friends:
    {'id': 'public',  'ispublic': '1', 'isfriend': '0', 'isfamily': '0'}

  family:
    {'id': 'public',  'ispublic': '1', 'isfriend': '0', 'isfamily': '0'}

  friends and family:
    {'id': 'public',  'ispublic': '1', 'isfriend': '0', 'isfamily': '0'}

looking up as other member (not contact):
  private:
    {'id': 'public',  'ispublic': '1', 'isfriend': '0', 'isfamily': '0'}

  friends:
    {'id': 'public',  'ispublic': '1', 'isfriend': '0', 'isfamily': '0'}

  family:
    {'id': 'public',  'ispublic': '1', 'isfriend': '0', 'isfamily': '0'}

  friends and family:
    {'id': 'public',  'ispublic': '1', 'isfriend': '0', 'isfamily': '0'}

looking up as other member (friend only):
  private:
    {'id': 'public',  'ispublic': '1', 'isfriend': '0', 'isfamily': '0'}

  friends:
    {'id': 'private', 'ispublic': '0', 'isfriend': '1', 'isfamily': '0'}
    {'id': 'public',  'ispublic': '1', 'isfriend': '0', 'isfamily': '0'}

  family:
    {'id': 'public',  'ispublic': '1', 'isfriend': '0', 'isfamily': '0'}

  friends and family:
    {'id': 'private', 'ispublic': '0', 'isfriend': '1', 'isfamily': '1'}
    {'id': 'public',  'ispublic': '1', 'isfriend': '0', 'isfamily': '0'}

looking up as other member (friend and family):
  private:
    {'id': 'public',  'ispublic': '1', 'isfriend': '0', 'isfamily': '0'}

  friends:
    {'id': 'private', 'ispublic': '0', 'isfriend': '1', 'isfamily': '0'}
    {'id': 'public',  'ispublic': '1', 'isfriend': '0', 'isfamily': '0'}

  family:
    {'id': 'private', 'ispublic': '0', 'isfriend': '0', 'isfamily': '1'}
    {'id': 'public',  'ispublic': '1', 'isfriend': '0', 'isfamily': '0'}

  friends and family:
    {'id': 'private', 'ispublic': '0', 'isfriend': '1', 'isfamily': '1'}
    {'id': 'public',  'ispublic': '1', 'isfriend': '0', 'isfamily': '0'}

looking up as other member (family only):
  private:
    {'id': 'public',  'ispublic': '1', 'isfriend': '0', 'isfamily': '0'}

  friends:
    {'id': 'public',  'ispublic': '1', 'isfriend': '0', 'isfamily': '0'}

  family:
    {'id': 'private', 'ispublic': '0', 'isfriend': '0', 'isfamily': '1'}
    {'id': 'public',  'ispublic': '1', 'isfriend': '0', 'isfamily': '0'}

  friends and family:
    {'id': 'private', 'ispublic': '0', 'isfriend': '1', 'isfamily': '1'}
    {'id': 'public',  'ispublic': '1', 'isfriend': '0', 'isfamily': '0'}

looking up as other member (blocked):
  private:
    {'id': 'public',  'ispublic': '1', 'isfriend': '0', 'isfamily': '0'}

  friends:
    {'id': 'public',  'ispublic': '1', 'isfriend': '0', 'isfamily': '0'}

  family:
    {'id': 'public',  'ispublic': '1', 'isfriend': '0', 'isfamily': '0'}

  friends and family:
    {'id': 'public',  'ispublic': '1', 'isfriend': '0', 'isfamily': '0'}</code></pre>

</details>
