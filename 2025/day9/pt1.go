package main

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

type Rectangle struct {
	area int
	c1   Coordinate // it is in no way guaranteed that c1 is top left and c2 is bottom right
	c2   Coordinate
}

func main() {
	file, err := os.ReadFile("../input/day9.txt")
	if err != nil {
		log.Fatal(err)
	}

	lines := strings.Split(string(file), "\n")

	coordinates := make([]Coordinate, 0)
	for _, line := range lines {
		x, y := processLine(line)
		coordinates = append(coordinates, Coordinate{x, y})
	}

	// PT 1
	rectangles := naiveFindLargestRectangle(coordinates)
	sort.Slice(rectangles, func(i, j int) bool {
		return rectangles[i].area > rectangles[j].area
	})

	fmt.Println("Largest rectangle is:", rectangles[0].area)
}

func processLine(line string) (int, int) {
	splitted := strings.Split(line, ",")

	x, _ := strconv.Atoi(splitted[0])
	y, _ := strconv.Atoi(splitted[1])

	return x, y
}

func naiveFindLargestRectangle(coordinates []Coordinate) []Rectangle {
	rectangles := make([]Rectangle, 0)
	for i := 0; i < len(coordinates); i++ {
		for j := i + 1; j < len(coordinates); j++ {
			area := getArea(coordinates[i], coordinates[j])
			rectangles = append(rectangles, Rectangle{area, coordinates[i], coordinates[j]})
		}
	}

	return rectangles
}

func getArea(c1, c2 Coordinate) int {
	return int((math.Abs(float64(c1.x-c2.x)) + 1) * (math.Abs(float64(c1.y-c2.y)) + 1))
}
