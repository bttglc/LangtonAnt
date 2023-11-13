#include <iostream>
#include <vector>

// TODO
// gray cells for already visited

using std::cout;
using std::vector;

// Define the maximum size for the NxN board
static const unsigned int N = 500;

// Enum to represent possible directions the ant can face
// DirectionCount is used for standard enum manipulation in function move
enum Direction { North, East, South, West, DirectionCount };

// Enum to represent cell colors
enum Color : bool { White = true, Black = false };

// Struct to represent the ant's state
struct Ant {
    unsigned int x;
    unsigned int y;
    Direction direction;
};

// Struct to represent a cell's state
struct Cell {
    Color col;
    unsigned int visited;  // Number that represent when the cell has been first visited
};

// Prototypes
static unsigned int simulate(const unsigned int&);
static void move(Ant&, vector<Cell>&, const unsigned int);
static bool visited(Cell);

int main()
{    
    
    // Vector to store the number of iterations required for each board size
    vector<unsigned int> iterations(N + 1, 0);
    iterations[1] = 1;

    // Run simulation for each board size from 2 to N
    for (unsigned int i = 2; i < N; ++i) iterations[i] = simulate(i); 

    return 0;
}

// Function to simulate Langton's ant movement until all cells have been visited at least once
static unsigned int simulate(const unsigned int& size){
    unsigned int iteration_counter = 1;  // Count the total iterations
    unsigned int visit_counter = 1;      // Count how many cells have been visited

    // Initialize the board with all white cells that haven't been visited
    // we use a one-dimensional vector for higher efficiency compared to a vector of vectors
    vector<Cell> board(size * size, {White, 0});

    // Initialize the ant's position and direction
    // Since the board has wrap-around functionality, the actual values are irrelevant
    // Thus, we pick arbitrary ones
    Ant A = {0, 0, North};
            
    // Continue moving the ant until all cells are visited.
    while (visit_counter < size * size){
        if (!visited(board[A.x * size + A.y])){ 
            board[A.x * size + A.y].visited = visit_counter;
            visit_counter++;
        }
        move(A, board, size);
        iteration_counter++;
    }
    return iteration_counter;
}

// Function to check if a cell has been visited.
static bool visited(Cell c){
    return c.visited != 0;
}

// Function to move the ant based on its current state and the cell it's on
static void move(Ant &A, vector<Cell> &board, const unsigned int size){
    
    // Movement deltas for each direction
    static const int dx[] = {0, 1, 0, -1};
    static const int dy[] = {-1, 0, 1, 0};

    // Calculate the current cell index from the ant's position
    int index = A.x * size + A.y;

    // If the ant is on a white cell, turn clockwise, else turn counter-clockwise
    // using modulo operator and enum properties to shorten the comparison
    if (board[index].col == White) {
        board[index].col = Black;
        A.direction = static_cast<Direction>((A.direction + 1) % DirectionCount);
    } else {
        board[index].col = White;
        A.direction = static_cast<Direction>((A.direction + DirectionCount - 1) % DirectionCount);
    }

    // Update the ant's position using the movement deltas and wrap around if necessary
    A.x = (A.x + dx[A.direction] + size) % size;
    A.y = (A.y + dy[A.direction] + size) % size;
}

/* MAC: compile using 'clang++ -std=c++11 -stdlib=libc++ -Weverything ant_sim.cpp' */