package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

// NP-complete problem LOL
// https://en.wikipedia.org/wiki/Bin_packing_problem

const (
	EPISLON = 10 // Make a reasonable assumption for epsilon
)

type Present struct {
	grid []string
	area int
}

func main() {
	file, err := os.ReadFile("../input/day12.txt")
	if err != nil {
		log.Fatal(err)
	}

	splitted := strings.Split(string(file), "\n\n")

	presents := parsePresents(splitted[:6])	
	possibleByEpsilon := 0

	for _, line := range strings.Split(splitted[len(splitted) - 1], "\n") {
		splitLine := strings.Split(line, ": ")

		// Get dim
		dimString := strings.Split(splitLine[0], "x")
		width, _ := strconv.Atoi(dimString[0])
		length, _ := strconv.Atoi(dimString[1])
		dim := width * length

		// Requirements
		reqs := strings.Split(splitLine[1], " ")
		areaNeeded := 0
		for ind, req := range reqs {
			reqInt, _ := strconv.Atoi(req)

			areaNeeded += presents[ind].area * reqInt
		}

		if dim - areaNeeded > 10 {
			possibleByEpsilon++
		}
	}

	fmt.Println("Potentially possible based on current epsilon:", possibleByEpsilon)
}

func parsePresents(input []string) []Present {
	presents := make([]Present, 0)

	for _, present := range input {
		lines := strings.Split(present, "\n")

		// Ignore line 0
		lines = lines[1:]
		area := 0 
		for _, line := range lines {
			for _, c := range line {
				if c == '#' {
					area++
				}
			}
		}

		presents = append(presents, Present{lines, area})
	}

	return presents
}