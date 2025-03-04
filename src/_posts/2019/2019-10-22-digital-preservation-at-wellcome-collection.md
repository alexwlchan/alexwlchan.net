---
layout: post
date: 2019-10-22T16:01:51.760Z
title: Digital preservation at Wellcome Collection
summary: Slides from a presentation about our processes, practices, and tools.
canonical_url: https://stacks.wellcomecollection.org/digital-preservation-at-wellcome-3f86b423047
tags:
  - wellcome collection
  - digital preservation
colors:
  css_light: "#64573f"
  css_dark:  "#eeeab4"
---
*I wrote this article while I was working at Wellcome Collection. It was originally published [on their Stacks blog](https://stacks.wellcomecollection.org/digital-preservation-at-wellcome-3f86b423047) under a CC BY 4.0 license, and is reposted here in accordance with that license.*

<p><em>This is the text version of a talk I gave at </em><a href="https://www.eventbrite.co.uk/e/glam-digital-champions-digital-lunch-october-tickets-73928130027"><em>a GLAM Digital Champions event</em></a><em> on 18th October 2019.</em></p><p><em>GLAM Digital Champions is a Cambridge-based community of practitioners for sharing ideas about the use of digital technologies in Gardens, Galleries, Libraries, Archives and Museums. It was set up by </em><a href="https://twitter.com/georgeopteryx"><em>George Doji</em></a><em> and </em><a href="https://twitter.com/marycktech"><em>Mary Chester-Kadwell</em></a><em>. I met Mary at PyCon UK this year, and she invited me to come and give a brief overview of how we’re doing digital preservation at Wellcome.</em></p><p><em>You can also </em><a href="/files/2019/2019-10-18-glam-cam-digipres-slides.pdf"><em>download my slides</em></a><em> as a PDF.</em></p>

---

<figure style="width: 500px;">
  {%
    picture
    filename="h76dp2d4.jpg"
    width="500"
    alt="A room with circular, raked seating. Two men are talking, one pointing to a skeleton hanging from the skylight."
  %}
  <figcaption>The Anatomical Theatre in Cambridge. Published for R. Ackermann’s <em>History of Cambridge</em>. Credit: <a href="https://wellcomecollection.org/works/h76dp2d4">Wellcome Collection</a>. CC BY.</figcaption>
</figure>

<p>Hello everyone, and thank you having me. It’s a pleasure to be here in Cambridge.</p><p>My name is Alex. I’m a senior software developer at Wellcome Collection in London, and today I’m going to give you a brief overview of how we do digital preservation at Wellcome Collection.</p><p>For those of you who don’t know us, Wellcome Collection is <a href="https://wellcomecollection.org/pages/Wuw2MSIAACtd3Stq">a free museum and library that aims to challenge how we all think and feel about health</a>.</p><p>What does that actually mean?</p><p>Our building is a library, archive and museum all rolled into one. (No gardens yet, but we do have a couple of house plants!)</p><p>Wellcome Collection is a big place. We have a reference library and archive for researchers; we have a series of permanent and rotating exhibitions; we have event spaces and regular events; we write stories and we publish books. It covers a wide range of material around science, medicine, health and art. Alongside our physical archive, we have a large digital archive, and that’s what I’m going to talk about today.</p><p>We can imagine the process of digital preservation in three stages: production, storage, and retrieval. We choose what we’re going to save, we save it, we get it back later.</p>

<figure>
  {%
    picture
    filename="1*vR5fuMVndhE8A8ED8OqR1A.jpg"
    width="750"
    alt="A three step diagram. Production to storage, storage to retrieval."
  %}
  <figcaption>Icon credit: Legal archivist (production), by <a href="https://thenounproject.com/term/legal-archivist/1823613/">Miroslav Kurdov</a>. S3 bucket (storage) from <a href="https://commons.wikimedia.org/wiki/File:AWS_Simple_Icons_Storage_Amazon_S3.svg">AWS Simple Icons</a>. Legal counsel (retrieval), by <a href="https://thenounproject.com/term/legal-counsel/1824436">Miroslav Kurdov</a>.</figcaption>
</figure>

<p>Let’s discuss those steps in turn.</p>

---

<h2>Production</h2><p>The production process varies at Wellcome, depending on whether we are considering <a href="https://en.wikipedia.org/wiki/Digitization"><em>digitised</em></a> or <a href="https://en.wikipedia.org/wiki/Born-digital"><em>born-digital</em></a> files. Digitising means creating a digital representation of a physical object: for example, scanning a page or photographing a book. A born-digital file is one that started life as a digital file: maybe a Word document or a web page.</p><p>Let’s consider each in turn.</p>

<h3>Digitisation</h3><p>We have a lot of experience at Wellcome with digitisation: we’ve been digitising the collection for over a decade, and we have 40 million images.</p><p>How do we choose what to digitise? We have <a href="https://wellcomelibrary.org/what-we-do/digitisation/digitisation-schedules/">a long-term digitisation schedule</a>, for parts of the collection we want to digitise — often planned years in advance. We also have capacity for ad-hoc digitisation. If a researcher in New Zealand wants to see something from our collections, they can ask for that to be digitised specially, and we can try to accommodate.</p><p>So we know what we want to digitise, and we’ve picked it off the shelf — how does the digitisation happen? There are a couple of streams:</p><ul><li>We have a contract with <a href="https://archive.org/scanning">the Internet Archive</a>, who scan our bound, printed books. They have specialist book scanners that mean they can scan very quickly.</li><li>We send audiovisual material (VHS tapes, audio cassettes, etc.) to <a href="https://r3storestudios.com">R3Store</a>.</li><li><a href="https://www.townswebarchiving.com/">TownsWeb</a> work on-site at Euston Road and help to digitise our paper archives.</li><li>We’re lucky to have a team of in-house photographers, who handle anything that needs extra care — maybe it’s fragile, bulky, or even radioactive. They work closely with the conservation team.</li></ul><p>Now we have a pile of images, and we need to add them to the catalogue. We use a workflow manager called <a href="https://www.intranda.com/en/digiverso/goobi/goobi-overview/">Goobi</a>, made by Intranda. It collates metadata and OCR, adds checksums to the files, and spits out a bundle of images, <a href="https://en.wikipedia.org/wiki/Metadata_Encoding_and_Transmission_Standard">METS</a> (metadata) and <a href="https://en.wikipedia.org/wiki/ALTO_(XML)">ALTO</a> (OCR data).</p>

<figure>
  {%
    picture
    filename="1*vls47QYBTA-MLhiaQ0444A.png"
    width="750"
    alt=""
  %}
  <figcaption>A screenshot of Goobi, from <a href="https://www.intranda.com/en/digiverso/goobi/goobi-overview/">Intranda’s website</a>.</figcaption>
</figure>

<h3>Born-digital</h3><p>Born-digital archiving is something newer for us at Wellcome: it was the new shiny a few years ago, and we brought in lots of material. Now we’re starting to think more carefully about how we want to do born-digital archiving, how we’re going to catalogue it, and so on.</p><p>Suppose somebody offers us some files — we start by assessing them. Are these files a good fit for our collection? If they are, we’ll transfer them to Wellcome, and go through them in more detail. This is a more thorough analysis, where we’re looking for files that might need extra work before we can make it available. For example, PDFs of medical research are easier to present than something that’s password-protected.</p><p>To prepare the files for ingest, we are about to start using <a href="https://www.archivematica.org/en/">Archivematica</a>, an open-source digital preservation system made by Artefactual. It does a lot of automation for us: virus scanning, generating metadata and checksums, deleting <a href="https://en.wikipedia.org/wiki/.DS_Store">.DS_Store</a> and <a href="https://en.wikipedia.org/wiki/Windows_thumbnail_cache#Thumbs.db">thumbs.db</a> files that we don’t care about, and it spits out a bundle of files and metadata.</p>

<figure>
  {%
    picture
    filename="1*Lya8QRpYJe2b9RMHGIKCiQ.png"
    width="750"
    alt=""
  %}
  <figcaption>A screenshot of our Archivematica instance.</figcaption>
</figure>

<p>That gives you a brief overview of our production process, both digitised and born-digital.</p>

{%
  picture
  filename="1*ufbrVq09zlHEUDhavUm-Xw.jpg"
  width="750"
  alt=""
%}

<p>At the end of this process, we have a clutch of files and metadata, but nowhere to put them. Where do keep these precious things? Let’s talk about storage.</p>

---

<h2>Storage</h2>

{%
  picture
  filename="1*EoyW2yIN3mUPlRBe-sl_WA.png"
  width="350"
  style="float: right; margin-top: 0; margin-left: 1em; margin-bottom: 1em;"
  alt=""
%}

<p>Historically, we’ve used a storage system called <a href="https://preservica.com/">Preservica</a>, which is a fairly popular service used for digital preservation. (Although judging by hands in the room, it has yet to reach Cambridge!)</p><p>We’re in the process of migrating our storage away from Preservica. We wanted a storage service with the following attributes:</p><ul><li>Based on a common, open format for ingesting both digitised and born-digital assets</li><li>A preference for open-source software</li><li>That would allow us to batch process large volumes of data quickly. For example, if we wanted to re-run the OCR process for our digitised images.</li><li>Human-readable storage layout. We want to make it as easy as possible for future developers to understand the storage, even if the current service is no longer in use.</li><li>Running in the cloud, with content replicated to different locations and providers.</li><li>Conforming to the <a href="https://en.wikipedia.org/wiki/Don%27t_repeat_yourself">DRY (Don’t repeat yourself)</a> principles</li></ul><p>And so we’re in the process of migrating our content from Preservica up to our new storage service. (As in, half an hour before the talk, I was in a café running migration scripts!)</p>

{%
  picture
  filename="1*UuDm5nnqC5r-ssTLan1j7A.jpg"
  width="750"
  alt=""
%}

<p>In our new storage service, you upload files in <a href="https://en.wikipedia.org/wiki/BagIt">a BagIt package</a>. This is a standard packaging format, used to pass around hierarchical filesystems. It’s often used in digital libraries, and both Goobi and Archivematica can produce BagIt packages.</p><p>The storage service unpacks the BagIt “bag”, counts out the files, verifies the checksums, and generally checks everything is in order. Assuming all is well, it uploads a copy of the bag to Amazon S3, and a second copy to S3 Glacier.</p><p>Later next year, we’ll be adding a replica to Azure Blob Storage in Amsterdam (both our S3 copies are in Dublin). This gives us an extra layer of redundancy and protection, in case AWS close our account or Dublin falls into the sea.</p><p>We know we’re lucky to have in-house software developers, so we want to share this work as much as possible. All the code for the storage service is <a href="https://github.com/wellcometrust/storage-service">open-source and MIT licensed</a>, as is the <a href="https://github.com/wellcometrust/platform/tree/master/docs/rfcs/002-archival_storage">original design document</a>.</p><p>So we upload packages to the storage service, which keeps them safe in cloud storage for preservation evermore. Now suppose somebody comes to our website, and they want to see something we’ve preserved. How do they get it out? Let’s finish by discussing retrieval.</p><p><em>[Somebody asked about versioning in the Q&amp;A — for example, what if we’ve digitised a book, and we need to replace one of the images?</em></p><p><em>The BagIt spec supports partial updates with “fetch files”. You build a package with a replacement image, and a fetch file that refers to files in another location — in our case, the location of previously stored bag.</em></p><p><em>The storage service tracks the versions of a given bag, keeps every version forever, and lets you see how a bag looked at a particular point in time.]</em></p>

---

<h2>Retrieval</h2><p>We have a number of services that sit in front of the storage service, and serve content to our website. Right now we only serve digitised content, but we want to think about how to do born-digital in the future.</p><p><a href="https://digirati.com/work/galleries-libraries-archives-museums/products/digital-library-cloud-services/"><em>DLCS (Digital Library Cloud Services)</em></a><em> </em>is a service that provides <a href="https://en.wikipedia.org/wiki/International_Image_Interoperability_Framework">IIIF APIs</a> for our digitised content. IIIF is a set of standards for presenting large images, commonly used in museums and libraries. DLCS presents three types of IIIF API for us:</p><ul><li>The <em>IIIF Presentation API</em> tells you what images are available in a particular work. If a book has 100 pages, and there are 100 digitised images, the Presentation API tells you how to find them.</li><li>The <em>IIIF Image API</em> returns the images themselves. It can scale all the way from a tiny thumbnail (if you’re just skimming) to a deep zoomed version (if you’re studying in detail). This includes converting the image to different formats. Our original images are all JPEG2000, but we usually serve them as regular JPEG.</li><li>The <em>IIIF Auth API</em> controls access to images. Most of our images are completely open access, but there are a handful where we need some access controls — for example if it’s an archive about somebody who’s still alive or recently deceased.</li></ul>

<figure style="width: 500px;">
  {%
    picture
    filename="1*Yg-L-t_LAox7F5iCv_Lzag.png"
    width="500"
    alt=""
  %}
  <figcaption>An illustration of two Lorises. “The Slender Loris, in waking and sleeping posture.” Taken from <a href="https://commons.wikimedia.org/wiki/File:SlenderLorisLyd2.png">Royal Natural History volume 1, page 230</a>. Public domain.</figcaption>
</figure>

<p><a href="https://github.com/loris-imageserver/loris"><em>Loris</em></a><em> </em>is an open-source IIIF Image API server that we use to serve the other images on our website (a handful of catalogue images, and editorial images for events and exhibitions).</p><p>Presenting all the images on the site through IIIF gives them a consistent interface — the same code can be used to retrieve images everywhere.</p><p>(I previously wrote about <a href="/2017/loris-for-iiif/">our use of Loris</a> in 2017.)</p><p>So that’s how we get the images —but what about the metadata that goes with them?</p>

{%
  picture
  filename="1*ur1I7fXRMlk2kzIsxHZSXQ.png"
  width="750"
  alt=""
%}

<p>A lot of our metadata is split across different databases: Sierra for our library catalogue, Calm for our archives, Miro for our image collections, and so on. The same object is split across multiple places, and it’s hard for users to find it. It’s not clear which search box to use, and you only get a partial record.</p><p>We’ve been building a unified catalogue search that combines records from multiple databases, transforms them into a unified model, and presents all the data in one place. There’s also an open API that lets you get the search results as JSON, so other people can build their own tools on top of it.</p>

<figure>
  {%
    picture
    filename="1*qzr8XlrC5gmo3LqY4eNGhA.png"
    width="750"
    alt=""
    class="screenshot"
  %}
  <figcaption>Screenshot from <a href="https://wellcomecollection.org/works/ptnfbubj">https://wellcomecollection.org/works/ptnfbubj</a></figcaption>
</figure>

<p>What ties it all together is the new Wellcome Collection website, where people can browse the catalogue in a nice graphical viewer.</p><p>We’ve completely redesigned it, with new works pages for presenting this unified catalogue. It includes a IIIF viewer for doing deep zoom of images and browsing the pages of a book (pictured above). The new website is also much more accessible: it uses progressive enhancement and the OCR from our digitisation as alt text in the images.</p><p>Under the hood, it’s using the Catalogue API to get metadata, and DLCS and Loris to serve the images. We do a lot of user research on the website to get a sense of how well search is performing, how easily people are finding what they need, to track site performance, and so on.</p>

---

<p>So now we’ve gone from start to finish: we’ve chosen something we want to store, we’ve saved it in the storage service, and somebody has found it through our website on the other side. I hope this has given you a flavour of how we do digital preservation at Wellcome.</p>

---

<h2>Read more</h2>

<p>Browse the catalogue: <a href="https://wellcomecollection.org/works">wellcomecollection.org/works</a></p><p>Get our code: <a href="https://github.com/wellcometrust/platform">github.com/wellcometrust/platform</a></p><p>Browse our developer docs, learn how to use our APIs: <a href="https://developers.wellcomecollection.org/">developers.wellcomecollection.org/</a></p>

---

<p><em>Thanks to Christy Henshaw, Jonathan Tweed and Tom Scott for their help reviewing drafts of this talk.</em></p>
