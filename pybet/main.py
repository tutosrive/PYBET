from pybet.menus.PlayerMenu import manage_players
from pybet.menus.GameMenu import play_games
from pybet.menus.HistoryMenu import view_history
from pybet.menus.QueueMenu import manage_queue
from pybet.menus.BacktrackingMenu import optimal_betting_path
from pybet.menus.ReportsMenu import generate_reports

def main():
    while True:
        print("\n=== Menú Principal ===")
        print("1. Gestionar Jugadores")
        print("2. Jugar")
        print("3. Ver Historial")
        print("4. Manejar Cola de Espera")
        print("5. Camino Óptimo de Apuestas")
        print("6. Generar Reportes")
        print("0. Salir")

        choice = input("Seleccione una opción: ").strip()

        if choice == '1':
            manage_players()
        elif choice == '2':
            play_games()
        elif choice == '3':
            view_history()
        elif choice == '4':
            manage_queue()
        elif choice == '5':
            optimal_betting_path()
        elif choice == '6':
            generate_reports()
        elif choice == '0':
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida, intente de nuevo.")

if __name__ == '__main__':
    main()