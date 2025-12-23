package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

const MAX_BATTERY_BANK_LEN = 100

/*
Ideation for part 2:
  - dp with states for maximum joltage if you turn 1 battery on, 2 batteries on, so on, until 12
    => but also need to keep track of length and where the last battery flipped on was
*/
func main() {
	var lengthFlag = flag.Int("l", 12,
		"number of batteries you want to consider in your joltage per battery bank")
	flag.Parse()

	if *lengthFlag > MAX_BATTERY_BANK_LEN {
		panic("Specified number of batteries is greater than maximum # of batteries in a bank of " + strconv.Itoa(MAX_BATTERY_BANK_LEN))
	}

	file, err := os.ReadFile("../input/day3.txt")
	if err != nil {
		log.Fatal(err)
	}

	banks := strings.Split(string(file), "\n")

	total := 0
	for _, bank := range banks {
		fmt.Println(findHighestJoltage(bank, *lengthFlag))
		total += findHighestJoltage(bank, *lengthFlag)
	}

	fmt.Println("Maximum joltage obtainable:", total)
}

func findHighestJoltage(bank string, length int) int {
	battery := make([]int, len(bank))
	for i := range battery {
		battery[i] = ctoi(bank[i])
	}

	// We will use tabulation to build a dp table of the best values based on two states:
	// 1. last index we are able to consider, i
	// 2. the length of the current subsequence we are considering, l
	dp := make([][]int, length+1) // y-dim of len(bank)
	for i := range dp {
		dp[i] = make([]int, len(bank)) // x-dim of length
	}

	// Fill the first row with prefix max array
	dp[1][0] = battery[0]
	for i := 1; i < len(battery); i++ {
		dp[1][i] = max(battery[i], dp[1][i-1])
	}

	for l := 2; l <= length; l++ {
		for i := l - 1; i < len(battery); i++ {
			// How will we tabulate?
			// For each index, we will consider the max of two options:
			// 1. the value at dp[l][i - 1]
			// 2. the value formed by the following equation: dp[l - 1][i - 1] * 10 + battery[i]
			dp[l][i] = max(dp[l][i-1], dp[l-1][i-1]*10+battery[i])
		}
	}

	// Debugging
	// for _, arr := range dp {
	// 	fmt.Println(arr)
	// }

	return dp[length][len(battery)-1]
}

func ctoi(c byte) int {
	return int(c - '0')
}
