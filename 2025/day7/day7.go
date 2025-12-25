package main

import (
	"fmt"
	"log"
	"os"
	"strings"

	. "github.com/jiasunzhu613/AdventOfCode/utils"
)

type Coordinate struct {
	row int
	col int
}

func main() {
	file, err := os.ReadFile("../input/day7.txt")
	if err != nil {
		log.Fatal(err)
	}

	lines := strings.Split(string(file), "\n")

	seen := NewSet[Coordinate]()
	memoTimelines := make(map[Coordinate]int)

	fmt.Println("=======SPLITS NOW=======")
	splits := countSplits(lines, seen, 0, strings.Index(lines[0], "S"))
	fmt.Println("Total number of beam splits:", splits)

	fmt.Println()

	fmt.Println("=======TIMELINES NOW=======")
	timelines := countTimelines(lines, memoTimelines, 0, strings.Index(lines[0], "S"))
	fmt.Println("Total number of timelines:", timelines)
}

func countSplits(lines []string, seen *Set[Coordinate], r int, c int) int {
	if r >= len(lines) || c < 0 || c >= len(lines[0]) {
		return 0
	}

	for ; r < len(lines); r++ {
		if lines[r][c] == '^' {
			// We specifically want to memoize the coordinates where we split
			if In(seen, Coordinate{row: r, col: c}) {
				return 0
			}

			AddItem(seen, Coordinate{row: r, col: c})

			return 1 + countSplits(lines, seen, r, c-1) + countSplits(lines, seen, r, c+1)
		}
	}

	return 0
}

func countTimelines(lines []string, memo map[Coordinate]int, r int, c int) int {
	if r >= len(lines) || c < 0 || c >= len(lines[0]) {
		return 0
	}

	for ; r < len(lines); r++ {
		if lines[r][c] == '^' {
			// We specifically want to memoize the coordinates where we split
			// Intuition behind memoization: we will treat each split point as a subproblem and think of it as if it were the starting point
			// From each split point, the number of timelines that can be generated will always be the same, so we can reuse for future upstream splits points
			value, ok := memo[Coordinate{row: r, col: c}]
			if ok {
				return value
			}

			result := countTimelines(lines, memo, r, c-1) + countTimelines(lines, memo, r, c+1)
			memo[Coordinate{row: r, col: c}] = result

			return result
		}
	}

	return 1
}
