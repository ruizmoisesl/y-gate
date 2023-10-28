from flask import Flask, render_template, request, redirect , url_for, session, flash
from flask_mysqldb import MySQL
import secrets
import os
import base64

app= Flask(__name__)

IMG_FOLDER= os.path.join('static', 'IMG')

app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= '1234567'
app.config['MYSQL_DB']= 'ygate'
app.static_url_path = '/static'
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['UPLOAD_FOLDER']= IMG_FOLDER


ygatelogo= os.path.join(app.config['UPLOAD_FOLDER'], "Y'GATE logo.png")
ygate= os.path.join(app.config['UPLOAD_FOLDER'], "ygate.png")
carrusel1= os.path.join(app.config['UPLOAD_FOLDER'], "Y'GATE logo.pgn")
carrusel2= os.path.join(app.config['UPLOAD_FOLDER'], "Y'GATE logo.png")
carrusel3= os.path.join(app.config['UPLOAD_FOLDER'], "Y'GATE logo.png")
carrusel4= os.path.join(app.config['UPLOAD_FOLDER'], "Y'GATE logo.png")
menu= os.path.join(app.config['UPLOAD_FOLDER'], "menu.svg")
pan= os.path.join(app.config['UPLOAD_FOLDER'], "pan.jpg")
gatos= os.path.join(app.config['UPLOAD_FOLDER'], "gatos.jpg")
postre= os.path.join(app.config['UPLOAD_FOLDER'], "postre.jpg")
ropa= os.path.join(app.config['UPLOAD_FOLDER'], "ropa.jpg")
hambur= os.path.join(app.config['UPLOAD_FOLDER'], "hambur.jpg")
grani= os.path.join(app.config['UPLOAD_FOLDER'], "grani.jpg")
ara= os.path.join(app.config['UPLOAD_FOLDER'], "ara.jpg")
jumbo= os.path.join(app.config['UPLOAD_FOLDER'], "jumbo.jpg")
exito= os.path.join(app.config['UPLOAD_FOLDER'], "exito.jpg")
olimpica= os.path.join(app.config['UPLOAD_FOLDER'], "olimpica.jpg")
colanta= os.path.join(app.config['UPLOAD_FOLDER'], "colanta.jpg")
d1= os.path.join(app.config['UPLOAD_FOLDER'], "d1.jpg")
caru= os.path.join(app.config['UPLOAD_FOLDER'], "caru.jpg")
user= os.path.join(app.config['UPLOAD_FOLDER'], "user.jpg")


mysql=MySQL(app)



@app.route('/')
def principal():
    return render_template('principal.html', logo_image= ygatelogo , carrusel1= carrusel1 ,carrusel2= carrusel2 ,carrusel3= carrusel3,carrusel4= carrusel4  )

@app.route('/suscribirse')
def suscribirse():
    return render_template('suscribirse.html',logo_imag= ygatelogo)

@app.route('/registro_cliente')
def re_cliente():
    return render_template('registro-cliente.html', logo_image= ygatelogo)

@app.route('/registrop', methods= ['POST'])
def cliente():
    if request.method == 'POST':
        nombre= request.form['name']
        nombreUsu= request.form['nameuser']
        password= request.form['password']
        passwordr= request.form['passwordr']
        cursor= mysql.connection.cursor()
        cursor.execute('INSERT INTO usuario (nombre, nombreUsu, contraseña) VALUES (%s, %s, %s)',(nombre,nombreUsu,password))
        mysql.connection.commit()
        return redirect(url_for('interfaz'))
    
@app.route('/interfaz')
def interfaz():
   return render_template('interfaz-usuario.html', logo_image= ygatelogo ,user=user,menu= menu, ropa= ropa , gatos= gatos , pan= pan , postre=postre ,hambur= hambur, grani= grani, ara=ara, olimpica=olimpica,exito=exito,colanta=colanta, jumbo=jumbo , d1=d1, caru=caru)


@app.route('/iniciar_sesion')
def iniciar_sesion():
    return render_template('iniciar_sesion.html', logo_image= ygate)

@app.route('/sesion', methods=['POST'])
def iniciarsesion():
    if request.method == 'POST':
        email = request.form['correo']
        contraseña = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM usuario WHERE correo_electronico = %s  AND contraseña = %s', (email, contraseña))
        user = cursor.fetchone()
        
        if user:
            session['correo_electronico'] = email
            return redirect(url_for('planes'))
        else:
            return 'inicio de sesion no valido'
    
    return render_template('iniciar_sesion.html')

@app.route('/sesion_empresa')
def sesion_empresa():
    return render_template('login_empresa.html', logo_image= ygate)

@app.route('/loginempresa', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['correo']
        contraseña = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM empresas WHERE correo = %s  AND contraseña = %s', (email, contraseña))
        user = cursor.fetchone()
        
        if user:
            nombre=session['nombre_empresa']
            return redirect(url_for('add_producto'))
        else:
            return 'inicio de sesion no valido'
    
    return render_template('iniciar_sesion.html')



@app.route('/planes')
def planes():
    return render_template('planes.html' ,logo_imag= ygatelogo)


@app.route('/cerrar_sesion', methods=['POST'])
def cerrar_sesion():
    if 'nombreUsu' in session:
        session.pop('nombreUsu', None)
    return redirect(url_for('principal'))

@app.route('/registro_empresa')
def empresa():
    return render_template('registro-empresa.html', logo_imag= ygatelogo)

@app.route('/rempresa', methods= ['POST'])
def rempresa():
    if request.method == 'POST' :
        propietario=request.form['propietario']
        nombre_empresa=request.form['nombre_empresa']
        correo= request.method['correo']
        contraseña= request.form['contraseña']
        contraseñar= request.form['contraseñar']
        logo= request.files['logo_empresa']
        
        if contraseña == contraseñar:
            cursor= mysql.connection.cursor()
            cursor.execute('INSERT INTO empresa(nombre_empresa, nombre_propietario, correo,contraseña) VALUES (%s,%s,%s,%s)',(nombre_empresa, propietario,correo,contraseña ))
            cursor.commit()
            return redirect(url_for('interfaz'))
        else:
            flash('las contraseñas no coinciden. vuelve a intentar')
            return redirect(url_for('empresa'))

@app.route('/add_producto')
def add_producto():
    return render_template('agregar_producto.html', llgate=ygate )

@app.route('/agregar', methods=['POST'])
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        cantidad = request.form['cantidad']
    
    imagen= None

    if 'imagen' in request.files:
       imagen = request.files['imagen']
       
    if imagen:
        ruta_de_la_imagen = "static/imgDB" + imagen.filename
        imagen.save(ruta_de_la_imagen)

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO productos (nombre, precio, cantidad, imagen) VALUES (%s, %s, %s, %s)",(nombre, precio, cantidad, ruta_de_la_imagen))
        mysql.connection.commit()
        cur.close()

    return redirect(url_for('add_producto'))


@app.route('/interfaz_empresa')
def interfaz_empresa():
    return render_template('interfaz-empresa.html')
        
if __name__ == '__main__':
    app.run(debug=True)
