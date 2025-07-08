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

function renderValknuts(flagId1, flagId2, flagId3, { strokeWidth }) {
  const stripe1 = FLAGS[flagId1].stripes;
  const stripe2 = FLAGS[flagId2].stripes;
  const stripe3 = FLAGS[flagId3].stripes;
  
  var lines = [
    '<svg viewBox="0 0 900, 550" xmlns="http://www.w3.org/2000/svg">'
  ];
  
  const hasBlack = stripe1.includes("#000000") || stripe2.includes("#000000") || stripe3.includes("#000000");
  const background = hasBlack ? "#222222" : "black";
  lines.push(`<polygon points="0,0 900,0 900,600 0,600" fill="${background}"/>`);
  
  // Centre the valknut on the page by trial and error
  lines.push('<g transform="translate(229 450)">');
  
  const barWidth = 50;
  const gapWidth = 10;
  
  lines.push(drawValknut(stripe1, { barWidth, gapWidth }));
  
  const center = positionXY({
    x: 2 * barWidth + 5 / 3 * gapWidth,
    y: 3 * barWidth + 8 / 3 * gapWidth,
  });
  
  lines.push(`<g transform="rotate(120 ${center})">`);
  lines.push(drawValknut(stripe2, { barWidth, gapWidth }));
  lines.push("</g>");
  
  lines.push(`<g transform="rotate(240 ${center})">`);
  lines.push(drawValknut(stripe3, { barWidth, gapWidth }));
  lines.push("</g>");
  
  lines.push("</g>");
  
  lines.push(`
      <text x="450" y="512" fill="white" font-size="1.7em" text-anchor="middle"
      font-family="Arial Narrow, Arial, sans-serif">
      YOUR COWARDLY BIGOTRY IS AN AFFRONT TO THE ALLFATHER</text>
  `)

  lines.push('</svg>')
  
  return lines.join("");
}

function radians(degrees) {
  return degrees * Math.PI / 180;
}

function positionXY({ x, y }) {
  const xCoord = x + y * Math.cos(radians(60));
  const yCoord = -y * Math.sin(radians(60));
  
  return `${xCoord},${yCoord}`;
}

function getValknutTriCoordinates({ barWidth, gapWidth, stripeCount, stripeStart, stripeEnd }) {
  // Coordinate axes
  //
  //              (0, t2)
  //             /
  //            /
  //           +------> (t1, 0)
  //
  // The shape to be drawn is defined as follows:
  //
  //                                 (0, 6B+5W)
  //                                      /\
  //
  //                                 (B, 4B+5W)
  //                                      /\
  //
  //                    ..    ..                          ..   ..
  //                   /     /                              \    \
  //                  /     /                                \    \
  //      (0, 3B+3W) +-----+ (B, 3B+3W)        (2B+2W, 3B+3W) +----+ (3B+2W, 3B+3W)
  //
  //     (0, 2B+W) +-----+ (B, 2B+W)              (3B+4W, 2B+W) +-----+ (4B+4W, 2B+W)
  //              /     /                                        \     \
  //             /     /                                          \     \
  //            /     +--------------------------------------------+     \
  //           /  (B, B)                                      (4B+5W, B)  \
  //          /                                                            \
  //  (0, 0) +--------------------------------------------------------------+ (6B+5W, 0)
  //
  // But then we need to adjust for the part of the stripe we're drawing.
  //
  const lowerStripe = (stripeStart - 1) / stripeCount;
  const upperStripe = stripeEnd / stripeCount;
  
  const coordinatesLower = [
    {
      x: lowerStripe * barWidth,
      y: lowerStripe * barWidth,
    },
    {
      x: 6 * barWidth + 5 * gapWidth - lowerStripe * (2 * barWidth),
      y: lowerStripe * barWidth,
    },
    {
      x: 4 * barWidth + 4 * gapWidth - lowerStripe * barWidth,
      y: 2 * barWidth + gapWidth,
    },
    {
      x: 4 * barWidth + 4 * gapWidth - upperStripe * barWidth,
      y: 2 * barWidth + gapWidth,
    },
    {
      x: 6 * barWidth + 5 * gapWidth - upperStripe * (2 * barWidth),
      y: upperStripe * barWidth,
    },
    {
      x: upperStripe * barWidth,
      y: upperStripe * barWidth
    },
    {
      x: upperStripe * barWidth,
      y: 2 * barWidth + gapWidth
    },
    {
      x: lowerStripe * barWidth,
      y: 2 * barWidth + gapWidth
    },
  ];
  
  const coordinatesUpper = [
    {
      x: lowerStripe * barWidth,
      y: 3 * barWidth + 3 * gapWidth},
    {
      x: upperStripe * barWidth,
      y: 3 * barWidth + 3 * gapWidth
    },
    {
      x: upperStripe * barWidth,
      y: 6 * barWidth + 5 * gapWidth - upperStripe * (2 * barWidth),
    },
    {
      x: 3 * barWidth + 2 * gapWidth - upperStripe * barWidth,
      y: 3 * barWidth + 3 * gapWidth
    },
    {
      x: 3 * barWidth + 2 * gapWidth - lowerStripe * barWidth,
      y: 3 * barWidth + 3 * gapWidth
    },
    {
      x: lowerStripe * barWidth,
      y: 6 * barWidth + 5 * gapWidth - lowerStripe * (2 * barWidth),
    },
  ];
  
  return { coordinatesLower, coordinatesUpper };
}
  
function drawValknut(stripes, { barWidth, gapWidth }) {
  var lines = [];
  
  stripes.forEach((fillColor, index) => {
    const stripeStart = index + 1;
    const stripeEnd =
      stripes[index] === fillColor
        ? index + 1
        : index;
    
    const { coordinatesLower, coordinatesUpper } = getValknutTriCoordinates({
      barWidth, gapWidth, stripeCount: stripes.length, stripeStart, stripeEnd
    });
    
    lines.push(
      `<polygon points="${coordinatesLower.map(positionXY).join(' ')}" fill="${fillColor}"/>`
    );
    lines.push(
      `<polygon points="${coordinatesUpper.map(positionXY).join(' ')}" fill="${fillColor}"/>`
    )
  });
  
  return lines.join("\n");
}