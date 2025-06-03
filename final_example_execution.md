```shell
Visite esta página (https://docs.dev2forge.software/chromologger/) antes de ejecutar este módulo
✅ Data directories and files initialized.

=== Player CRUD Operations ===
The JSON file "./pybet/data/players.json" is empty    
✔ Created Player: Alice (ID: X9Z980, Balance: 1000.00)
✔ Created Player: Bob (ID: KV0RHA, Balance: 1500.00)  
✔ Created Player: Charlie (ID: QQK3OL, Balance: 1200.00)

List of all players after creation:
           Players
┏━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┓
┃ ID     ┃ Name    ┃ Balance ┃
┡━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━┩
│ X9Z980 │ Alice   │ 1000.00 │
│ KV0RHA │ Bob     │ 1500.00 │
│ QQK3OL │ Charlie │ 1200.00 │
└────────┴─────────┴─────────┘

✔ Updated Player: Bobby (ID: KV0RHA, Balance: 1800.00)

✔ Deleted Player: Charlie (ID: QQK3OL)

Final list of players:
   Players After Deletion   
┏━━━━━━━━┳━━━━━━━┳━━━━━━━━━┓
┃ ID     ┃ Name  ┃ Balance ┃
┡━━━━━━━━╇━━━━━━━╇━━━━━━━━━┩
│ X9Z980 │ Alice │ 1000.00 │
│ KV0RHA │ Bobby │ 1800.00 │
└────────┴───────┴─────────┘


=== Player History ===
Pushed action -> 'Alice: Logged in': OK
Pushed action -> 'Alice: Deposited $500': OK
Pushed action -> 'Alice: Bet $200 on Tragamonedas': OK

Alice's history after pushes:
              Alice's History
┏━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Index ┃ Action                          ┃
┡━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│     1 │ Alice: Logged in                │
│     2 │ Alice: Deposited $500           │
│     3 │ Alice: Bet $200 on Tragamonedas │
└───────┴─────────────────────────────────┘

Popped action: Alice: Bet $200 on Tragamonedas
Alice's history after pop:
   Alice's History (After Pop)   
┏━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Index ┃ Action                ┃
┡━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━┩
│     1 │ Alice: Logged in      │
│     2 │ Alice: Deposited $500 │
└───────┴───────────────────────┘


=== Waiting Queue ===
The JSON file "./pybet/data/queue.json" is empty
Enqueuing players A, B, Alice:
     Current Queue      
┏━━━━━━━━━━┳━━━━━━━━━━━┓
┃ Position ┃ Player ID ┃
┡━━━━━━━━━━╇━━━━━━━━━━━┩
│        1 │ A         │
│        2 │ B         │
│        3 │ X9Z980    │
└──────────┴───────────┘
Peek front: A
Dequeued: A
Dequeued: B
 Queue After 2 Dequeues 
┏━━━━━━━━━━┳━━━━━━━━━━━┓
┃ Position ┃ Player ID ┃
┡━━━━━━━━━━╇━━━━━━━━━━━┩
│        1 │ X9Z980    │
└──────────┴───────────┘
Cleared queue. Now: []


=== Optimal Betting Path (Backtracking) ===
                        Optimal Betting Path
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Initial Balance ┃ Bet Options     ┃ Best Sequence   ┃ Total Used ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│             100 │ [5, 10, 20, 50] │ [5, 10, 20, 50] │         85 │
└─────────────────┴─────────────────┴─────────────────┴────────────┘


=== Gameplay Simulation ===

-- Tragamonedas Play --
Manual Test: Run play_slot(manager) and follow prompts.

-- Adivinanzas Play --
Manual Test: Run play_guessing(manager) and follow prompts.


=== Generating Reports ===

-- Top Balances Report --
         Top Balances
┏━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━┓
┃ Posición ┃ Nombre ┃   Saldo ┃
┡━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━┩
│        1 │ Bobby  │ 1800.00 │
│        2 │ Alice  │ 1000.00 │
└──────────┴────────┴─────────┘
→ Guardado en ./pybet/data/reports/top_balances.json y ./pybet/data/reports/top_balances.csv

-- Earnings Ranking Report --
     Ranking de Ganancias      
┏━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━┓
┃ Posición ┃ Nombre ┃   Saldo ┃
┡━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━┩
│        1 │ Bobby  │ 1800.00 │
│        2 │ Alice  │ 1000.00 │
└──────────┴────────┴─────────┘
→ Guardado en ./pybet/data/reports/earnings_ranking.json y ./pybet/data/reports/earnings_ranking.csv

-- Player History Report (Alice) --
Manual Test: Run _report_player_history(manager) and enter: X9Z980 when prompted.


-- Loss Counts Report --
         Ranking de Pérdidas
┏━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ Posición ┃ Nombre ┃ Cant. Pérdidas ┃
┡━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│        1 │ Alice  │              0 │
│        2 │ Bobby  │              0 │
└──────────┴────────┴────────────────┘
→ Guardado en ./pybet/data/reports/loss_counts.json y ./pybet/data/reports/loss_counts.csv

-- Game Participation Report --
  Participación por Juego  
┏━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Juego        ┃ Cantidad ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ Tragamonedas │        0 │
│ Adivinanzas  │        0 │
└──────────────┴──────────┘
→ Guardado en ./pybet/data/reports/game_participation.json y ./pybet/data/reports/game_participation.csv
→ Guardado en ./pybet/data/reports/game_participation.json y ./pybet/data/reports/game_participation.csv

All reports generated in directory: d:\UNIVERSIDAD\SEMESTRE_3\tecnicas-de-programacion\0-final-project\casino\pybet\data\reports

=== Exporting Alice's History Manually ===
Alice's history exported → d:\UNIVERSIDAD\SEMESTRE_3\tecnicas-de-programacion\0-final-project\casino\pybet\data\reports\history_X9Z980.json,
d:\UNIVERSIDAD\SEMESTRE_3\tecnicas-de-programacion\0-final-project\casino\pybet\data\reports\history_X9Z980.csv

✅ Example script completed. Please verify outputs above and check data/reports/ for generated files.
```