import sqlite3

def conectar():
    conn = sqlite3.connect("biblioteca.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            genero TEXT NOT NULL,
            estado TEXT NOT NULL  -- "leído" o "no leído"
        )
    """)
    conn.commit()
    return conn

def agregar_libro(conn):
    titulo = input("Título: ")
    autor = input("Autor: ")
    genero = input("Género: ")
    estado = input("Estado (leído/no leído): ")

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO libros (titulo, autor, genero, estado) VALUES (?, ?, ?, ?)",
        (titulo, autor, genero, estado)
    )
    conn.commit()
    print(" Libro agregado con éxito.\n")


# ---------------------------------------------------------
# Actualizar libro
# ---------------------------------------------------------
def actualizar_libro(conn):
    id_libro = input("ID del libro a actualizar: ")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM libros WHERE id = ?", (id_libro,))
    resultado = cursor.fetchone()

    if not resultado:
        print(" No existe un libro con ese ID.\n")
        return

    print("Dejá vacío un campo si no querés modificarlo.\n")

    nuevo_titulo = input(f"Título ({resultado[1]}): ") or resultado[1]
    nuevo_autor = input(f"Autor ({resultado[2]}): ") or resultado[2]
    nuevo_genero = input(f"Género ({resultado[3]}): ") or resultado[3]
    nuevo_estado = input(f"Estado ({resultado[4]}): ") or resultado[4]

    cursor.execute("""
        UPDATE libros
        SET titulo = ?, autor = ?, genero = ?, estado = ?
        WHERE id = ?
    """, (nuevo_titulo, nuevo_autor, nuevo_genero, nuevo_estado, id_libro))

    conn.commit()
    print(" Libro actualizado con éxito.\n")


# ---------------------------------------------------------
# Eliminar libro
# ---------------------------------------------------------
def eliminar_libro(conn):
    id_libro = input("ID del libro a eliminar: ")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM libros WHERE id = ?", (id_libro,))
    if not cursor.fetchone():
        print(" No existe un libro con ese ID.\n")
        return

    cursor.execute("DELETE FROM libros WHERE id = ?", (id_libro,))
    conn.commit()
    print(" Libro eliminado con éxito.\n")


# ---------------------------------------------------------
# Ver lista de libros
# ---------------------------------------------------------
def ver_libros(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM libros")
    libros = cursor.fetchall()

    if not libros:
        print(" No hay libros registrados.\n")
        return

    print("\n LISTA DE LIBROS REGISTRADOS")
    print("-" * 50)
    for libro in libros:
        print(f"ID: {libro[0]}")
        print(f"Título: {libro[1]}")
        print(f"Autor: {libro[2]}")
        print(f"Género: {libro[3]}")
        print(f"Estado: {libro[4]}")
        print("-" * 50)
    print()


# ---------------------------------------------------------
# Buscar libros
# ---------------------------------------------------------
def buscar_libros(conn):
    print("\nBuscar por:")
    print("1. Título")
    print("2. Autor")
    print("3. Género")
    opcion = input("Elegí una opción: ")

    campo = None
    if opcion == "1":
        campo = "titulo"
    elif opcion == "2":
        campo = "autor"
    elif opcion == "3":
        campo = "genero"
    else:
        print(" Opción inválida.\n")
        return

    valor = input(f"Ingresá el {campo}: ")

    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM libros WHERE {campo} LIKE ?", ("%"+valor+"%",))
    resultados = cursor.fetchall()

    if not resultados:
        print(" No se encontraron coincidencias.\n")
        return

    print("\n RESULTADOS DE BÚSQUEDA")
    print("-" * 50)
    for libro in resultados:
        print(f"ID: {libro[0]}")
        print(f"Título: {libro[1]}")
        print(f"Autor: {libro[2]}")
        print(f"Género: {libro[3]}")
        print(f"Estado: {libro[4]}")
        print("-" * 50)
    print()


# ---------------------------------------------------------
# Menú principal
# ---------------------------------------------------------
def menu():
    con = conectar()

    while True:
        print("===== BIBLIOTECA PERSONAL =====")
        print("1. Agregar libro")
        print("2. Actualizar libro")
        print("3. Eliminar libro")
        print("4. Ver libros")
        print("5. Buscar libros")
        print("6. Salir")
        opcion = input("Elegí una opción: ")

        if opcion == "1":
            agregar_libro(con)
        elif opcion == "2":
            actualizar_libro(con)
        elif opcion == "3":
            eliminar_libro(con)
        elif opcion == "4":
            ver_libros(con)
        elif opcion == "5":
            buscar_libros(con)
        elif opcion == "6":
            print("👋 Saliendo...")
            con.close()
            break
        else:
            print(" Opción inválida. Intentá nuevamente.\n")


# ---------------------------------------------------------
# Ejecución
# ---------------------------------------------------------
if __name__ == "__main__":
    menu()