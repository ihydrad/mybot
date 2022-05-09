import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

first_vac_day = 30
y = np.random.randint(0, 10, first_vac_day)
date_list = [
    datetime.datetime.today() - datetime.timedelta(days=x)
    for x in range(0, first_vac_day)
    ]
plt.plot(date_list, y)
x_axis = plt.gca().xaxis
x_axis.set_major_locator(mdates.MonthLocator())
x_axis.set_major_formatter(mdates.DateFormatter('%b'))
plt.xlabel('Месяц')
plt.ylabel('Вакансии')
plt.title('Вакансии по месяцам')
plt.show()
