from flask import Flask, render_template, request
import math
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        a = complex(request.form['a'])
        b = complex(request.form['b'])
        z = complex(request.form['z'])
        w = reflection_function(a, b, z)
        n = calculate_result(z, w)

        # Create a plot
        plt.figure(figsize=(10, 5))
        # ... Your existing plot code ...
        
        # Grafik
        z_real, z_imag = np.real(z), np.imag(z)
        w_real, w_imag = np.real(w), np.imag(w)

        # chizma yaratish
        plt.figure(figsize=(10, 5))
        plt.grid(True, linestyle='--', alpha=0.5, which='both', linewidth=0.5)
        # koordinata o'lchami
        real_min=min(z_real, w_real, 0)-1
        real_max=max(z_real, w_real, 0)+1
        imag_min=min(z_imag, w_imag, 0)-1
        imag_max=max(z_imag, w_imag, 0)+1

        # haqiqiy va mavhum o'qlar
        plt.plot([real_min, real_max], [0, 0], 'k')
        plt.plot([0, 0], [imag_min, imag_max], 'k')

        # Grafik o'lchamini avtomatik qilish
        plt.xlim([real_min, real_max])
        plt.ylim([imag_min, imag_max])


        plt.quiver(0, 0, z_real, z_imag, angles='xy', scale_units='xy', scale=1, color='blue', label='z')
        plt.quiver(0, 0, w_real, w_imag, angles='xy', scale_units='xy', scale=1, color='red', label='w=a•z+b')

        # Add labels and legend
        plt.xlabel('Im(z)')
        plt.ylabel('Re(z)')
        plt.legend()
        # Save the plot to a BytesIO object
        img_data = BytesIO()
        plt.savefig(img_data, format='png')
        img_data.seek(0)
        img_base64 = base64.b64encode(img_data.read()).decode('utf-8')
        plt.close()

        # Display result and plot in the template
        return render_template('index.html', result=f'a={a}, b={b}, z={z}', result2=f'w = {w}',result3=n, plot=img_base64)

    # Display the form if it's a GET request
    return render_template('index.html')

def reflection_function(a, b, z):
    return a * z + b

def calculate_result(z, w):
    z_abs = abs(z)
    w_abs = abs(w)

    if w_abs > z_abs:
        return f"z vektor {w_abs/z_abs:.3f}... marta kattalashdi"
    elif w_abs < z_abs:
        return f"z vektor {z_abs/w_abs:.3f}... marta kichraydi"
    else:
        return "O'zgarmadi"

if __name__ == '__main__':
    app.run(debug=True)
