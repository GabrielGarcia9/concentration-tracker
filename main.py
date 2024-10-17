from src.config import ConfigManager  # Importar la configuración
from src.database.database import TemporizadorDB  # Importar la base de datos
from src.notifications.notification import (
    getSondNotifyEndConcentration,
)  # Importar notificaciones
from src.timer.timer import TemporizadorTimer  # Importar el temporizador
from src.ui.print_menu import (
    print_menu_general,
    print_menu_concetracion,
    print_menu_estudio,
    print_menu_meditacion,
    print_menu_ejercicio_fisico,
    print_menu_trabajo,
    print_despedida,
)
from src.utils.utils import (
    generate_grouped_data,
    generate_combined_line_plots,
    generate_subgroup_plots,
)  # Importar funciones utilitarias


def iniciar_y_añadir_time_in_db(time, id_1, id_2):
    db = TemporizadorDB()
    config_manager = ConfigManager()
    temporizador = TemporizadorTimer(config_manager.config[time], db)
    temporizador.start(id_1, id_2)
    getSondNotifyEndConcentration()
    db.close()


def main():
    Fin = False

    while not Fin:

        print_menu_general()
        opc = int(input("Ingresar opcion:"))

        if opc == 1:
            print_menu_concetracion()
            tipe_concentration = int(input("Ingresar tipo:"))

            if tipe_concentration == 1:  # Estudio
                print_menu_estudio()
                materia = int(input("Ingresar materia:"))
                if materia == 1:  # Idiomas
                    iniciar_y_añadir_time_in_db("study_duration", 1, 1)
                elif materia == 2:  # Desarrollo de software
                    iniciar_y_añadir_time_in_db("study_duration", 1, 2)

                elif materia == 3:  # Matemáticas aplicadas
                    iniciar_y_añadir_time_in_db("study_duration", 1, 9)
                elif materia == 4:  # Inteligencia artificial ap. automático
                    iniciar_y_añadir_time_in_db("study_duration", 1, 10)
                elif materia == 5:  # Otros
                    iniciar_y_añadir_time_in_db("study_duration", 1, 11)

                elif materia == 6:
                    continue

            elif tipe_concentration == 2:
                print_menu_meditacion()
                opc = int(input("Ingresar tipo de meditación:"))
                if opc == 1:  # Visspassana  codigo 3
                    iniciar_y_añadir_time_in_db("meditation_duration", 2, 3)
                elif opc == 2:  # Fulmindnes codigo 4
                    iniciar_y_añadir_time_in_db("meditation_duration", 2, 4)
                elif opc == 3:
                    continue

            elif tipe_concentration == 3:
                print_menu_ejercicio_fisico()
                opc = int(input("Ingresar tipo de ejercicio físico:"))
                if opc == 1:  # Cardio codigo 5
                    iniciar_y_añadir_time_in_db("exercise_physical_duration", 3, 5)
                elif opc == 2:  # Fuerza codigo 6
                    iniciar_y_añadir_time_in_db("exercise_physical_duration", 3, 6)
                elif opc == 3:
                    continue

            elif tipe_concentration == 4:
                print_menu_trabajo()
                opc = int(input("Ingresar tipo trabajo:"))
                if opc == 1:
                    iniciar_y_añadir_time_in_db("work_duration", 4, 7)
                elif opc == 2:
                    iniciar_y_añadir_time_in_db("work_duration", 4, 8)
                elif opc == 3:
                    continue

            elif tipe_concentration == 5:
                continue

        elif opc == 2:
            db = TemporizadorDB()
            data = db.get_table_concentration_sessions()
            db.close()

            total_per_day, total_per_day_per_type, sub_grouped_data = (
                generate_grouped_data(data)
            )

            generate_combined_line_plots(total_per_day, total_per_day_per_type)
            generate_subgroup_plots(sub_grouped_data)

        elif opc == 3:
            config_manager = ConfigManager()
            print(
                f"El tiempo de estudio actual es de {config_manager.config['study_duration']/60} minutos."
            )
            print(
                f"El tiempo de meditación actual es de {config_manager.config['meditation_duration']/60} minutos."
            )
            print(
                f"El tiempo de ejercicio físico actual es de {config_manager.config['exercise_physical_duration']/60} minutos."
            )
            print(
                f"El tiempo de trabajo actual es de {config_manager.config['work_duration']/60} minutos."
            )

            print(
                """Opciones de configuración:
                  1) Cambiar tiempo de estudio
                  2) Cambiar tiempo de meditación
                  3) Cambiar tiempo de ejercicio físico 
                  4) Cambiar tiempo de trabajo
                  5) Regresar
                  """
            )
            opc_config = int(input("Elegir opción:"))

            if opc_config == 1:
                value = int(input("Ingresar valor en minutos:"))
                config_manager.update_config("study_duration", value * 60)
                print("¡Configuración exitosa!")

            elif opc_config == 2:
                value = int(input("Ingresar valor en minutos:"))
                config_manager.update_config("meditation_duration", value * 60)
                print("¡Configuración exitosa!")

            elif opc_config == 3:
                value = int(input("Ingresar valor en minutos:"))
                config_manager.update_config("exercise_physical_duration", value * 60)
                print("¡Configuración exitosa!")

            elif opc_config == 4:
                value = int(input("Ingresar valor en minutos:"))
                config_manager.update_config("work_duration", value * 60)
                print("¡Configuración exitosa!")
            elif opc_config == 5:
                continue

        elif opc == 4:
            Fin = True
            print_despedida()


if __name__ == "__main__":
    main()
