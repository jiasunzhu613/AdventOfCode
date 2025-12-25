package utils

type Set[T comparable] struct {
	m map[T]struct{}
}

// Make new set with input values if any (uses variadics)
// Empty struct uses 0 memory
func NewSet[T comparable](items ...T) *Set[T] {
	s := &Set[T]{
		m: make(map[T]struct{}),
	}

	for _, item := range items {
		s.m[item] = struct{}{} // second set of braces is for construction of the empty struct
	}

	return s
}

func AddItem[T comparable](set *Set[T], item T) {
	_, ok := set.m[item]

	// If already in set, we dont care anymore
	if ok {
		return
	}

	set.m[item] = struct{}{}
}

func In[T comparable](set *Set[T], item T) bool {
	_, ok := set.m[item]

	return ok
}