package main

// Resource for 2D prefix sum table: https://en.wikipedia.org/wiki/Summed-area_table
// Resource for 2D Coordinate compression: https://codeforces.com/blog/entry/14457

import (
	"fmt"
	"log"
	"math"
	"os"
	"sort"
	"strconv"
	"strings"
)

type Coordinate struct {
	x int
	y int
}

type Pair[T comparable] struct { a, b T }

type Set[T comparable] struct {
	m map[T]struct{}
}

// Make new set with input values if any (uses variadics)
// Empty struct uses 0 memory
func newSet[T comparable](items ...T) *Set[T] {
	s := &Set[T] {
		m: make(map[T]struct{}),
	}

	for _, item := range items {
		s.m[item] = struct{}{} // second set of braces is for construction of the empty struct
	}

	return s
}

func addItem[T comparable](set *Set[T], item T) {
	_, ok := set.m[item]

	// If already in set, we dont care anymore
	if ok {
		return
	}

	set.m[item] = struct{}{}
}

func in[T comparable](set *Set[T], item T) bool{
	_, ok := set.m[item]

	return ok
}

// in order for the rectangle to be valid, there should not be any red cells within the rectangle
// there can be red cells on the corner or border but not within the rectangle

func main() {
	file, err := os.ReadFile("../../input/day9.txt")
	if err != nil {
		log.Fatal(err)
	}
	
	lines := strings.Split(string(file), "\n")
	
	coordinates := make([]Coordinate, 0)
	xCoordinates := make([]int, 0)
	xSet := newSet[int]()
	yCoordinates := make([]int, 0)
	ySet := newSet[int]()
	for _, line := range lines {
		x, y := processLine(line)
		coordinates = append(coordinates, Coordinate{x, y})
		
		if !in(xSet, x) {
			xCoordinates = append(xCoordinates, x)
			addItem(xSet, x)
		}

		if !in(ySet, y) {
			yCoordinates = append(yCoordinates, y)
			addItem(ySet, y)
		}
	}


	sort.Ints(xCoordinates)
	sort.Ints(yCoordinates)

	xCompression := 1
	xMapping := make(map[int]int)
	yCompression := 1
	yMapping := make(map[int]int)

	// Int arrays to match how much weight each col/row has in the compressed grid
	xWeights := make([]int, 0)
	yWeights := make([]int, 0)

	// START: Create coordinate compression mapping for x
	for i := 0; i < len(xCoordinates) - 1; i++ {
		_, ok := xMapping[xCoordinates[i]]
		
		if ok {
			continue
		}

		// Add to mapping
		xMapping[xCoordinates[i]] = xCompression

		// Increment compression counter
		diff := xCoordinates[i + 1] - xCoordinates[i]
		if diff >= 2 {
			xCompression += 2
		} else {
			xCompression++
		}
	}
	xMapping[xCoordinates[len(xCoordinates) - 1]] = xCompression
	// END: Create coordinate compression mapping for x

	// START: Add weights for x
	xWeights = append(xWeights, xCoordinates[0])
	xWeights = append(xWeights, 1)
	for i := 1; i < len(xCoordinates); i++ {
		// Increment compression counter
		diff := xCoordinates[i] - xCoordinates[i - 1]
		if diff >= 2 {
			xWeights = append(xWeights, diff)
			xWeights = append(xWeights, 1)
		} else {
			xWeights = append(xWeights, 1)
		}
	}
	// END: add weights for x

	for i := 0; i < len(yCoordinates) - 1; i++ {
		_, ok := yMapping[yCoordinates[i]]
		
		if ok {
			continue
		}

		// Add to mapping
		yMapping[yCoordinates[i]] = yCompression

		// Increment compression counter
		diff := yCoordinates[i + 1] - yCoordinates[i]
		if diff >= 2 {
			yCompression += 2
		} else {
			yCompression++
		}
	}
	yMapping[yCoordinates[len(yCoordinates) - 1]] = yCompression

	// START: Add weights for y
	yWeights = append(yWeights, yCoordinates[0])
	yWeights = append(yWeights, 1)
	for i := 1; i < len(yCoordinates); i++ {
		// Increment compression counter
		diff := yCoordinates[i] - yCoordinates[i - 1]
		if diff >= 2 {
			yWeights = append(yWeights, diff)
			yWeights = append(yWeights, 1)
		} else {
			yWeights = append(yWeights, 1)
		}
	}
	// END: add weights for y

	compressedCoordinates := make([]Coordinate, 0)
	for _, coordinate := range coordinates {
		x, y := coordinate.x, coordinate.y
		compressedCoordinates = append(compressedCoordinates, Coordinate{xMapping[x], yMapping[y]})
	}

	edges := newSet[Coordinate]()

	// Find all edges in compressed grid
	for i := 0; i < len(compressedCoordinates); i++ {
		prevI := mod(i - 1, len(compressedCoordinates))

		x, y := compressedCoordinates[i].x, compressedCoordinates[i].y
		xx, yy := compressedCoordinates[prevI].x, compressedCoordinates[prevI].y

		// on same x axis
		if x == xx {
			for i := min(y, yy); i <= max(y, yy); i++ {
				addItem(edges, Coordinate{x, i})
			}
		} else { // on same y axis 
			for i := min(x, xx); i <= max(x, xx); i++ {
				addItem(edges, Coordinate{i, y})
			}
		}
	}

	// Flood fill grid that is outside of the shape, mark each value with a 1
	// (0, 0) should never be a filled slot, so we start here

	// Build raw grid for flood fill marking
	X, Y := xCompression + 1, yCompression + 1
	grid := make([][]int, Y)
	for i := 0; i < len(grid); i++ {
		grid[i] = make([]int, X)
	}

	dx := []int{0, 1, -1, 0}
	dy := []int{1, 0, 0, -1}
	FloodFill(edges, &grid, newSet[Coordinate](), dx, dy, X, Y, Coordinate{0, 0})
	FloodFill(edges, &grid, newSet[Coordinate](), dx, dy, X, Y, Coordinate{X - 1, 0})
	FloodFill(edges, &grid, newSet[Coordinate](), dx, dy, X, Y, Coordinate{0, Y - 1})
	FloodFill(edges, &grid, newSet[Coordinate](), dx, dy, X, Y, Coordinate{X - 1, Y - 1})

	// DEBUGGING
	// for _, line := range grid {
	// 	fmt.Println(line)
	// }

	// Generate sum table
	table := GenerateSumTable(grid)

	validPairs := findValidCoordinatePairs(compressedCoordinates, table)

	largestRectangle := naiveFindLargestRectangle(coordinates, validPairs)

	fmt.Println("Largest rectangle is:", largestRectangle)
}

func processLine(line string) (int, int) {
	splitted := strings.Split(line, ",")

	x, _ := strconv.Atoi(splitted[0])
	y, _ := strconv.Atoi(splitted[1])

	return x, y
}

func getArea(c1, c2 Coordinate) int {
	return int((math.Abs(float64(c1.x - c2.x)) + 1) * (math.Abs(float64(c1.y - c2.y)) + 1))
}

func findValidCoordinatePairs(coordinates []Coordinate, table [][]int) []Pair[int] {
	pairs := make([]Pair[int], 0)
	
	for i := 0; i < len(coordinates); i++ {
		for j := i + 1; j < len(coordinates); j++ {
			query := QueryTable(table, coordinates[i], coordinates[j])
			if query == 0 {
				pairs = append(pairs, Pair[int]{i, j})
			}
		}
	}

	return pairs
}

func QueryTable(table [][]int, c1, c2 Coordinate) int {
	// This function does not cover edge cases because they will 
	// not happen with AOC input but beware of using this function on all cases
	boundMin := Coordinate{min(c1.x, c2.x) - 1, min(c1.y, c2.y) - 1}
	boundMax := Coordinate{max(c1.x, c2.x), max(c1.y, c2.y)}
	
	return table[boundMin.y][boundMin.x] + table[boundMax.y][boundMax.x] - 
			(table[boundMin.y][boundMax.x] + table[boundMax.y][boundMin.x])
}

func naiveFindLargestRectangle(coordinates []Coordinate, pairs []Pair[int]) int {
	best := 0
	for _, pair := range pairs {
		area := getArea(coordinates[pair.a], coordinates[pair.b])
		if area > best {
			best = area
		}
	}

	return best
}

func mod(a, b int) int {
	return (a + b) % b
}

// DFS flood fill
func FloodFill(edges *Set[Coordinate], grid *[][]int, visited *Set[Coordinate], dx, dy []int, X, Y int, curr Coordinate) {
	if curr.x < 0 || curr.x >= X || curr.y < 0 || curr.y >= Y {
		return
	}

	_, ok := visited.m[curr]
	if ok {
		return
	}
	
	_, ok2 := edges.m[curr]
	if ok2 {
		return
	}
	
	addItem(visited, curr)

	(*grid)[curr.y][curr.x] = 1

	for i := 0; i < len(dx); i++ {
		FloodFill(edges, grid, visited, dx, dy, X, Y, Coordinate{curr.x + dx[i], curr.y + dy[i]})
	}
}

func GenerateSumTable(grid [][]int) [][]int {
	table := make([][]int, len(grid))
	for i := 0; i < len(grid); i++ {
		table[i] = make([]int, len(grid[0]))
	}

	for i := 0; i < len(table); i++ {
		for j := 0; j < len(table[0]); j++ {
			table[i][j] = grid[i][j] + SafeRetrieve(table, i, j - 1) + 
							SafeRetrieve(table, i - 1, j) - SafeRetrieve(table, i - 1, j - 1)
		}
	}

	return table
}

func SafeRetrieve(grid [][]int, r, c int) int {
	if r < 0 || r >= len(grid) || c < 0 || c >= len(grid[0]) {
		return 0
	}

	return grid[r][c]
}


