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
	BIG_NUMBER = 1e10
)

// use binary bits to find all combinations of button presses
// since xor is commutative, we dont need to consider repeition of same button press since
// pressing the same button twice is equivalent to not pressing it at all
func main() {
	file, err := os.ReadFile("../input/day10.txt")
	if err != nil {
		log.Fatal(err)
	}
	
	lines := strings.Split(string(file), "\n")


	// PT1
	summedLeastClicks := 0 
	for _, line := range lines {
		target, _ := extractTargetWithLength(line)
		buttons := extractButtons(line)
		fmt.Println(target, buttons)
		
		summedLeastClicks += GetLeastButtonPresses(target, 0, 0, 0, buttons)
	}
	fmt.Println("Least number of clicks need to configure all machines:", summedLeastClicks)
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

func extractButtons(line string) []int {
	r := regexp.MustCompile(`\(([^()]*)\)`)
	captured := r.FindAllStringSubmatch(line, -1)
	
	values := make([]int, 0)
	for _, button := range captured {
		splitted := strings.Split(button[1], ",")
		value := 0
		for _, b := range splitted {
			bit, _ := strconv.Atoi(b)
			value += int(math.Pow(2, float64(bit)))
		} 
		values = append(values, value)
	}

	return values
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

	result := min(GetLeastButtonPresses(target, considered, consider + 1, clicks + 1, buttons), 
				  GetLeastButtonPresses(target, current, consider + 1, clicks, buttons))

	return result
}