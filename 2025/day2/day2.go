package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

func main() {
	// Declare and parse flag for identifying whether we are trying to get output for pt1 or pt2
	var ptFlag = flag.Int("pt", 2, "specify which aoc 'part' you would like output for")
	flag.Parse()

	file, err := os.ReadFile("../input/day2.txt")
	if err != nil {
		log.Fatal(err)
	}

	productRanges := strings.Split(string(file), ",")

	total := 0
	for _, ranges := range productRanges {
		start, end := convertRanges(ranges)
		for ; start <= end; start++ {
			s_start := strconv.Itoa(start)
			if *ptFlag == 1 && isDoubled(s_start) {
				total += start
			}

			if *ptFlag == 2 && isRepeated(s_start) {
				total += start
			}
		}
	}

	fmt.Printf("Total sum of invalid ids in part %d is: %d\n", *ptFlag, total)
}

func convertRanges(productIdRange string) (int, int) {
	ranges := strings.Split(productIdRange, "-")
	if len(ranges) != 2 {
		panic("Length of product id range is not 2")
	}

	start, err := strconv.Atoi(ranges[0])
	if err != nil {
		log.Fatal(err)
	}

	end, err := strconv.Atoi(ranges[1])
	if err != nil {
		log.Fatal(err)
	}

	return start, end
}

func isDoubled(id string) bool {
	// Odd lengthed strings can never be doubled
	if len(id) & 1 == 1 {
		return false
	}

	mid := len(id) / 2
	return id[:mid] == id[mid:]
}

func isRepeated(id string) bool {
	mid := len(id) / 2
	for i := 1; i <= mid; i++ {
		// If the current subsection we are testing for repeatability is not divisible, then ignore!
		if len(id) % i != 0 {
			continue
		}

		segment := id[:i]
		works := true
		for j := i; j < len(id); j += i {
			if id[j: j + i] != segment {
				works = false
				break
			}
		}

		if works {
			return true
		}
	}

	return false
}