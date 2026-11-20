import os
import csv
import glob
import argparse
import matplotlib.pyplot as plt
from collections import defaultdict, deque

# Set folders for input and output
INPUT_FOLDER = "input_data"
RESULTS_FOLDER = "results"

os.makedirs(RESULTS_FOLDER, exist_ok = True)

# Read the NFA from a given .csv file
def read_nfa(filename):
    nfa = defaultdict(lambda: defaultdict(set))
    starting_state = None
    accepting_states = set()

    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            start = row["starting_state"].strip()
            accept = row["accepting_state"].strip()
            source = row["from_state"].strip()
            symbol = row["symbol"].strip()
            destination = row["to_state"].strip()

            # Store the starting and accepting states
            if starting_state is not None and starting_state != start:
                raise ValueError(f"Could not get starting_state.")

            starting_state = start
            accepting_states.add(accept)

            # Store each NFA transition
            nfa[source][symbol].add(destination)

    if starting_state is None:
        raise ValueError(f"Could not get transitions.")

    return nfa, starting_state, accepting_states

# Convert the NFA to a DFA with subset construction
def convert_nfa_to_dfa(nfa, alphabet, starting_state, accepting_state):
    starting_state = frozenset({starting_state})
    dfa_states = [starting_state]
    dfa_transitions = {}

    queue = deque([starting_state])

    # For each discovered DFA state
    while queue:
        current = queue.popleft()
        dfa_transitions[current] = {}

        for symbol in alphabet:
            next_states = set()
            
            # Get every possible NFA destination
            for state in current:
                next_states.update(nfa[state][symbol])
            next_states = frozenset(next_states)
            dfa_transitions[current][symbol] = next_states

            # If a new DFA is discovered, add it to the queue
            if next_states not in dfa_states:
                dfa_states.append(next_states)
                queue.append(next_states)

    # Get DFA states with at least one accepting NFA state
    accepting_dfa = [
        state for state in dfa_states
        if state & accepting_state
    ]

    return dfa_states, dfa_transitions, accepting_dfa

# Count all states in the original NFA
def count_nfa_states(nfa, starting_state, accepting_states):
    nfa_states = {starting_state} | accepting_states

    for source, symbols in nfa.items():
        nfa_states.add(source)

        for destinations in symbols.values():
            nfa_states.update(destinations)

    return nfa_states

# Create a plot of the conversion results
def create_plot(filename, nfa_count, dfa_count):
    plt.figure()

    plt.bar(
        ["NFA", "DFA"],
        [nfa_count, dfa_count]
    )

    plt.title(f"State Comparison: {os.path.basename(filename)}")
    plt.ylabel("Number of States")

    plot_name =os.path.basename(filename).replace(".csv", "_plot.png")
    plot_path = os.path.join(RESULTS_FOLDER, plot_name)

    plt.savefig(plot_path)
    plt.close()

def main():
    # Get filename as command line argument
    parser = argparse.ArgumentParser(
        description = "Covert a NFA to a DFA using its .csv file"
    )
    parser.add_argument(
        "filename",
        help = "Name of the NFA .csv file, found in input_data folder"
    )
    args = parser.parse_args()

    filename = os.path.join(INPUT_FOLDER, args.filename)
    if not os.path.isfile(filename):
        print(f"Error: {args.filename} was not found in {INPUT_FOLDER}")
        return

    # Read the NFA from the .csv file and create its alphabet
    nfa, starting_state, accepting_states = read_nfa(filename)

    alphabet = sorted({
        symbol
        for symbols in nfa.values()
        for symbol in symbols
    })

    # Convert the NFA to an equivalent DFA
    dfa_states, dfa_transitions, accepting_dfa = convert_nfa_to_dfa(nfa, alphabet, starting_state, accepting_states)
    
    # Get state counts and growth
    nfa_states = (count_nfa_states(nfa, starting_state, accepting_states))

    # Get variables for final results
    nfa_count = len(nfa_states)
    dfa_count = len(dfa_states)
    increase = dfa_count - nfa_count
    ratio = dfa_count / nfa_count

    # Display results
    print("NFA TO DFA CONVERSION")
    print("---------------------")
    print(f"File: {args.filename}")
    print(f"NFA states: {nfa_count}")
    print(f"DFA states: {dfa_count}")
    print(f"Increase in states: {increase}")
    print(f"Growth ratio: {ratio:.2f}x")

    print("\nDFA STATES:")
    for i, state in enumerate(dfa_states, start = 1):
        print(f"DFA #{i} = {sorted(state)}")

    print("\nDFA TRANSITIONS:")
    for i, state in enumerate(dfa_states, start = 1):
        for symbol in alphabet:
            destination = dfa_transitions[state][symbol]
            destination_number = dfa_states.index(destination) + 1
            print(f"DFA #{i} --{symbol}--> DFA #{destination_number}")

    print("\nACCEPTING DFAs:")
    for state in accepting_dfa: 
        print(f"DFA #{dfa_states.index(state) + 1}")

    # Save the results
    results = {
        "file": args.filename,
        "nfa_states": nfa_count,
        "dfa_states": dfa_count,
        "increase": increase,
        "growth_ratio": round(ratio, 2)
    } 
    
    results_name = os.path.basename(filename).replace(".csv", "_results.csv")
    results_path = os.path.join(RESULTS_FOLDER, results_name)
    with open(results_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames = results.keys())
        writer.writeheader()
        writer.writerow(results)

    # Create the results plot
    create_plot(filename, nfa_count, dfa_count)

    print("\n========================")
    print("CONVERSION SUCCEEDED")
    print(f"Results are stored in: {results_path}")
    print(f"The plot is saved to: {RESULTS_FOLDER}")
    print(f"State increase: {len(dfa_states) - len(nfa)}")

if __name__ == "__main__":
    main()