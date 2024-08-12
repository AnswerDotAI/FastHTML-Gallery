# Cellular Automata

Cellular automata are a class of models that are used to simulate complex systems. They are made up of a grid of cells, each of which can be in one of a finite number of states. The state of each cell is updated at each time step based on the states of its neighbors. Cellular automata are used in a wide range of applications, including modeling the spread of diseases, traffic flow, and the behavior of crowds.This project is a 1 dimensional cellular automata. 

## How it works

We start with an initial row. In this app the row is a series of white squares followed by a single black square followed by more white squares. 

A cell is created based on the state of the three cells above it ( directly above and to the left and right). That means there are eight possible combinations of the three cells. We consider a white square to be a 0 and a black square to be a 1. This gives us a number between 0 and 7, I'll call this the cell update number.

The rule is a number between 0 and 256. We take that number and convert it to its binary representation. This will be a sequence of 8 0s and 1s. Taking the cell update number, we look at the corresponding digit in the rule. If it is a 1, the cell becomes black, if it is a 0, the cell becomes white.

You can see a visual representation of the rule in the app. 

## Key Technologies and Techniques

* **HTMX Polling**: We use polling to update the grid every 100ms. This is done by setting the `hx-get` attribute `every .1s`. This triggers a GET request until we run out of generations and then the `Response(status_code=286)` stops the polling.

* **[Progress Bar](https://fasthtml.gallery/widgets/progress_bar/display)**

* **[Show Hide Button](https://fasthtml.gallery/widgets/show_hide/display)**

* **Inline Validation**:






