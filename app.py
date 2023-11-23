from flask import Flask
from flask import render_template, request, redirect, session, url_for, flash
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask import send_from_directory
from flask_cors import CORS
import os
import mysql.connector


app = Flask(__name__)
CORS(app)
app.secret_key = "itserviceweb" 
bcrypt = Bcrypt(app)

# Configuración de la conexión a MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="sitio"
)

cursor = db.cursor()

@app.route('/')
def inicio():
    cursor.execute("SELECT * FROM `servicios` ORDER BY id DESC LIMIT 4")
    servicios=cursor.fetchall()
    db.commit()

    cursor.execute("SELECT * FROM `clientes` ORDER BY id DESC LIMIT 6")
    clientes=cursor.fetchall()
    db.commit()
    return render_template('sitio/index.html', servicios=servicios, clientes=clientes)


@app.route('/', methods=['POST'])
def enviar_formulario():
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form['nombreContacto']
        apellido = request.form['apellidoContacto']
        correo = request.form['correoContacto']
        mensaje = request.form['mensajeContacto']

        # Insertar datos en MySQL
        sql = "INSERT INTO contacto (nombre, apellido, correo, mensaje) VALUES (%s, %s, %s, %s)"
        valores = (nombre, apellido, correo, mensaje)

        cursor.execute(sql, valores)
        db.commit()
        # Mostrar alerta de éxito
        flash('Pronto te contactaremos', 'success')

        return redirect('/')

@app.route('/admin/')
def admin_index():
    if not 'login' in session:
        return redirect("/admin/login") 
    
    return render_template('admin/index.html')


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        usuario = request.form['txtUsuario']
        contrasena = request.form['txtPassword']

        cursor.execute("SELECT * FROM usuarios WHERE usuario=%s", (usuario,))
        usuario_data = cursor.fetchone()

        if usuario_data and bcrypt.check_password_hash(usuario_data[2], contrasena):
            # Contraseña correcta
            session["login"]=True
            session['usuario_id'] = usuario_data[0]
            session["usuario"]=usuario
            return redirect('/admin/')  # Cambia a la página que prefieras después del login
        else:
            # Usuario o contraseña incorrectos
            return render_template('admin/login.html', mensaje="Usuario o Contraseña incorrecta")

    return render_template('admin/login.html')

@app.route('/admin/cerrar')
def admin_login_cerrar():
    session.clear()
    return redirect('/admin/login')

 

@app.route('/admin/servicios')
def admin_servicios():

    if not 'login' in session:
        return redirect("/admin/login")
    
    cursor.execute("SELECT * FROM `servicios`")
    servicios=cursor.fetchall()
    db.commit()
 
    return render_template('admin/servicios.html', servicios=servicios)

@app.route('/admin/cerrar')
def admin_cerrar():
    return render_template('admin/cerrar.html')

#enruta para ver la imagen
@app.route('/static/img/<imagen>')
def imagenes(imagen):
    print(imagen)

    return send_from_directory(os.path.join('static/img/'),imagen)

#guarda los servicios en el administardor
@app.route('/admin/servicios/guardar', methods=['POST'])
def admin_servicios_guardar():

    if not 'login' in session:
        return redirect("/admin/login") 
      
    _archivo=request.files['txtImagen']
    _nombre=request.form['txtNombre']
    _descripcion=request.form['txtParrafo']
    
    tiempo=datetime.now()
    horaActual=tiempo.strftime('%Y%H%M%S')

    if _archivo.filename!="":
        nuevoNombre=horaActual+"_"+_archivo.filename
        _archivo.save("static/img/"+nuevoNombre)

    sql="INSERT INTO `servicios` (`id`, `imagen`, `nombre`, `parrafo`) VALUES (NULL, %s, %s, %s);"
    datos=(nuevoNombre, _nombre, _descripcion)
    cursor.execute(sql,datos)
    db.commit()

    return redirect('/admin/servicios')

@app.route('/admin/servicios/borrar', methods=['POST'])
def admin_servicios_borrar():

    if not 'login' in session:
        return redirect("/admin/login") 
    
    _id = request.form['txtID']

    #buscamos cual es el nombre de la imagen al cual vamos a eliminar
    cursor.execute("SELECT imagen FROM `servicios` WHERE id=%s", (_id,))
    nombreImagen=cursor.fetchall()
    db.commit() 

    #y si esta se elimina
    if os.path.exists("static/img/"+str(nombreImagen[0][0])):
        os.unlink("static/img/"+str(nombreImagen[0][0]))

    cursor.execute("DELETE FROM servicios WHERE id=%s", (_id,))
    db.commit() 

    return redirect('/admin/servicios')

#consulta
@app.route('/admin/contacto')
def admin_contacto():

    if not 'login' in session:
        return redirect("/admin/login")
    print("aqui entra")
    cursor.execute("SELECT * FROM `contacto`")
    contactos=cursor.fetchall()
    db.commit()
    
    return render_template('admin/contacto.html', contactos=contactos)

@app.route('/admin/contacto', methods=['POST'])
def admin_contacto_mostrar():

    if not 'login' in session:
        return redirect("/admin/login") 
    
    _id = request.form['txtID']
    cursor.execute("SELECT * FROM `contacto`")
    contactos=cursor.fetchall()
    cursor.execute("SELECT * FROM `contacto` WHERE id=%s", (_id,))
    vercontacto=cursor.fetchall()
    
    return render_template('admin/contacto.html', vercontacto=vercontacto, contactos=contactos)


@app.route('/admin/contacto/borrar', methods=['POST'])
def admin_contacto_borrar():

    if not 'login' in session:
        return redirect("/admin/login") 
    
    _idBorrar = request.form['txtIDBorrar']

    cursor.execute("DELETE FROM contacto WHERE id=%s", (_idBorrar,))
    db.commit() 

    return redirect('/admin/contacto')


@app.route('/admin/clientes')
def admin_clientes():

    if not 'login' in session:
        return redirect("/admin/login")
    
    cursor.execute("SELECT * FROM `clientes`")
    clientes=cursor.fetchall()
    db.commit()
 
    return render_template('admin/clientes.html', clientes=clientes)


#guarda los clientes
@app.route('/admin/clientes/guardar', methods=['POST'])
def admin_clientes_guardar():

    if not 'login' in session:
        return redirect("/admin/login") 
      
    _archivo=request.files['txtImagen']
    _nombre=request.form['txtNombre']
    
    tiempo=datetime.now()
    horaActual=tiempo.strftime('%Y%H%M%S')

    if _archivo.filename!="":
        nuevoNombre=horaActual+"_"+_archivo.filename
        _archivo.save("static/img/"+nuevoNombre)

    sql="INSERT INTO `clientes` (`id`, `imagen`, `nombre`) VALUES (NULL, %s, %s);"
    datos=(nuevoNombre,_nombre)
    cursor.execute(sql,datos)
    db.commit()

    return redirect('/admin/clientes')

@app.route('/admin/clientes/borrar', methods=['POST'])
def admin_clientes_borrar():

    if not 'login' in session:
        return redirect("/admin/login") 
    
    _id = request.form['txtID']

    #buscamos cual es el nombre de la imagen al cual vamos a eliminar
    cursor.execute("SELECT imagen FROM `clientes` WHERE id=%s", (_id,))
    nombreImagen=cursor.fetchall()
    db.commit() 

    #y si esta se elimina
    if os.path.exists("static/img/"+str(nombreImagen[0][0])):
        os.unlink("static/img/"+str(nombreImagen[0][0]))

    cursor.execute("DELETE FROM clientes WHERE id=%s", (_id,))
    db.commit() 

    return redirect('/admin/clientes')

if __name__ =='__main__':
    app.run(debug=True)