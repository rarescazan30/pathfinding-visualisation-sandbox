**Cazan Rares-Stefan - 324CA**

**Chiselita Sebastian - 324CA**

# Pathfinding Visualisation Sandbox

## 1) Project Description:

For this project, we implemented a real-time `simulation` and `visualization` of pathfinding algorithms. The main objective was to build an interactive tool that demonstrates how different algorithms explore a `maze` to find a `path` between two points.

The application handles dynamic interactions, allowing the user to `draw walls`, place the `start/finish`, and includes a `Race Mode` where the user competes against the computer to find the path first. The user can also `save` the labyrinths created and `load` mazes with a specified text format or choose from existing `presets/templates`.

## 2) Class Structure and Implementation:

To ensure a clean architecture, we structured the project into multiple packages:

### 2.1) Main and Managers:

The `main.py` file is the entry point of the application. It initializes the `pygame` window, the main loop, and coordinates the updates between the logic and the display.

The Managers handle specific responsibilities:

* **`TextureManager`:** Handles loading and caching of all `sprite` assets (textures for walls, floors, etc) to optimize performance.

* **`EventHandler`:** Processes all user inputs (`keyboard presses` and `mouse clicks`) and delegates actions to the grid or the algorithms.

### 2.2) Algorithms:

We implemented the pathfinding logic in the algorithms package. Each algorithm modifies the state of the nodes directly to visualize the process:

* **`BFS (Breadth-First Search)`:** Explores all neighbors level by level, guaranteeing the `shortest path` on any maze;

* **`DFS (Depth-First Search)`:** Explores as `deep` as possible along each branch before backtracking;

* **`Greedy Best-First Search`:** A greedy approach that expands the node `closest to the goal`.

* **`A* (A-Star)`:** Uses a heuristic function to estimate the cost, making it the `most efficient` choice for finding the `shortest` path.

### 2.3) Core and Grid Logic:

The map is represented by the `grid.py` module in the `core` package.

* **`Grid:`** Manages the 2D array of spots. It handles the logic for `neighbor validation` (checking boundaries and walls).

* **`matrix_utils.py:`** Helper module for initializing the data structures and resetting the matrix state without restarting the application.

### 2.4) UI and Entities:

The graphical interface components are located in the `ui` package:

* **`Spot:`** Represents a `single` cell/tile on the map. It holds `state` data (is_wall, is_start, is_end, etc) and references to its graphical assets.

* **`Button:`** A reusable class for the UI `controls` (choosing algorithms, clearing the grid).

* **`PresetChooser:`** A `separate` window class allowing users to select `pre-configured` maps.

### 2.5) Assets and Config:

* **`assets/:`** Contains the visual resources (.png files) for the `textures`.

* **`config/presets.py:`** Stores the static data for `predefined` mazes.

## 3) Important Implementation Details:

### 3.1) Link to Github project:
https://github.com/rarescazan30/pathfinding-visualisation-sandbox

### 3.2) Languages & Technologies:

* **Programming Language**: Python 3.12.3
* **Graphics Engine**: `pygame` (Surface rendering, Event loop, Sprite management)
* **GUI Components**:
  * `easygui`: For native OS file dialogs (Load/Save windows).
  * Custom UI elements (Buttons, Windows) built from scratch using Pygame.
* **System Integration**: `pyperclip` (For clipboard operations).

### 3.3) Installation and Setup:

To run the project, a `Python virtual environment` is recommended to manage dependencies.

`Step 1:` Create Virtual Environment

#### Windows
`python -m venv venv`
`.\venv\Scripts\activate`

#### macOS/Linux
`python3 -m venv venv`
`source venv/bin/activate`


`Step 2:` Install Dependencies
The project relies on `pygame` for rendering, `easygui` for file dialogs(load for windows), and `pyperclip` for clipboard operations:

`pip install pygame easygui pyperclip`

`Step 3:` Run the Application

`python main.py`

### 3.4) Controls and Interaction:

#### The Mouse and Keyboard controls:

* **`Left Click:`** `Place` Start/End nodes (first 2 clicks) or `draw Walls` (can use Left Click + Drag).

* **`Right Click:`** `Erase` Start/End nodes.

* **`Spacebar:`** Start the `visualization` of the currently selected algorithm.

* **`C:`** `Clear` the grid.

#### Button interactions:

* **`Texture buttons:`** You can choose between 2 `textures` and a default `color` option for all kinds of tiles (wall, path, start, search, etc).

* **`Find Path:`** Same as `spacebar`, start the `visualization` of the currently selected algorithm.

* **`Race Mode OFF/ON:`** Activates/deactivates mode where the user can `draw a path` and `competes` with the algorithm for who finds the path `first`. The `time` to find the path is shown in the end.

* **`Toggle grid:`** Activates/deactivates `grid lines` for visual preferences.

* **`Grid size -/+:`** Increase/Decrease `grid size`. (min = 10, max = 60)

* **`Presets:`** Redirects the user to a `new window` where a `premade maze` can be chosen.

* **`Load Mac/Win:`** 2 buttons for 2 loading options that we found. One only works on `mac` and the other only on `windows`. `Linux` seems to work on both. The user writes or pastes a labyrinth using the `specified text format`.

* **`Save:`** Save the maze on the screen on `clipboard` in the `specified text format`.

* **`BFS/DFS/GBFS/A*:`** Buttons for choosing the `current algorithm`.


### 3.5) Coordinate System:

The grid uses a standard `2D coordinate system` where `(0,0)` is the `top-left` corner. The algorithms interact with the `Spot` objects using `(row, col)` indices.

## 4) Credits:
* **Cazan Rares-Stefan**:
  * **`Features Implemented`**:
    * **`Visual Logic`**: `Spot Class` for grid representation, connecting `Backend` algorithm logic with `Frontend` visual updates.
    * **`System`**: `Save` and `Load for Mac` functionalities implemented
    * **`Minigame`**: `Race Mode` minigame with a `Timer`, allowing the user to race against the machine
    * **`Algorithms`**: Depth-First Search (`DFS`), Greedy Best-First Search (`Greedy BFS`), A Star (`A*`)
  * **`Key Challenges`**:
    * **`Faulty event handling`**: Multiple errors caused by poor `Event Management` when implementing `Race Mode`.
    * **`Load conflicts`**: Introduced new `Load` logic with proper macOS support.
    * **`Visual synchronization`**: Critical issues while implementing user-supported input for `Race Mode`. Added `Yield` to algorithms and adjusted update handling.

* **Chiselita Sebastian**:
  * **`Features Implemented`**:
    * **`Grid Tools`**: `Eraser` tool, `Grid lines` rendering, and `Toggle Grid` button.
    * **`Visual Logic`**: `Texture/Color` mapping for tiles, `Grid sizing`, and `Dynamic centralization`.
    * **`System`**: `Save` and `Load for Windows/Linux` functionalities and the `Presets` engine (logic & `pre-defined` maps).
    * **`Algorithms`**: Breadth-First Search (`BFS`).
  * **`Key Challenges`**:
    * **`GUI Conflicts`**: Critical crashes caused by the interaction between `easygui` file dialogs and the main `pygame` event loop.
    * **`State Synchronization`**: Fixed logic errors where the Eraser tool would remove visual elements without updating the backend grid state (`visual vs. functional desync`).
    * **`Dynamic Layout`**: Solved rendering alignment issues to ensure the maze remains perfectly `centered` regardless of the grid size selection.

* **`Duminica Andra-Sara-Maria`**:
  * Created the images used in assets/ for texture creation.