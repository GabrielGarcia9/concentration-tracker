import time
from datetime import datetime
import threading

class TemporizadorTimer:
    def __init__(self, duration: int, db):
        self.duration = duration  # duración en segundos
        self.elapsed_time = 0
        self.stop_event = threading.Event() 
        self.input_event = threading.Event()
        
        self.db = db

    def start(self, concentration_type_id, subconcentration_type_id):
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"Temporizador iniciado a las {start_time}. Tiempo de concentración durante {self.duration // 60} minutos...")
        
        timer_thread = threading.Thread(target = self._run_timer)
        timer_thread.start()

        input_thread = threading.Thread(target = self._check_for_exit)
        input_thread.daemon = True
        input_thread.start()

        timer_thread.join()

        self.input_event.set()
        
        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\nTemporizador terminado a las {end_time}.")

        self.db.add_session(start_time, end_time, concentration_type_id, subconcentration_type_id)

    def _run_timer(self):
        interval = 1  
        while self.elapsed_time < self.duration and not self.stop_event.is_set():
            time.sleep(interval)
            self.elapsed_time += 1
            remaining_time = self.duration - self.elapsed_time * interval
            total_ticks = self.duration // interval
           
            mins, secs = divmod(remaining_time, 60)
            time_format = '{:02d}:{:02d}'.format(mins, secs)

            # Actualizar barra de progreso
            progress = (self.elapsed_time / total_ticks) * 100
            progress_bar = '#' * (self.elapsed_time * 40 // total_ticks)  # Barra de progreso con longitud de 40 caracteres
            print(f"\r[{progress_bar:<40}] {progress:.2f}% - Tiempo restante: {time_format}. Ingrese 'q' para detener el temporizador: ", end="")

            
        if self.elapsed_time >= self.duration:
            print("\n¡Tiempo terminado!")

        elif self.stop_event.is_set():
            print("\n¡Tiempo interrumpido!")

    def _check_for_exit(self):
        while not self.stop_event.is_set() and not self.input_event.is_set():
            if self.input_event.is_set():
                break
            try:
                user_input = input("Ingrese 'q' para continuar.")
                if user_input.lower() == 'q':
                    self.stop_event.set() 
                    break
                else:
                    print("Entrada invalida. Solo 'q' para detener el temporizador.")
            except EOFError:
                break

        


