package main

import (
	"fmt"
	"log"
	"math"
	"os"
	"regexp"
	"strconv"
	"strings"
)

const (
	BIG_NUMBER = 100000 * 100000
	BASE       = 500
)

type Pattern struct {
	cost []int
	length int
}

// PT1
// use binary bits to find all combinations of button presses
// since xor is commutative, we dont need to consider repeition of same button press since
// pressing the same button twice is equivalent to not pressing it at all

// PT2
// https://www.reddit.com/r/adventofcode/comments/1pk87hl/2025_day_10_part_2_bifurcate_your_way_to_victory/
func main() {
	file, err := os.ReadFile("../input/day10.txt")
	if err != nil {
		log.Fatal(err)
	}

	lines := strings.Split(string(file), "\n")

	// PT1 + PT2
	summedLeastClicks := 0
	summedLeastClicksJoltage := 0 
	for _, line := range lines {
		target, _ := extractTargetWithLength(line)
		buttons, _, rawButtons := extractButtons(line)
		_, joltages := extractJoltage(line)

		summedLeastClicks += GetLeastButtonPresses(target, 0, 0, 0, buttons)
		
		memo := make(map[string]int)
		options := make([]string, 0)
		GetButtonPressesStates(target, 0, 0, "", buttons, &options) // try all options that could make the on/off pattern
		patterns := getAllPattern(options, len(joltages), rawButtons)
		summedLeastClicksJoltage += GetLeastButtonPressesJoltage(joltages, buttons, rawButtons, patterns, memo)

	}
	fmt.Println("Least number of clicks need to configure all machines:", summedLeastClicks)
	fmt.Println("Least number of clicks need to make joltage match for all machines:", summedLeastClicksJoltage)
}

func extractTargetWithLength(line string) (int, int) {
	r := regexp.MustCompile(`\[(.*)\]`)
	captured := r.FindStringSubmatch(line)

	target := captured[1]

	value := 0
	for ind, c := range target {
		if c == '#' {
			value += int(math.Pow(2, float64(ind)))
		}
	}

	return value, len(target)
}

// Extracts value for button in both base 2 and base 200
func extractButtons(line string) ([]int, []int, [][]int) {
	r := regexp.MustCompile(`\(([^()]*)\)`)
	captured := r.FindAllStringSubmatch(line, -1)

	values := make([]int, 0)
	values2 := make([]int, 0)
	raw := make([][]int, 0)
	
	for _, button := range captured {
		splitted := strings.Split(button[1], ",")
		value := 0
		value2 := 0
		value3 := make([]int, 0)
		for _, b := range splitted {
			bit, _ := strconv.Atoi(b)
			value += int(math.Pow(2, float64(bit)))
			value2 += int(math.Pow(BASE, float64(bit)))
			value3 = append(value3, bit)
		}
		values = append(values, value)
		values2 = append(values2, value2)
		raw = append(raw, value3)
	}

	return values, values2, raw
}

// Express as a base X number
func extractJoltage(line string) (int, []int){
	r := regexp.MustCompile(`\{(.*)\}`)
	captured := r.FindStringSubmatch(line)

	joltage := captured[1]
	splitted := strings.Split(joltage, ",")

	values := make([]int, 0)
	value := 0
	for ind, co := range splitted {
		coeff, _ := strconv.Atoi(co)
		values = append(values, coeff)
		value += coeff * int(math.Pow(BASE, float64(ind)))
	}
	
	return value, values
}

func GetLeastButtonPresses(target, current, consider, clicks int, buttons []int) int {
	if target == current {
		return clicks
	}

	if consider == len(buttons) {
		return BIG_NUMBER
	}

	// Consider current button
	considered := current ^ buttons[consider]

	result := min(GetLeastButtonPresses(target, considered, consider+1, clicks+1, buttons),
		GetLeastButtonPresses(target, current, consider+1, clicks, buttons))

	return result
}

func GetButtonPressesStates(target, current, consider int, state string, buttons []int, best *[]string) {
	if consider == len(buttons) {
		*best = append(*best, state)
		return
	}

	// Consider current button
	considered := current ^ buttons[consider]

	GetButtonPressesStates(target, considered, consider+1, state + "1", buttons, best)
	GetButtonPressesStates(target, current, consider+1, state + "0", buttons, best)
}

func GetLeastButtonPressesJoltage(joltages, buttonsInBaseTwo []int, buttons [][]int, patterns []Pattern, memo map[string]int) int {
	// Base cases + memo
	memoClicks, ok := memo[arrayToString(joltages)]
	if ok {
		return memoClicks
	}

	if allZeros(joltages) {
		return 0
	}

	if hasNegative(joltages) {
		return BIG_NUMBER
	}

	// Start: Recursive
	leastJoltage := BIG_NUMBER
	for _, pattern := range patterns {
		// check parity between option and joltages
		if !sameParity(pattern.cost, joltages) {
			continue
		}

		copiedJoltage := make([]int, len(joltages))
		copy(copiedJoltage, joltages)
		// fmt.Println("copied:", copiedJoltage)

		for ind, val := range pattern.cost {
			copiedJoltage[ind] -= val
		}

		// We dont care about any iteration where the joltages go negative
		if hasNegative(copiedJoltage) {
			continue
		}	
		
		// Figure out how to find smalled array
		for i := range copiedJoltage {
			copiedJoltage[i] /= 2
		}

		clicks := 2 * GetLeastButtonPressesJoltage(copiedJoltage, buttonsInBaseTwo, buttons, patterns, memo) + pattern.length
		leastJoltage = min(leastJoltage, clicks)
	}
	
	// add to memo
	memo[arrayToString(joltages)] = leastJoltage
	return leastJoltage
}

func arrayToString(arr []int) string {
	return strings.Join(strings.Fields(fmt.Sprint(arr)), ",")
}

func allZeros(arr []int) bool {
	for _, ele := range arr {
		if ele != 0 {
			return false
		}
	}

	return true
}

func hasNegative(arr []int) bool {
	for _, ele := range arr {
		if ele < 0 {
			return true
		}
	}

	return false
}

func getPattern(bits string, l int, buttons [][]int) ([]int, int) {
	active := 0
	change := make([]int, l)
	for ind, c := range bits {
		if c == '1' {
			for _, index := range buttons[ind] {
				change[index]++
			}
			active++
		}
	}

	return change, active
}

func getAllPattern(options []string, l int, buttons [][]int) []Pattern {
	patterns := make([]Pattern, 0)
	for _, opt := range options {
		cost, length := getPattern(opt, l, buttons)
		patterns = append(patterns, Pattern{cost, length})
	}

	return patterns
}

func sameParity(a, b []int) bool{
	for i := range a {
		if a[i] % 2 != b[i] % 2 {
			return false
		}
	}

	return true
}