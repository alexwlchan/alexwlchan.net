---
layout: til
date: 2024-07-05 12:41:56 +01:00
title: Using the Wikimedia Commons API to tell if a file has been deleted
tags:
  - wikimedia commons
---
Flickypedia Backfillr Bot will occasionally try to get structured data for files which have been deleted from Wikimedia Commons.
You can see the deletion if you open the file in a web browser:

{%
  picture
  filename="deleted_wmc_file.png"
  width="506"
  class="screenshot"
  alt="Screenshot of a file on Wikimedia Commons with a red box ‘The page does not exist. The deletion, protection, and move log for the page are provided below for reference’. The log shows that the file was deleted on 26 June 2024."
  link_to="https://commons.wikimedia.org/wiki/File:Mugeni_Elijah.jpg"
%}

How can you tell if a file has been deleted using the API?

You can use the [log events API](https://www.mediawiki.org/wiki/API:Logevents) to retrieve a list of log events for this page, and filter for log events with type `delete`:

```shell
curl \
  --get 'https://commons.wikimedia.org/w/api.php' \
  --data 'action=query' \
  --data 'list=logevents' \
  --data-urlencode 'letitle=File:Mugeni Elijah.jpg' \
  --data 'format=xml' \
  --data 'letype=delete'
```

Here's the response for a file which has been deleted:

```
<?xml version="1.0"?>
<api batchcomplete="">
  <query>
    <logevents>
      <item logid="355945145" ns="6" title="File:Mugeni Elijah.jpg" pageid="0" logpage="128511537" type="delete" action="delete" user="Minorax" timestamp="2024-06-26T02:06:08Z" comment="per [[Commons:Deletion requests/Files found with 154165274@N03]]">
        <params/>
      </item>
      <item logid="335508303" ns="6" title="File:Mugeni Elijah.jpg" pageid="0" logpage="115072643" type="delete" action="delete" user="Krd" timestamp="2023-02-07T04:06:55Z" comment="No permission since 30 January 2023">
        <params/>
      </item>
    </logevents>
  </query>
</api>
```

(This file was deleted twice because it was uploaded twice -- if you remove `letype=delete`, you can see two upload events.)

Here's the response for a file which hasn't been deleted (or which doesn't exist):

```
<?xml version="1.0"?>
<api batchcomplete="">
  <query>
    <logevents/>
  </query>
</api>
```