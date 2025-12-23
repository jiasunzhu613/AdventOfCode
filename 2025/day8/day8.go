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

const (
	MAX_WIRES = 1000
)

type Coordinate struct {
	x int
	y int
	z int
}

type JunctionBoxDistance struct {
	distance float64
	from     int
	to       int
}

type UnionFind struct {
	id         []int
	size       []int
	components int
}

func NewUnionFind(length int) *UnionFind {
	unionFind := &UnionFind{id: make([]int, 0), size: make([]int, 0)}

	for i := 0; i < length; i++ {
		unionFind.id = append(unionFind.id, i)
		unionFind.size = append(unionFind.size, 1)
	}

	unionFind.components = length

	return unionFind
}

// Find the current set a node is a in
func find(unionFind UnionFind, node int) int {
	// If the node was not merged, the current set should be the unionFind.id[node]
	root := node
	for root != unionFind.id[root] {
		root = unionFind.id[root]
	}

	// Path compression, we will retraverse the path to get to the root node, and we will compress all nodes
	// along the path to the root node
	for node != root {
		next := unionFind.id[node] // Temp value
		unionFind.id[node] = root
		node = next
	}

	return root
}

func connected(unionFind UnionFind, node1 int, node2 int) bool {
	return find(unionFind, node1) == find(unionFind, node2)
}

// Unify two sets
func unify(unionFind UnionFind, node1 int, node2 int) {
	if connected(unionFind, node1, node2) {
		return
	}

	root1 := find(unionFind, node1) // Find root for node 1
	root2 := find(unionFind, node2) // Find root for node 2

	if unionFind.size[root1] < unionFind.size[root2] {
		unionFind.id[root1] = root2
		unionFind.size[root2] += unionFind.size[root1]
		unionFind.size[root1] = 0
	} else {
		unionFind.id[root2] = root1
		unionFind.size[root1] += unionFind.size[root2]
		unionFind.size[root2] = 0
	}

	unionFind.components--
}

func main() {
	file, err := os.ReadFile("../input/day8.txt")
	if err != nil {
		log.Fatal(err)
	}

	lines := strings.Split(string(file), "\n")

	unionFind := NewUnionFind(len(lines))

	// Calculate distances from each node to the other
	coordinates := make([]Coordinate, 0)
	for _, line := range lines {
		x, y, z := processLine(line)
		coordinates = append(coordinates, Coordinate{x, y, z})
	}

	distances := make([]JunctionBoxDistance, 0)
	for i := 0; i < len(coordinates); i++ {
		for j := i + 1; j < len(coordinates); j++ {
			distance := distance3D(coordinates[i], coordinates[j])
			distances = append(distances, JunctionBoxDistance{distance, i, j})
		}
	}

	sort.Slice(distances, func(i, j int) bool {
		return distances[i].distance < distances[j].distance
	})

	for i := 0; i < MAX_WIRES; i++ {
		junctionBox := distances[i]
		unify(*unionFind, junctionBox.from, junctionBox.to)
	}

	sizeCopy := make([]int, len((*unionFind).size))
	copy(sizeCopy, (*unionFind).size)
	fmt.Println(sizeCopy)
	sort.Slice(sizeCopy, func(i, j int) bool {
		return sizeCopy[i] > sizeCopy[j]
	})

	productOfSizes := sizeCopy[0] * sizeCopy[1] * sizeCopy[2]
	fmt.Println("Product of top 3 circuits:", productOfSizes)

	_, xProduct := connnectedAll(distances, coordinates, *unionFind)
	fmt.Println("Product of x of last two connected junction boxes:", xProduct)
}

func processLine(line string) (int, int, int) {
	splitted := strings.Split(line, ",")

	x, _ := strconv.Atoi(splitted[0])
	y, _ := strconv.Atoi(splitted[1])
	z, _ := strconv.Atoi(splitted[2])

	return x, y, z
}

func distance3D(c1, c2 Coordinate) float64 {
	xDiff := c1.x - c2.x
	yDiff := c1.y - c2.y
	zDiff := c1.z - c2.z

	squareSum := float64(xDiff*xDiff + yDiff*yDiff + zDiff*zDiff)
	return math.Sqrt(squareSum)
}

func connnectedAll(edges []JunctionBoxDistance, coordinates []Coordinate, unionFind UnionFind) (int, int) {
	lastConnectedXProduct := -1
	totalWeight := 0

	for i := 0; unionFind.components != 1 && i < len(edges); i++ {
		if connected(unionFind, edges[i].from, edges[i].to) {
			continue
		}

		// Connect the two nodes
		totalWeight += int(edges[i].distance)
		unify(unionFind, edges[i].from, edges[i].to)
		lastConnectedXProduct = coordinates[edges[i].from].x * coordinates[edges[i].to].x
	}

	return totalWeight, lastConnectedXProduct
}
