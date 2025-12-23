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
	var ptFlag = flag.Int("pt", 2, "specify aoc part you would like an answer to")
	flag.Parse()

	file, err := os.ReadFile("../input/day6.txt")
	if err != nil {
		log.Fatal(err)
	}

	rawLines := strings.Split(string(file), "\n")

	lines := make([][]string, 0)
	for _, line := range strings.Split(string(file), "\n") {
		lines = append(lines, normalizedStringFields(line))
	}

	total := 0
	startCounter := 0
	for c := range lines[0] {
		var values []int
		if *ptFlag == 1 {
			values = normalProcessValues(lines, c)
		} else {
			lengthToNext := findLengthToNext(rawLines[len(rawLines)-1], startCounter)
			values = cephalopodProcessValues(rawLines, startCounter, startCounter+lengthToNext-1)
			startCounter += lengthToNext
		}

		fmt.Println(values)
		operator := lines[len(lines)-1][c]
		switch operator {
		case "*":
			total += product(values)
		case "+":
			total += sum(values)
		}
	}

	fmt.Println("Total value:", total)
}

func normalizedStringFields(s string) []string {
	return strings.Fields(strings.TrimSpace(s))
}

func product(arr []int) int {
	result := 1
	for _, val := range arr {
		result *= val
	}

	return result
}

func sum(arr []int) int {
	result := 0
	for _, val := range arr {
		result += val
	}

	return result
}

func normalProcessValues(lines [][]string, c int) []int {
	values := make([]int, 0)
	for r := 0; r < len(lines)-1; r++ {
		value, _ := strconv.Atoi(lines[r][c])
		values = append(values, value)
	}

	return values
}

func findLengthToNext(lastLine string, start int) int {
	count := 1
	start++

	for lastLine[start] == ' ' {
		count++
		start++
		if start == len(lastLine) {
			break
		}
	}

	if start == len(lastLine) {
		count++
	}

	return count
}

func cephalopodProcessValues(lines []string, start int, end int) []int {
	cephalopod := make([]int, 0)
	for i := 0; i < end-start; i++ {
		value := 0
		for r := 0; r < len(lines)-1; r++ {
			// Modify new value
			if lines[r][start+i] == ' ' {
				continue
			}

			v := lines[r][start+i] - '0'
			if v != 0 {
				value *= 10
			}
			value += int(v)
		}

		cephalopod = append(cephalopod, value)
	}

	return cephalopod
}
