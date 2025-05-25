from pybet.logic.HistoryStack import HistoryStack
from pybet.logic.WaitingQueue import WaitingQueue
from pybet.logic.Backtracking import Backtracking

def test_history_and_queue():
    print("=== Testing HistoryStack ===")
    hs = HistoryStack(max_size=3)
    hs.push("Action 1")
    hs.push("Action 2")
    hs.push("Action 3")
    hs.push("Action 4")  # "Action 1" drops out
    print("Current stack (should be 2,3,4):", hs.stack)
    print("Pop:", hs.pop())
    print("Peek now:", hs.peek())
    hs.clear()
    print("Is empty after clear?", hs.is_empty())

    print("\n=== Testing WaitingQueue ===")
    wq = WaitingQueue()
    for pid in ["playerA", "playerB", "playerC"]:
        wq.enqueue(pid)
    print("Queue after enqueues (A,B,C):", wq.queue)
    print("Peek front (should be A):", wq.peek())
    print("Dequeue (should remove A):", wq.dequeue())
    print("Queue now (B,C):", wq.queue)
    wq.clear()
    print("Is empty after clear?", wq.is_empty())

def test_backtracking():
    print("\n=== Testing Backtracking (Class‐based) ===")
    initial = 100
    options = [5, 20, 50, 70, 30]
    solver = Backtracking(initial, options)
    sequence, total = solver.findOptimalPath()
    print(f"Initial balance: {initial}")
    print(f"Bet options: {options}")
    print(f"Best sequence of bets: {sequence}")
    print(f"Total used in bets: {total}")

if __name__ == "__main__":
    test_history_and_queue()
    test_backtracking()