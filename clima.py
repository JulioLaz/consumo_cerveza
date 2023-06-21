from flask import Flask, render_template, request
import requests

app = Flask(__name__, static_folder='static')

consumo_mean= 25401.3671232876

@app.route('/', methods=['GET', 'POST'])
def index():
    global datos_climaticos
    if request.method == 'POST':
        if 'enviar' in request.form:
            # x3 = int(request.form.get('x3'))

        # Obtener los datos del formulario
            pais = request.form['pais']
            provincia = request.form['provincia']
            lluvia = request.form['lluvia']
            x3 = int(request.form.get('x3'))


            # Obtener los datos climáticos utilizando la API de OpenWeatherMap
            clave_api = 'c796a4ed594d8361bc09614d8ef0ca65'
            url = f'http://api.openweathermap.org/data/2.5/weather?q={provincia},{pais}&appid={clave_api}&units=metric&lang=es'
            response = requests.get(url)
            datos_climaticos = response.json()

               
            def calcular():

                  x1=datos_climaticos['main']['temp']
                  x2=int(request.form['lluvia'])
                  x3 = int(request.form.get('x3'))

      

                  coeficientes = [[5951.97633931], [684.73675898], [-60.7824355], [5401.08333866]]
                  if x3==1:
                     consumo_hoy = round(coeficientes[0][0] + x1 * coeficientes[1][0] + x2 * coeficientes[2][0]+ coeficientes[3][0])
                     num=(consumo_hoy - consumo_mean)*100 / consumo_mean
                     consumo = float("{}".format(round(num, 2)))

                  elif x3==0: 
                     consumo_hoy = round(coeficientes[0][0] + x1 * coeficientes[1][0] + x2 * coeficientes[2][0])
                     num=(consumo_hoy - consumo_mean)*100/consumo_mean
                     consumo = float("{}".format(round(num, 2)))

                  # Pasar el resultado a la plantilla de resultado
                  return consumo
        
        # Renderizar la plantilla con los datos climáticos
        return render_template('sitio/resultado.html', datos_climaticos=datos_climaticos,consumo=calcular(),pais=pais, provincia=provincia, lluvia=lluvia, x3=x3)
    else:
        return render_template('sitio/index.html')

@app.route('/resultado')
def resultado():
   return render_template('sitio/resultado.html')

if __name__ == '__main__':
    app.run()
