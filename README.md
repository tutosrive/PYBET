**PYBET**

A system for managing a betting site (Casino), which allows you to simulate player management,
participation in different games of chance, and the establishment's internal processes.

⚙ To use locally (Collaborators)

1. Clone this repository (HTTPS)
    ```shell
    git clone https://github.com/tutosrive/PYBET.git
    ```

2. If you already have it, simply update it with this command:
    ```shell
    git pull origin main
    ```

3. Create and activate a virtual environment:
    ```shell
    python -m venv .venv
    .venv\Scripts\activate
    ```
    *(On Linux/Mac: `source .venv/bin/activate`)*

4. Install the required dependencies:
    ```shell
    pip install -r requirements.txt
    ```

5. Change branch (do not work in `main`):
    ```shell
    git switch {your-branch-name}
    ```
    > Work in your branch, after...

6. Add the changes:
    ```shell
    git add .
    ```

7. Commit the changes:
    ```shell
    git commit -m "Your descriptive message"
    ```

8. Push the changes to the repository:
    ```shell
    git push origin {your-branch-name}
    ```

---

## Step-by-Step Guide: How to Use Every Feature in PYBET

Below is a detailed, step-by-step guide for running and testing every main feature of the PYBET casino system. Follow these instructions after setting up your environment as described above.

### 1. Start the Application
1. Open a terminal in the project root directory.
2. Activate your virtual environment if not already active:
   ```shell
   .venv\Scripts\activate
   ```
3. Run the main program:
   ```shell
   python run.py
   ```
4. You will see a main menu with numbered options. Use the number keys to select options as described below.

### 2. Player Management (CRUD)
1. From the main menu, select the option labeled **Player Management** (usually option 1).
2. Inside the Player Management menu, you can:
   - **Add a player:** Choose the option to add a player, enter the player's name and initial balance when prompted.
   - **List all players:** Choose the option to list all players to see their IDs, names, and balances.
   - **Update a player:** Select the update option, enter the player ID, and provide new details as prompted.
   - **Delete a player:** Select the delete option, enter the player ID to remove them from the system.
3. Return to the main menu by selecting the exit/back option.

### 3. Player History
1. From the main menu, select **Player History**.
2. Enter the player ID when prompted.
3. You can now:
   - **View history:** See all actions performed by the player.
   - **Add an action:** Add a new action to the player's history.
   - **Remove last action:** Remove the most recent action (pop).
   - **Export history:** Choose the export option to save the player's history as JSON/CSV in `./pybet/data/reports/`.
4. Return to the main menu when done.

### 4. Waiting Queue
1. From the main menu, select **Waiting Queue**.
2. You can:
   - **Enqueue:** Add a player to the queue by entering their ID.
   - **Dequeue:** Remove the player at the front of the queue.
   - **View queue:** Display the current queue order.
   - **Clear queue:** Remove all players from the queue.
3. Return to the main menu when finished.

### 5. Backtracking (Optimal Betting Path)
1. From the main menu, select **Backtracking**.
2. Enter the initial balance and the list of bet options as prompted.
3. The system will calculate and display the optimal sequence of bets to maximize usage of the balance.
4. Review the result and return to the main menu.

### 6. Play Games
1. From the main menu, select **Games**.
2. Choose one of the following:
   - **Tragamonedas (Slot Machine):** Select this to play the slot machine game. Enter the player ID and follow the prompts to place bets and spin.
   - **Adivinanzas (Guessing Game):** Select this to play the guessing game. Enter the player ID and follow the prompts to guess numbers and place bets.
3. After playing, you can return to the games menu or main menu.

### 7. Reports
1. From the main menu, select **Reports**.
2. Choose the report you want to generate:
   - **Top balances:** Shows players with the highest balances.
   - **Earnings ranking:** Ranks players by their earnings.
   - **Player history report:** Enter a player ID to generate a detailed history report.
   - **Loss counts:** Shows how many times each player has lost.
   - **Game participation:** Shows how many times each game has been played.
3. Reports are saved in `./pybet/data/reports/` as both JSON and CSV files. The system will display the file paths after generation.

### 8. Export Player History
- You can export a player's history from either the **Reports** or **Player History** menu by selecting the export option and entering the player ID. Files will be saved in `./pybet/data/reports/`.

### 9. Example Scripts (Automated Demonstrations)
- To see a full demonstration of all features (with console output), run:
  ```shell
  python final_example.py
  ```
- For a simpler, quick simulation, run:
  ```shell
  python examples.py
  ```
- These scripts will create players, simulate games, and generate/export reports automatically. Check the console output and the `./pybet/data/reports/` directory for results.

---

**Tip:** If you ever get lost, return to the main menu and select the desired option again. For any manual test, always start with `python run.py` and follow the menu prompts as described above.
