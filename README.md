# cs-475-group-10
## Purpose
The purpose of this repository is to investigate the state explosion problem when converting an NFA to a DFA. As the number of NFA states is increased, the number of equivalent DFA states is believed to increase exponentially.

## Requirements
- Python
- Matplotlib
- .csv input files

## File Organization
### Input
To use the written python code, it requires a .csv file that contains information about the NFA to convert:

| NFA ID | Starting State | Accepting State | From State | Symbol | To State |
| ------ | -------------- | --------------- | ---------- | ------ | ----- |
| The ID of the NFA to convert. This should be the same for every entry in the file. | The state that the NFA starts with. This should be the same for every entry. | The accepting state of the NFA. This should be the same for every entry. | The state that the transition starts from. | The symbol that causes a state transition. | The state that a transition moves to. |

These files are stored in the input_data folder.

### Processing
All processing occurs in convert_nfa.py. It has 5 functions (including main) to do this:

| Function | Task | Input | Output |
| ------ | -------------- | --------------- | ---------- |
| main | Converts a NFA (specified in the command line) to a DFA and saves the results as a plot | Command line argument, such as "python convert_nfa.py nfa1.csv" | Printed text; Output files are moved to the results folder. |
| read_nfa | Reads a NFA from a given .csv file | The name of the file to read | NFA transitions, starting state, and accepting states |
| convert_nfa_to_dfa | Converts a NFA to a DFA with subset construction | The NFA and its alphabet, starting state, and accepting states | DFA states, transitions, and accepting states |
| count_nfa_states | Counts all states in the original NFA | The NFA transitions, starting state, and accepting states | The set of all NFA states |
| create_plot | Creates a plot of the conversion results | The filename, NFA state count, and DFA state count | A PNG file that is moved to the results folder by main |

### Final Output
All output is saved in the results folder

The NFA-to-DFA conversion results are displayed with the following:
- Number of states
- State increase
- Growth ratio
- DFA States
- Transitions
- Accepting states

The results also saved as a bar chart PNG file. Its corresponding .csv file contains the following:
| File | NFA States | DFA States | Increase | Growth Ratio |
| ------ | -------------- | --------------- | ---------- | ------ |
| The name of the NFA file that was converted | The number of NFA states | The number of DFA states | The increase in states due to conversion| The ratio of growth from conversion |
