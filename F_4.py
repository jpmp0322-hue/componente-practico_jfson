
from abc import ABC, abstractmethod
from datetime import datetime
import logging
import re



# 1. CONFIGURACION DEL ARCHIVO DE REGISTRO


logging.basicConfig(
    filename="software_fj.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)



# 2. EXCEPCIONES PERSONALIZADAS


class ErrorSoftwareFJ(Exception):
    """Excepcion general del sistema."""
    pass


class DatosInvalidosError(ErrorSoftwareFJ):
    pass


class ClienteNoEncontradoError(ErrorSoftwareFJ):
    pass


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    pass


class ReservaInvalidaError(ErrorSoftwareFJ):
    pass


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    pass



# 3. CLASE ABSTRACTA ENTIDAD


class Entidad(ABC):

    def __init__(self, identificacion):
        if not identificacion:
            raise DatosInvalidosError(
                "La identificacion es obligatoria."
            )

        self._identificacion = str(identificacion)

    @property
    def identificacion(self):
        return self._identificacion

    @abstractmethod
    def mostrar_informacion(self):
        pass



# 4. CLASE CLIENTE


class Cliente(Entidad):

    def __init__(self, identificacion, nombre, correo, telefono):
        super().__init__(identificacion)

        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise DatosInvalidosError(
                "El nombre debe tener minimo 3 caracteres."
            )
        self._nombre = valor.strip()

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str) or not re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+", valor
        ):
            raise DatosInvalidosError("Correo electronico invalido.")
        self._correo = valor

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        if not str(valor).isdigit() or len(str(valor)) < 7:
            raise DatosInvalidosError("Telefono invalido.")
        self._telefono = str(valor)

    def mostrar_informacion(self):
        return (
            f"ID: {self.identificacion} | "
            f"Nombre: {self.nombre} | "
            f"Correo: {self.correo} | "
            f"Telefono: {self.telefono}"
        )



# 5. CLASE ABSTRACTA SERVICIO


class Servicio(ABC):

    def __init__(self, codigo, nombre, tarifa):
        if not codigo or not nombre:
            raise DatosInvalidosError(
                "El codigo y nombre del servicio son obligatorios."
            )

        if not isinstance(tarifa, (int, float)) or tarifa <= 0:
            raise DatosInvalidosError("La tarifa debe ser positiva.")

        self.codigo = codigo
        self.nombre = nombre
        self.tarifa = tarifa
        self.disponible = True

    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        pass

    @abstractmethod
    def describir_servicio(self):
        pass

    @abstractmethod
    def validar_parametros(self, duracion):
        pass



# 6. SERVICIO DE RESERVA DE SALAS


class ServicioSala(Servicio):

    def __init__(self, codigo, nombre, tarifa, capacidad):
        super().__init__(codigo, nombre, tarifa)

        if not isinstance(capacidad, int) or capacidad <= 0:
            raise DatosInvalidosError("Capacidad de sala invalida.")

        self.capacidad = capacidad

    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatosInvalidosError("Duracion de reserva invalida.")

    # Sobrecarga simulada mediante parametros opcionales
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        self.validar_parametros(duracion)

        if not 0 <= impuesto <= 100:
            raise DatosInvalidosError("Impuesto invalido.")

        if not 0 <= descuento <= 100:
            raise DatosInvalidosError("Descuento invalido.")

        subtotal = self.tarifa * duracion
        total = subtotal + (subtotal * impuesto / 100)
        total -= total * descuento / 100

        return round(total, 2)

    def describir_servicio(self):
        return (
            f"Sala: {self.nombre} | "
            f"Capacidad: {self.capacidad} personas | "
            f"Tarifa por hora: ${self.tarifa}"
        )



# 7. SERVICIO DE ALQUILER DE EQUIPOS


class ServicioEquipo(Servicio):

    def __init__(self, codigo, nombre, tarifa, cantidad):
        super().__init__(codigo, nombre, tarifa)

        if not isinstance(cantidad, int) or cantidad < 0:
            raise DatosInvalidosError("Cantidad de equipos invalida.")

        self.cantidad = cantidad

    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatosInvalidosError("Duracion de alquiler invalida.")

        if self.cantidad <= 0:
            raise ServicioNoDisponibleError(
                "No hay equipos disponibles."
            )

    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        self.validar_parametros(duracion)

        if not 0 <= impuesto <= 100 or not 0 <= descuento <= 100:
            raise DatosInvalidosError("Impuesto o descuento invalido.")

        subtotal = self.tarifa * duracion
        total = subtotal * (1 + impuesto / 100)
        total = total * (1 - descuento / 100)

        return round(total, 2)

    def describir_servicio(self):
        return (
            f"Equipo: {self.nombre} | "
            f"Disponibles: {self.cantidad} | "
            f"Tarifa por hora: ${self.tarifa}"
        )



# 8. SERVICIO DE ASESORIAS ESPECIALIZADAS


class ServicioAsesoria(Servicio):

    def __init__(self, codigo, nombre, tarifa, especialidad):
        super().__init__(codigo, nombre, tarifa)

        if not isinstance(especialidad, str) or not especialidad.strip():
            raise DatosInvalidosError("Especialidad obligatoria.")

        self.especialidad = especialidad

    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatosInvalidosError("Duracion de asesoria invalida.")

    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        self.validar_parametros(duracion)

        if not 0 <= impuesto <= 100 or not 0 <= descuento <= 100:
            raise DatosInvalidosError("Impuesto o descuento invalido.")

        subtotal = self.tarifa * duracion
        total = subtotal * (1 + impuesto / 100)
        total *= (1 - descuento / 100)

        return round(total, 2)

    def describir_servicio(self):
        return (
            f"Asesoria: {self.nombre} | "
            f"Especialidad: {self.especialidad} | "
            f"Tarifa por hora: ${self.tarifa}"
        )



# 9. CLASE RESERVA


class Reserva:

    def __init__(self, codigo, cliente, servicio, duracion):
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("Cliente no valido.")

        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("Servicio no valido.")

        servicio.validar_parametros(duracion)

        self.codigo = codigo
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"
        self.costo = 0

    def confirmar(self, impuesto=0, descuento=0):

        if self.estado != "Pendiente":
            raise OperacionNoPermitidaError(
                "La reserva no se encuentra pendiente."
            )

        if not self.servicio.disponible:
            raise ServicioNoDisponibleError(
                "El servicio no esta disponible."
            )

        self.costo = self.servicio.calcular_costo(
            self.duracion, impuesto, descuento
        )

        if isinstance(self.servicio, ServicioEquipo):
            if self.servicio.cantidad <= 0:
                raise ServicioNoDisponibleError(
                    "No quedan equipos disponibles."
                )
            self.servicio.cantidad -= 1

        self.estado = "Confirmada"

        logging.info(
            f"Reserva {self.codigo} confirmada. "
            f"Costo: ${self.costo}"
        )

        return self.costo

    def cancelar(self):

        if self.estado != "Confirmada":
            raise OperacionNoPermitidaError(
                "Solo se pueden cancelar reservas confirmadas."
            )

        if isinstance(self.servicio, ServicioEquipo):
            self.servicio.cantidad += 1

        self.estado = "Cancelada"

        logging.info(f"Reserva {self.codigo} cancelada.")

    def procesar(self):
        try:
            if self.estado != "Confirmada":
                raise OperacionNoPermitidaError(
                    "No se puede procesar una reserva sin confirmar."
                )

            print(f"Procesando reserva {self.codigo}...")
            print(f"Cliente: {self.cliente.nombre}")
            print(f"Servicio: {self.servicio.nombre}")
            print(f"Costo total: ${self.costo}")

        except ErrorSoftwareFJ as error:
            logging.error(
                f"Error al procesar reserva {self.codigo}: {error}"
            )
            raise

    def mostrar_reserva(self):
        return (
            f"Reserva: {self.codigo} | "
            f"Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Duracion: {self.duracion} horas | "
            f"Estado: {self.estado} | "
            f"Costo: ${self.costo}"
        )


# 10. CLASE PRINCIPAL DE GESTION


class GestorSoftwareFJ:

    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, cliente):

        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("Objeto cliente incorrecto.")

        if any(c.identificacion == cliente.identificacion
               for c in self.clientes):
            raise DatosInvalidosError("El cliente ya esta registrado.")

        self.clientes.append(cliente)
        logging.info(f"Cliente registrado: {cliente.nombre}")
        return True

    def registrar_servicio(self, servicio):

        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("Tipo de servicio incorrecto.")

        if any(s.codigo == servicio.codigo for s in self.servicios):
            raise DatosInvalidosError("Codigo de servicio duplicado.")

        self.servicios.append(servicio)
        logging.info(f"Servicio registrado: {servicio.nombre}")
        return True

    def crear_reserva(self, codigo, id_cliente, codigo_servicio, duracion):

        try:
            cliente = next(
                (c for c in self.clientes
                 if c.identificacion == str(id_cliente)),
                None
            )

            if cliente is None:
                raise ClienteNoEncontradoError(
                    f"No existe el cliente {id_cliente}."
                )

            servicio = next(
                (s for s in self.servicios
                 if s.codigo == codigo_servicio),
                None
            )

            if servicio is None:
                raise ServicioNoDisponibleError(
                    f"No existe el servicio {codigo_servicio}."
                )

            if any(r.codigo == codigo for r in self.reservas):
                raise ReservaInvalidaError(
                    "El codigo de reserva ya existe."
                )

            reserva = Reserva(
                codigo, cliente, servicio, duracion
            )

            self.reservas.append(reserva)

            logging.info(f"Reserva creada: {codigo}")
            return reserva

        except ErrorSoftwareFJ as error:
            logging.error(f"Error creando reserva: {error}")
            raise

    def buscar_cliente(self, identificacion):

        for cliente in self.clientes:
            if cliente.identificacion == str(identificacion):
                return cliente

        raise ClienteNoEncontradoError(
            "Cliente no encontrado."
        )

    def listar_clientes(self):
        for cliente in self.clientes:
            print(cliente.mostrar_informacion())

    def listar_servicios(self):
        for servicio in self.servicios:
            print(servicio.describir_servicio())

    def listar_reservas(self):
        for reserva in self.reservas:
            print(reserva.mostrar_reserva())



# 11. PROGRAMA PRINCIPAL Y PRUEBAS


def ejecutar_pruebas():

    sistema = GestorSoftwareFJ()

    print("\n==================================")
    print("       SISTEMA SOFTWARE FJ")
    print("====================================")

    # OPERACION 1: Registrar cliente valido
    print("\nOPERACION 1: Registrar cliente")

    try:
        cliente1 = Cliente(
            "1001",
            "Carlos Ramirez",
            "carlos@gmail.com",
            "3001234567"
        )

        sistema.registrar_cliente(cliente1)
        print("Cliente registrado correctamente.")

    except ErrorSoftwareFJ as error:
        logging.error(f"Operacion 1: {error}")
        print("Error:", error)

    # OPERACION 2: Registrar otro cliente
    print("\nOPERACION 2: Registrar segundo cliente")

    try:
        cliente2 = Cliente(
            "1002",
            "Maria Torres",
            "maria@gmail.com",
            "3101234567"
        )

        sistema.registrar_cliente(cliente2)
        print("Segundo cliente registrado.")

    except ErrorSoftwareFJ as error:
        logging.error(f"Operacion 2: {error}")
        print("Error:", error)

    # OPERACION 3: Intentar registrar cliente invalido
    print("\nOPERACION 3: Cliente con correo invalido")

    try:
        cliente3 = Cliente(
            "1003",
            "Pedro Lopez",
            "correo_incorrecto",
            "3201234567"
        )

        sistema.registrar_cliente(cliente3)

    except ErrorSoftwareFJ as error:
        logging.error(f"Operacion 3: {error}")
        print("Error controlado:", error)

    # OPERACION 4: Registrar servicio de sala
    print("\nOPERACION 4: Registrar sala")

    try:
        sala = ServicioSala(
            "S01", "Sala de reuniones", 50000, 20
        )

        sistema.registrar_servicio(sala)
        print("Sala registrada correctamente.")

    except ErrorSoftwareFJ as error:
        logging.error(f"Operacion 4: {error}")
        print("Error:", error)

    # OPERACION 5: Registrar equipos
    print("\nOPERACION 5: Registrar equipos")

    try:
        equipo = ServicioEquipo(
            "E01", "Proyector multimedia", 30000, 5
        )

        sistema.registrar_servicio(equipo)
        print("Equipo registrado correctamente.")

    except ErrorSoftwareFJ as error:
        logging.error(f"Operacion 5: {error}")
        print("Error:", error)

    # OPERACION 6: Registrar asesoria
    print("\nOPERACION 6: Registrar asesoria")

    try:
        asesoria = ServicioAsesoria(
            "A01", "Asesoria tecnologica", 80000,
            "Ingenieria de software"
        )

        sistema.registrar_servicio(asesoria)
        print("Asesoria registrada correctamente.")

    except ErrorSoftwareFJ as error:
        logging.error(f"Operacion 6: {error}")
        print("Error:", error)

    # OPERACION 7: Intentar registrar servicio invalido
    print("\nOPERACION 7: Servicio con tarifa invalida")

    try:
        servicio_invalido = ServicioSala(
            "S02", "Sala incorrecta", -1000, 10
        )

        sistema.registrar_servicio(servicio_invalido)

    except ErrorSoftwareFJ as error:
        logging.error(f"Operacion 7: {error}")
        print("Error controlado:", error)

    # OPERACION 8: Crear reserva correcta
    print("\nOPERACION 8: Crear reserva de sala")

    try:
        reserva1 = sistema.crear_reserva(
            "R001", "1001", "S01", 2
        )

        costo = reserva1.confirmar(19, 10)

        print("Reserva confirmada.")
        print("Costo final:", costo)

    except ErrorSoftwareFJ as error:
        logging.error(f"Operacion 8: {error}")
        print("Error:", error)

    # OPERACION 9: Procesar reserva
    print("\nOPERACION 9: Procesar reserva")

    try:
        reserva1.procesar()

    except ErrorSoftwareFJ as error:
        logging.error(f"Operacion 9: {error}")
        print("Error:", error)

    # OPERACION 10: Reserva con cliente inexistente
    print("\nOPERACION 10: Cliente inexistente")

    try:
        sistema.crear_reserva(
            "R002", "9999", "E01", 2
        )

    except ErrorSoftwareFJ as error:
        logging.error(f"Operacion 10: {error}")
        print("Error controlado:", error)

    # OPERACION 11: Reserva de equipo
    print("\nOPERACION 11: Reserva de equipo")

    try:
        reserva2 = sistema.crear_reserva(
            "R003", "1002", "E01", 3
        )

        reserva2.confirmar(19, 5)
        reserva2.procesar()

    except ErrorSoftwareFJ as error:
        logging.error(f"Operacion 11: {error}")
        print("Error:", error)

    # OPERACION 12: Cancelar reserva
    print("\nOPERACION 12: Cancelar reserva")

    try:
        reserva2.cancelar()
        print("Reserva cancelada correctamente.")

    except ErrorSoftwareFJ as error:
        logging.error(f"Operacion 12: {error}")
        print("Error:", error)

    # OPERACION 13: Intentar cancelar nuevamente
    print("\nOPERACION 13: Cancelacion no permitida")

    try:
        reserva2.cancelar()

    except ErrorSoftwareFJ as error:
        logging.error(f"Operacion 13: {error}")
        print("Error controlado:", error)

    # OPERACION 14: Intentar confirmar una reserva
    # con duracion incorrecta y mostrar encadenamiento
    print("\nOPERACION 14: Validacion de duracion")

    try:
        try:
            sistema.crear_reserva(
                "R004", "1001", "S01", -2
            )
        except DatosInvalidosError as causa:
            raise ReservaInvalidaError(
                "No fue posible crear la reserva."
            ) from causa

    except ReservaInvalidaError as error:
        logging.exception("Operacion 14: Error encadenado")
        print("Error controlado:", error)
        print("Causa original:", error.__cause__)

    # OPERACION 15: Bloque try/except/else/finally
    print("\nOPERACION 15: Consulta de cliente")

    try:
        cliente = sistema.buscar_cliente("1001")

    except ClienteNoEncontradoError as error:
        logging.error(f"Operacion 15: {error}")
        print("Error:", error)

    else:
        print("Consulta realizada correctamente.")
        print(cliente.mostrar_informacion())

    finally:
        print("Consulta finalizada.")

    # OPERACION 16: Bloque try/except/finally
    print("\nOPERACION 16: Calculo con impuesto y descuento")

    try:
        total = sala.calcular_costo(2, 19, 10)
        print("Costo de la sala:", total)

    except ErrorSoftwareFJ as error:
        logging.error(f"Operacion 16: {error}")
        print("Error:", error)

    finally:
        print("Proceso de calculo finalizado.")

    # INFORMACION FINAL
    print("\n====================================")
    print("       RESUMEN DEL SISTEMA")
    print("====================================")

    print("\nCLIENTES REGISTRADOS:")
    sistema.listar_clientes()

    print("\nSERVICIOS REGISTRADOS:")
    sistema.listar_servicios()

    print("\nRESERVAS REGISTRADAS:")
    sistema.listar_reservas()

    print("\nEl programa finalizo correctamente.")
    print("Los eventos y errores se guardaron en software_fj.log")



# 12. EJECUCION DEL PROGRAMA


if __name__ == "__main__":

    try:
        ejecutar_pruebas()

    except Exception:
        logging.exception("Error inesperado en el programa principal.")
        print("Se presento un error inesperado. "
              "Consulte el archivo de registros.")

