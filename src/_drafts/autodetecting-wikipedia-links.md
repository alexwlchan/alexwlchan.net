---
layout: post
title: Links to Wikipedia can be hard to autodetect
summary:
tags:
  - wikipedia
---
Last year I built

trailing period

'<a href="https://en.wikipedia.org/wiki/William_Barnes_Jr" '
'rel="noreferrer nofollow">en.wikipedia.org/wiki/William_Barnes_Jr</a>.'

disambiguation params

comment_text = 'This guy! <a href="https://en.wikipedia.org/wiki/Reg_Dixon_" rel="noreferrer nofollow">en.wikipedia.org/wiki/Reg_Dixon_</a>(comedian)'
expected_text = 'This guy! <a href="https://en.wikipedia.org/wiki/Reg_Dixon_(comedian)" rel="noreferrer nofollow">en.wikipedia.org/wiki/Reg_Dixon_(comedian)</a>'

includes all wikipedia.org links, e.g. m.wikipedia.org

comment_text = '<a href="http://en.m.wikipedia.org/wiki/Black_Thursday_" rel="nofollow">en.m.wikipedia.org/wiki/Black_Thursday_</a>(1851)'
expected_text = '<a href="http://en.m.wikipedia.org/wiki/Black_Thursday_(1851)" rel="noreferrer nofollow">en.m.wikipedia.org/wiki/Black_Thursday_(1851)</a>'

or dutch wikipedia

comment_text = (
"Ship was until 1934 in use and afterwards scrapped.\n"
"see for total history\n"
'<a href="https://nl.wikipedia.org/wiki/Mauretania_" rel="noreferrer nofollow">nl.wikipedia.org/wiki/Mauretania_</a>(schip,_1907)'
)
expected_text = (
"Ship was until 1934 in use and afterwards scrapped.\n"
"see for total history\n"
'<a href="https://nl.wikipedia.org/wiki/Mauretania_(schip,_1907)" rel="noreferrer nofollow">nl.wikipedia.org/wiki/Mauretania_(schip,_1907)</a>'
)

and fragments

comment_text = (
"In\n"
'<a href="http://es.wikipedia.org/wiki/Atoyac_" rel="nofollow">es.wikipedia.org/wiki/Atoyac_</a>(Veracruz)#Toponimia\n'
"you'll find its coordinates"
)
expected_text = (
"In\n"
'<a href="http://es.wikipedia.org/wiki/Atoyac_(Veracruz)#Toponimia" rel="noreferrer nofollow">es.wikipedia.org/wiki/Atoyac_(Veracruz)#Toponimia</a>\n'
"you'll find its coordinates"
)

also wikimedia commons

# This example comes from Peter D. Tillman's comment:
# https://www.flickr.com/photos/aahs_archives/23586820864/#comment72157667048114519
#
# Retrieved 22 January 2025
comment_text = (
'In use at <a href="https://en.wikipedia.org/wiki/Bell_YFM-1_Airacuda" rel="nofollow">en.wikipedia.org/wiki/Bell_YFM-1_Airacuda</a>\n'
"From SDASM, Daniels collection:\n"
'<a href="https://commons.wikimedia.org/wiki/File:Airacuda_Bell_XFM-1_" rel="nofollow">commons.wikimedia.org/wiki/File:Airacuda_Bell_XFM-1_</a>(15954491367).jpg\n'
"Thanks for posting these!"
)
expected_text = (
'In use at <a href="https://en.wikipedia.org/wiki/Bell_YFM-1_Airacuda" rel="nofollow">en.wikipedia.org/wiki/Bell_YFM-1_Airacuda</a>\n'
"From SDASM, Daniels collection:\n"
'<a href="https://commons.wikimedia.org/wiki/File:Airacuda_Bell_XFM-1_(15954491367).jpg" rel="noreferrer nofollow">commons.wikimedia.org/wiki/File:Airacuda_Bell_XFM-1_(15954491367).jpg</a>\n'
"Thanks for posting these!"
)

but puncutation isn't always aprt of the URL!

(
    '<a href="https://en.wikipedia.org/wiki/Flickr" '
    'rel="noreferrer nofollow">en.wikipedia.org/wiki/Flickr</a>.'
)