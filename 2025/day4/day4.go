package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"strings"
)

func main() {
	var ptFlag = flag.Int("pt", 2, "specify which aoc part you would like an answer to")
	flag.Parse()

	file, err := os.ReadFile("../input/day4.txt")
	if err != nil {
		log.Fatal(err)
	}

	grid := strings.Split(string(file), "\n")

	// Use 2D rune slice instead for 2D value assignment
	grid2 := make([][]rune, len(grid))
	for index, line := range grid {
		grid2[index] = []rune(line)
	}

	liftable := 0
	new, new_grid := naiveCheck(grid2)
	for new != 0 {
		liftable += new

		if *ptFlag == 1 {
			break
		}

		// Update grid and iterate over new grid for new rolls to remove
		copy(grid2, new_grid) // Used to update the grid by copying elements from new_grid into grid2
		fmt.Println("Found", new, "new rolls")
		new, new_grid = naiveCheck(grid2)
	}

	fmt.Println("Amount of liftable rolls:", liftable)
}

func naiveCheck(grid [][]rune) (int, [][]rune) {
	// Directional vectors to check 8 adjacent units
	dr := []int{0, 0, 1, 1, 1, -1, -1, -1}
	dc := []int{1, -1, 0, 1, -1, 0, 1, -1}

	liftable := 0

	for i, line := range grid {
		for j, c := range line {
			if c != '@' {
				continue
			}

			count := 0
			for index := range dr {
				ii := i + dr[index]
				jj := j + dc[index]
				if ii < 0 || ii >= len(grid) || jj < 0 || jj >= len(grid[0]) {
					continue
				}

				if grid[ii][jj] == '@' || grid[ii][jj] == 'x' {
					count++
				}
			}

			if count < 4 {
				liftable++
				grid[i][j] = 'x' // mark x removable for sweep later
			}
		}
	}

	// Sweep stage
	for i, line := range grid {
		for j, c := range line {
			if c == 'x' {
				grid[i][j] = '.'
			}
		}
	}

	for _, line := range grid {
		fmt.Println(string(line))
	}
	return liftable, grid
}
