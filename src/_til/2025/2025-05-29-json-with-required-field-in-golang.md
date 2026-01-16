---
layout: til
title: Parsing JSON in Go with a required field
date: 2025-05-29 17:14:31 +01:00
tags:
  - golang
  - json
---
I've been doing a bit of work with Go recently, in particular writing some code to parse JSON.
Here's an example program that demonstrates what I learnt, where I'm parsing a JSON string as an instance of a Go struct:

```go
package main

import (
	"encoding/json"
	"fmt"
)

func main() {
	parseJson(`{"number_of_sides": 5}`)
	parseJson(`{}`)
	parseJson(`<number_of_sides>5</number_of_sides>`)
}

func parseJson(jsonString string) {
	var shape Shape

	fmt.Printf("trying to parse: %s\n", jsonString)

	if err := json.Unmarshal([]byte(jsonString), &shape); err != nil {
		fmt.Println("cannot parse string as JSON that looks like `Shape`")
	} else if shape.Sides == nil {
		fmt.Println("JSON did not include a numeric `number_of_sides` field")
	} else {
		fmt.Printf("shape has %d sides\n", *shape.Sides)
	}

	fmt.Println("")
}

type Shape struct {
	Sides *int `json:"number_of_sides"`
}
```

The `json:` annotation is a Go feature called a "struct tag" which tells the JSON unmarshaller which JSON field to look at.

## Required fields in JSON

I want to know if the `number_of_sides` field is present with value `0` or missing.

Suppose I define my struct with an `int` field:

```go
type Shape struct {
	Sides int `json:"number_of_sides"`
}
```

When I parse a JSON object without `number_of_sides`, Go will create a struct `Shape{Sides: 0}` using the 0-value.

Suppose I define my struct with a pointer to an `int`:

```go
type Shape struct {
	Sides *int `json:"number_of_sides"`
}
```

When I parse a JSON object without `number_of_sides`, Go will create a struct `Shape{Sides: nil}` using the 0-value for a pointer.
I have to remember to get the pointer value later, not the pointer itself.
