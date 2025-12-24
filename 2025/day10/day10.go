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

// PT1
// use binary bits to find all combinations of button presses
// since xor is commutative, we dont need to consider repeition of same button press since
// pressing the same button twice is equivalent to not pressing it at all

// PT2
// maybe dp, looks similar to coin change problem a little but more complicated
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
		buttons, _ := extractButtons(line)
		_, joltages := extractJoltage(line)

		// fmt.Println(target, buttons)

		summedLeastClicks += GetLeastButtonPresses(target, 0, 0, 0, buttons)
		summedLeastClicksJoltage += GetLeastButtonPressesJoltage(joltages, buttons)
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
func extractButtons(line string) ([]int, []int) {
	r := regexp.MustCompile(`\(([^()]*)\)`)
	captured := r.FindAllStringSubmatch(line, -1)

	values := make([]int, 0)
	values2 := make([]int, 0)
	
	for _, button := range captured {
		splitted := strings.Split(button[1], ",")
		value := 0
		value2 := 0
		for _, b := range splitted {
			bit, _ := strconv.Atoi(b)
			value += int(math.Pow(2, float64(bit)))
			value2 += int(math.Pow(BASE, float64(bit)))
		}
		values = append(values, value)
		values2 = append(values2, value2)
	}

	return values, values2
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

func GetLeastButtonPressesStates(least, target, current, consider, clicks int, state string, buttons []int, best *[]string) {
	if target == current && clicks == least{
		*best = append(*best, state)
		return
	}

	if consider == len(buttons) {
		return
	}

	// Consider current button
	considered := current ^ buttons[consider]

	GetLeastButtonPressesStates(least, target, considered, consider+1, clicks+1, state + "1", buttons, best)
	GetLeastButtonPressesStates(least, target, current, consider+1, clicks, state + "0", buttons, best)

	return
}

func GetLeastButtonPressesJoltage(joltages, buttonsInBaseTwo []int) int {
	target := 0
	for ind, joltage := range joltages {
		if joltage % 2 == 1 {
			target += int(math.Pow(2, float64(ind)))
		}
	}

	least := GetLeastButtonPresses(target, 0, 0, 0, buttonsInBaseTwo)

	best := make([]string, 0)
	GetLeastButtonPressesStates(least, target, 0, 0, 0, "", buttonsInBaseTwo, &best)

	for _, opt := range best {
		copiedJoltage := make([]int, 0)
		copy(copiedJoltage, joltages)

		for ind, c := range opt {
			if c == '1' {
				for _, val := range button
			}
		}
	}
	fmt.Println(best)
	return 1
}