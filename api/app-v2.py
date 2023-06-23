from flask import Flask, send_file
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
import time
import io
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route('/')
def home():
    return 'Home Page Route'
    
@app.route('/run')
def run_script():
    # Configuración de Selenium
    options = Options()
    options.add_argument('--headless')  # Ejecutar Chrome en modo headless
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(options=options)

    def login():
        username_= 'pabloa@grupoinformatico.com'
        password = '123456'   

        driver.get('https://www.danston.com/')

        time.sleep(1)

        icon_login =  driver.find_element("xpath",'//*[@id="usufoto2"]').click()

        input_user = driver.find_element("xpath",'//*[@id="login_usuario"]')

        input_user.send_keys(username_)

        input_password =driver.find_element("xpath",'//*[@id="login_clave"]')

        input_password.send_keys(password)

        button_login = driver.find_element("xpath",'//*[@id="btn_login_submit"]').click()

    def parse_product(url):
        resultado_list = []
        page = 0
        found = True

        while found:
            # Construir la URL de la página actual
            current_url = url['url'] + str(page)
            # Obtener el código fuente de la página actual
            time.sleep(1)
            driver.get(current_url)
            #time.sleep(1)
            # Esperar un segundo para que se cargue la página
            html = driver.page_source        
            # Analizar el código fuente con BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")
            # Buscar el producto en el código fuente de la página actual
            products = soup.find_all("div", class_="prod_item")

            if products:
                print(f"Producto encontrado en la página {page}")
                is_pager = soup.find_all('div', class_='pager0')            
                page_data = []
                
                for product in products:

                    try:
                        name = product.select_one('h2 > a > span').text.strip()
                    except AttributeError:
                        name = 'Sin nombre'
                    try:
                        sku = product.select_one('div.prodcod > span:nth-child(2)').text.strip()
                    except AttributeError:
                        sku = 'Sin SKU'
                    try:
                        price = product.select_one('div.precio_cont > span.pprecio').get('content').strip()
                    except AttributeError:
                        price = 'Sin Precio/Stock'

                    page_data.append({'nombre': name, 'sku': sku, 'precio': price, 'category':url['category']})
                
                resultado_list.append(page_data)
                
                if(is_pager):
                    page += 1
                else:
                    print('No hay paginacion')
                    found = False

            else:
                print(f"Producto no encontrado en la página {page}")
                found = False

        return resultado_list

    def save_csv(lista_listas):
        nombre_archivo = 'lista-articulos.csv'  # Nombre de archivo fijo
        with open(nombre_archivo, 'w', newline='') as archivo_csv:
            writer = csv.writer(archivo_csv)
            writer.writerow(['Nombre', 'SKU', 'Precio', 'Categoria'])  # Escribir encabezados en el archivo CSV

            for lista in lista_listas:
                for elemento in lista:
                    nombre = elemento['nombre']
                    sku = elemento['sku']
                    precio = elemento['precio']
                    category = elemento['category']
                    writer.writerow([nombre, sku, precio,category])

    urls=[ #{'url':'https://www.danston.com/productos/productos.php?path=0.2321&secc=productos&order=2&mo=1&pagina=','category':'Cartuchos Compatibles Tinta'},
        #{'url':'https://www.danston.com/cartuchos-compatibles-laser/?secc=productos&path=0.2292&order=2&mo=1&pagina=','category':'Cartuchos Compatibles Laser'},
        #{'url':'https://www.danston.com/productos/productos.php?path=0.2463&secc=productos&order=2&mo=1&pagina=','category':'Tintas'}, 
        #{'url':'https://www.danston.com/papeles/?secc=productos&path=0.2389&order=2&mo=1&pagina=','category':'Papeles'},
        #{'url':'https://www.danston.com/cintas-compatibles/?secc=productos&path=0.2377&order=2&mo=1&pagina=','category':'Cintas compatibles'}, 
        #{'url':'https://www.danston.com/productos/productos.php?path=0.2267.2278&secc=productos','category':'Microfono'},
        #{'url':'https://www.danston.com/accesoriosperisfericos/mouses/?secc=productos&path=0.2267.2269&order=2&mo=1&pagina=','category':'Mouse'}, 
        #{'url':'https://www.danston.com/accesoriosperisfericos/teclados/?secc=productos&path=0.2267.2272&order=2&mo=1&pagina=','category':'Teclados'},
       # {'url':'https://www.danston.com/accesoriosperisfericos/settecladoymouse/','category':'Combo'}, 
       # {'url':'https://www.danston.com/smartwatch/','category':'SmartWatch'}, 
       # {'url':'https://www.danston.com/productos/productos.php?path=0.2267.2277&secc=productos&order=2&mo=1&pagina=','category':'Auriculares'},
       # {'url':'https://www.danston.com/productos/productos.php?path=0.2267.2284&secc=productos&order=2&mo=1&pagina=','category':'Cables'}, 
       # {'url':'https://www.danston.com/productos/productos.php?path=0.2267.2485&secc=productos','category':'Accesorios Celular'},
       # {'url':'https://www.danston.com/productos/productos.php?path=0.2267.2486&secc=productos&order=2&mo=1&pagina=','category':'Cargadores'}, 
        {'url':'https://www.danston.com/productos/productos.php?path=0.2267.2279&secc=productos&order=2&mo=1&pagina=','category':'Parlantes'},          
      ]

    total_data_products = []
    login()
    for url in urls:
        total_data_products += parse_product(url)
    # Generar el archivo CSV en memoria
    csv_data = io.StringIO()
    writer = csv.writer(csv_data)
    writer.writerow(['Nombre', 'SKU', 'Precio', 'Categoria'])  # Encabezados del CSV

    for lista in total_data_products:
        for elemento in lista:
            nombre = elemento['nombre']
            sku = elemento['sku']
            precio = elemento['precio']
            category = elemento['category']
            writer.writerow([nombre, sku, precio, category])

    # Crear una respuesta para enviar el archivo CSV al navegador
     # Configurar la respuesta personalizada con el archivo CSV
    response = send_file(
    io.BytesIO(csv_data.getvalue().encode('utf-8')),
    mimetype='text/csv'
    )
    response.headers["Content-Disposition"] = "attachment; filename=lista-articulos.csv"


    return response

if __name__ == '__main__':
    app.run()
