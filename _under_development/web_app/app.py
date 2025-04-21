import base64
from flask import Flask, render_template, request, send_file
import matplotlib.pyplot as plt
import io

app = Flask(__name__)


def calculate_savings(saving_rate, interest_rate, investment_period):
    initial_savings = 0
    savings = [initial_savings]
    years = [0]
    for year in range(1, investment_period + 1):
        savings.append(savings[-1] * (1 + interest_rate) + saving_rate)
        years.append(year)
    return years, savings


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        saving_rate = float(request.form['saving_rate'])
        interest_rate = float(request.form['interest_rate'])
        investment_period = int(request.form['investment_period'])

        years, savings = calculate_savings(saving_rate, interest_rate,
                                              investment_period)

        # Plotting the result
        fig, ax = plt.subplots()
        ax.plot(years, savings)
        ax.set(title='Savings Plan Results', xlabel='Years',
               ylabel='Total Savings')

        # Save plot to a byte buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        # Convert plot to base64 string
        plot_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

        return render_template('result.html', result=savings[-1], plot_img=plot_base64)


    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
