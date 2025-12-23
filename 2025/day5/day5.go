package main

import (
	"fmt"
	"log"
	"os"
	"sort"
	"strconv"
	"strings"
)

type Range struct {
	start int
	stop  int
}

func main() {
	file, err := os.ReadFile("../input/day5.txt")
	if err != nil {
		log.Fatal(err)
	}

	// Get both parts of the input first
	sections := strings.Split(string(file), "\n\n")

	// Process Ranges
	inputRanges := strings.Split(sections[0], "\n")
	ranges := make([]Range, len(inputRanges))

	for index, inputRange := range inputRanges {
		stringRange := strings.Split(inputRange, "-")
		start, _ := strconv.Atoi(stringRange[0])
		stop, _ := strconv.Atoi(stringRange[1])

		ranges[index] = Range{start: start, stop: stop}
	}

	// Find cumulative disjoint ranges

	disjointRanges := findCumulativeDisjointRanges(ranges)
	fmt.Println(disjointRanges)

	totalPossibleFresh := 0
	for _, disjointRange := range disjointRanges {
		totalPossibleFresh += disjointRange.stop - disjointRange.start + 1
	}

	fmt.Println("Total number of possible fresh ingredients:", totalPossibleFresh)

	// Process values
	total := 0
	for _, s := range strings.Split(sections[1], "\n") {
		value, _ := strconv.Atoi(s)
		total += checkSpoiled(ranges, value)
	}
	fmt.Println("Total number of fresh:", total)
}

func findCumulativeDisjointRanges(ranges []Range) []Range {
	// Sort ranges slice
	sort.Slice(ranges, func(i, j int) bool {
		return ranges[i].start < ranges[j].start
	})

	fmt.Println(ranges)

	// We will store every disjoin range as a pair of values, corresponded by index
	// start[i] => stop[i], so on
	disjointRanges := make([]Range, 1)

	// for each range, it is either the start of a new disjoint range or it continue from the previous one
	for _, _range := range ranges {
		lastRange := disjointRanges[len(disjointRanges)-1]
		lastStart, lastStop := lastRange.start, lastRange.stop

		if lastStart <= _range.start && _range.stop <= lastStop {
			continue
		}

		// case 1: it joins previous range
		if lastStart <= _range.start && _range.start <= lastStop && lastStop <= _range.stop {
			disjointRanges[len(disjointRanges)-1].stop = _range.stop
		} else {
			disjointRanges = append(disjointRanges, _range)
		}
	}

	return disjointRanges[1:]
}

func checkSpoiled(ranges []Range, value int) int {
	for _, _range := range ranges {
		if _range.start <= value && value <= _range.stop {
			return 1
		}
	}

	return 0
}
