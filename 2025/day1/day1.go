package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

func main() {
	content, err := os.ReadFile("../input/day1.txt")
	if err != nil {
		log.Fatal(err)
	}

	input := strings.Split(string(content), "\n")
	dial := 50
	pt1 := 0
	pt2 := 0

	for _, line := range input {
		amount, _ := strconv.Atoi(string(line[1:]))
		dial = turnDial(dial, &pt1, &pt2, string(line[0]), amount)
	}
	fmt.Println("Password with normal method is:", pt1)
	fmt.Println("Password with method 0x434C49434B is:", pt2)
}

func turnDial(curr int, pt1 *int, pt2 *int, direction string, amount int) int {
	prerotations := amount / 100
	*pt2 += prerotations
	amount %= 100

	if direction == "L" {
		amount *= -1
	}

	if curr != 0 &&
		(min(curr, curr+amount) <= 0 && 0 <= max(curr, curr+amount)) ||
		(min(curr, curr+amount) <= 100 && 100 <= max(curr, curr+amount)) {
		*pt2++
	}
	curr += amount
	result := mod(curr, 100)
	if result == 0 {
		*pt1++
	}

	return result
}

func mod(a int, b int) int {
	return (a%b + b) % b
}
