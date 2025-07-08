// See https://github.com/alexwlchan/rainbow-hearts/blob/main/flags.py
const FLAGS = {
  "rainbow": {
    "stripes": [
      "#FF5D7D",
      "#FF764E",
      "#FFC144",
      "#88DF8E",
      "#00CCF2",
      "#B278D3"
    ],
    "url": "https://en.wikipedia.org/wiki/Rainbow_flag_(LGBT_movement)"
  },
  "asexual": {
    "stripes": [
      "#141414",
      "#969696",
      "#c4c4c4",
      "#870788"
    ],
    "url": "https://en.wikipedia.org/wiki/Asexuality"
  },
  "agender": {
    "stripes": [
      "#141414",
      "#a9b0b2",
      "#a9b0b2",
      "#dfdfdf",
      "#dfdfdf",
      "#a6d87b",
      "#a6d87b",
      "#dfdfdf",
      "#dfdfdf",
      "#a9b0b2",
      "#a9b0b2",
      "#141414"
    ],
    "url": "https://en.wikipedia.org/wiki/Agender"
  },
  "aromantic": {
    "stripes": [
      "#3e9b44",
      "#9abe72",
      "#dfdfdf",
      "#9b9b9b",
      "#141414"
    ],
    "url": "https://en.wikipedia.org/wiki/Romantic_orientation#Aromanticism"
  },
  "bear": {
    "stripes": [
      "#613406",
      "#be500e",
      "#e0c252",
      "#dec89d",
      "#d2d2d2",
      "#484848",
      "#141414"
    ],
    "url": "https://en.wikipedia.org/wiki/Bear_flag_(gay_culture)"
  },
  "lazy bisexual boy": {
    "stripes": [
      "#ca0a6d",
      "#ca0a6d",
      "#704e90"
    ],
    "url": "https://twitter.com/freezydorito/status/1152168216120221697"
  },
  "lazy bisexual girl": {
    "stripes": [
      "#704e90",
      "#0838a7",
      "#0838a7"
    ],
    "url": "https://twitter.com/freezydorito/status/1152168216120221697"
  },
  "bi": {
    "stripes": [
      "#ca0a6d",
      "#ca0a6d",
      "#704e90",
      "#0838a7",
      "#0838a7"
    ],
    "url": "https://en.wikipedia.org/wiki/Bisexuality"
  },
  "genderfluid": {
    "stripes": [
      "#e07096",
      "#e0e0e0",
      "#a117b5",
      "#141414",
      "#353fb1"
    ],
    "url": "https://en.wikipedia.org/wiki/Genderfluid"
  },
  "genderqueer": {
    "stripes": [
      "#a78dc5",
      "#dfdfdf",
      "#69883e"
    ],
    "url": "https://en.wikipedia.org/wiki/Genderqueer"
  },
  "non-binary": {
    "stripes": [
      "#e2d938",
      "#dfdfdf",
      "#8d57bc",
      "#383838"
    ],
    "url": "https://en.wikipedia.org/wiki/Non-binary_gender"
  },
  "pansexual": {
    "stripes": [
      "#e70c86",
      "#e7c60c",
      "#0ca6e7"
    ],
    "url": "https://en.wikipedia.org/wiki/Pansexuality"
  },
  "philly": {
    "stripes": [
      "#141414",
      "#7d541e",
      "#d30e0b",
      "#e7840c",
      "#e7d80c",
      "#07882d",
      "#114fe7",
      "#790d8b"
    ],
    "url": "https://en.wikipedia.org/wiki/LGBT_symbols#cite_ref-Philadelphia_93-0",
    "label": "Philly\u2019s pride flag"
  },
  "polysexual": {
    "stripes": [
      "#df23aa",
      "#11c667",
      "#2488de"
    ],
    "url": "https://rationalwiki.org/wiki/Polysexuality"
  },
  // Renamed after I realised the polyamory and polysexual flags are separate.
  // See https://github.com/queerjs/website/issues/59
  "poly": {
    "name": "polysexual",
    "stripes": [
      "#df23aa",
      "#11c667",
      "#2488de"
    ],
    "url": "https://rationalwiki.org/wiki/Polysexuality"
  },
  "trans": {
    "stripes": [
      "#55CDFC",
      "#F7A8B8",
      "#DDD",
      "#F7A8B8",
      "#55CDFC"
    ],
    "url": "https://en.wikipedia.org/wiki/Transgender_flags"
  },
  "black trans": {
    "stripes": [
      "#55CDFC",
      "#F7A8B8",
      "#383838",
      "#F7A8B8",
      "#55CDFC"
    ],
    "url": "https://en.wikipedia.org/wiki/File:Black_trans_flag.svg"
  },
  "lesbian": {
    "stripes": [
      "#B60063",
      "#C84896",
      "#E253AB",
      "#DDD",
      "#F0A7D2",
      "#D73F4F",
      "#990200"
    ],
    "url": "https://en.wikipedia.org/wiki/LGBT_symbols#Lesbianism"
  },
  "leather": {
    "stripes": [
      "#141414",
      "#141414",
      "#141414",
      "#141414",
      "#0909b7",
      "#0909b7",
      "#0909b7",
      "#0909b7",
      "#e40c11",
      "#141414",
      "#141414",
      "#141414",
      "#141414",
      "#0909b7",
      "#0909b7",
      "#0909b7",
      "#0909b7",
      "#d2d2d2",
      "#d2d2d2",
      "#d2d2d2",
      "#d2d2d2",
      "#0909b7",
      "#0909b7",
      "#0909b7",
      "#0909b7",
      "#141414",
      "#141414",
      "#141414",
      "#141414",
      "#0909b7",
      "#0909b7",
      "#0909b7",
      "#0909b7",
      "#141414",
      "#141414",
      "#141414",
      "#141414"
    ],
    "url": "https://en.wikipedia.org/wiki/Leather_Pride_flag"
  }
};

// Returns the ID of a random flag
function randomFlagId() {
  const choices = Object.keys(FLAGS);
  const index = Math.floor(Math.random() * choices.length);
  return choices[index];
}

function OuterStripes(stripes, { strokeWidth }) {
  const selectedStripes = stripes.slice(0, Math.floor(stripes.length / 2));
  
  return selectedStripes.map((stripe, index) => `
    <!-- ${stripe} / ${index} -->
    <use
      x="5"
      y="-960"
      xlink:href="#heart"
      stroke="${stripe}"
      stroke-width="${strokeWidth / 2 - (index / stripes.length) * strokeWidth}"
      stroke-linecap="round"
      fill="none"/>
  `).join("");
}

function InnerStripes(stripes, { strokeWidth }) {
  const selectedStripes =
    stripes.length % 2 === 0
      ? stripes.slice(Math.floor(stripes.length / 2), stripes.length)
      : stripes.slice(Math.floor(stripes.length / 2) + 1, stripes.length);
      
  return selectedStripes.reverse().map((stripe, index) => `
    <!-- ${stripe} / ${index} -->
    <use
      x="5"
      y="-960"
      xlink:href="#heart"
      stroke="${stripe}"
      stroke-width="${strokeWidth / 2 - (index / stripes.length) * strokeWidth}"
      stroke-linecap="round"
      fill="none"/>
  `).join("");
}

function MiddleStripe(stripes, { strokeWidth }) {
  if (stripes.length % 2 === 0) {
    return '';
  }
  
  const thisStripe = stripes[Math.floor(stripes.length / 2)];
  
  return `
      <!-- ${thisStripe} -->
      <use
        x="5"
        y="-960"
        xlink:href="#heart"
        stroke="${thisStripe}"
        stroke-width="${strokeWidth / stripes.length / 2}"
        stroke-linecap="round"
        fill="none"/>
  `;
}

function renderHeart({ leftFlagId, leftFlag }, { rightFlagId, rightFlag }, { strokeWidth }) {
  return `
    <svg viewBox="0 0 1100, 660" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <!-- Based on the heart from https://thenounproject.com/search/?q=heart&i=585522 -->
        <path id="heart" d="m 31,963.375 c -14.986319,0 -25,12.30467 -25,26 0,12.8493 7.296975,23.9547 16.21875,32.7188 8.921775,8.764 19.568704,15.2612 26.875,19.0312 a 2.0002,2.0002 0 0 0 1.8125,0 c 7.306296,-3.77 17.953225,-10.2672 26.875,-19.0312 C 86.703025,1013.3297 94,1002.2243 94,989.375 c 0,-13.69533 -10.013684,-26 -25,-26 -8.834204,0 -14.702885,4.50444 -19,10.59375 C 45.702885,967.87944 39.834204,963.375 31,963.375 z"/>

        <!-- This mask clips out the region where the left heart overlaps the right heart -->
        <mask id="exclude-left-heart-overlap">
          <rect x="0" y="0" width="1440" height="800" fill="white"/>
          <g transform="translate(100 110) scale(5.4) rotate(-10 30 30)">
            <use x="5" y="-960" xlink:href="#heart" stroke="black" stroke-width="16" fill="white"/>
          </g>
          <rect x="0" y="330" width="1440" height="330" fill="white"/>
        </mask>

        <!-- This mask only allows stuff *inside* the left-hand heart -->
        <mask id="left-heart-inside-only">
          <rect x="0" y="0" width="1440" height="800" fill="black"/>
          <g transform="translate(100 110) scale(5.4) rotate(-10 30 30)">
            <use x="5" y="-960" xlink:href="#heart" stroke="none" fill="white"/>
          </g>
        </mask>

        <!-- This mask clips out the region where the right heart overlaps the left heart -->
        <mask id="exclude-right-heart-overlap">
          <rect x="0" y="0" width="1440" height="800" fill="white"/>
          <g transform="translate(470 145) scale(5) rotate(10 30 30)">
             <use x="5" y="-960" xlink:href="#heart" stroke="black" stroke-width="15.14" fill="white"/>
           </g>
          <rect x="0" y="0" width="1440" height="330" fill="white"/>
        </mask>

        <!-- This mask only allows stuff *inside* the right-hand heart -->
        <mask id="right-heart-inside-only">
          <rect x="0" y="0" width="1440" height="800" fill="black"/>
          <g transform="translate(470 145) scale(5) rotate(10 30 30)">
             <use x="5" y="-960" xlink:href="#heart" stroke="none" fill="white"/>
           </g>
        </mask>
      </defs>

      <!-- Flag: ${leftFlagId} -->
      <svg mask="url(#exclude-right-heart-overlap)">
        <g transform="translate(100 110) scale(5.4) rotate(-10 30 30)">          
          ${OuterStripes(leftFlag.stripes, { strokeWidth })}
        </g>

        <svg mask="url(#left-heart-inside-only)">
          {% set ns = namespace(inner_stroke_width=stroke_width / 2) %}

          <g transform="translate(100 110) scale(5.4) rotate(-10 30 30)">
            ${InnerStripes(leftFlag.stripes, { strokeWidth })}
          </g>
        </svg>

        <g transform="translate(100 110) scale(5.4) rotate(-10 30 30)">\
          ${MiddleStripe(leftFlag.stripes, { strokeWidth })}
        </g>
      </svg>

      {%- set (label, stripe_data) = right_flag -%}
      {%- set stripes = stripe_data.stripes -%}

      <!-- Flag: ${rightFlagId} -->

      <svg mask="url(#exclude-left-heart-overlap)">
        <g transform="translate(470 145) scale(5) rotate(10 30 30)">
          ${OuterStripes(rightFlag.stripes, { strokeWidth })}
        </g>

        <svg mask="url(#right-heart-inside-only)">
          <g transform="translate(470 145) scale(5) rotate(10 30 30)">
            ${InnerStripes(rightFlag.stripes, { strokeWidth })}
          </g>
        </svg>

        <g transform="translate(470 145) scale(5) rotate(10 30 30)">
          ${MiddleStripe(rightFlag.stripes, { strokeWidth })}
        </g>
      </svg>
    </svg>
  `.trim();
}
