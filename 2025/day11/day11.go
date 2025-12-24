package main

import (
	"fmt"
	"log"
	"os"
	"strings"
)

const (
	TARGET = "out"
	START1 = "you"
	START2 = "svr"
)

func main() {
	file, err := os.ReadFile("../input/day11.txt")
	if err != nil {
		log.Fatal(err)
	}

	lines := strings.Split(string(file), "\n")

	// Construct adjacency map
	adjMap := make(map[string][]string)
	for _, line := range lines {
		splitted := strings.Split(line, ": ")
		key := splitted[0]
		values := strings.Split(splitted[1], " ")
		adjMap[key] = values
	}

	visited := make(map[string]int)
	paths := FindAllPaths(TARGET, START1, visited, adjMap)
	fmt.Println("All different paths:", paths)

	pathsWithAttraction := FindAllPathsWithAttractions(adjMap)
	fmt.Println("All different paths while visiting dac and fft:", pathsWithAttraction)
}

func FindAllPaths(target, curr string, visited map[string]int, adjMap map[string][]string) int {
	if curr == target {
		return 1
	}

	count, ok := visited[curr]
	if ok {
		return count
	}

	result := 0
	for _, neighbour := range adjMap[curr] {
		result += FindAllPaths(target, neighbour, visited, adjMap)
	}

	visited[curr] = result
	return result
}

func FindAllPathsWithAttractions(adjMap map[string][]string) int {
	// We will take a kinda stupid approach of just doing math and having terrible memory complexity
	allPaths := make(map[string]int)
	FindAllPaths(TARGET, START2, allPaths, adjMap)

	// svr to dac
	svrToDac := make(map[string]int)
	svrToDacPaths := FindAllPaths("dac", START2, svrToDac, adjMap)

	// svr to fft
	svrToFft := make(map[string]int)
	svrToFftPaths := FindAllPaths("fft", START2, svrToFft, adjMap)

	// dac to fft
	dacToFft := make(map[string]int)
	dacToFftPaths := FindAllPaths("fft", "dac", dacToFft, adjMap)

	// fft to dac
	fftToDac := make(map[string]int)
	fftToDacPaths := FindAllPaths("dac", "fft", fftToDac, adjMap)

	// total paths
	total := 0
	total += allPaths["fft"] * dacToFftPaths * svrToDacPaths // svr -> dac -> fft -> out
	total += allPaths["dac"] * fftToDacPaths * svrToFftPaths // svr -> fft -> dac -> out
															 // ^ note with things in the middle but these are the main "attractions"

	return total
}