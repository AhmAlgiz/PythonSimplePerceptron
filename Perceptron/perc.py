from tkinter import *
from os import listdir

dir = 'my/dir/...'

def read(dir):
    with open(dir, 'r') as f:
        data = f.read().replace('\n', ' ').split(sep = ' ')
        for i in range(len(data)):
            data[i] = int(data[i])
        return data

def write(dir, weights):
    with open(dir, 'w') as file:
        for i in range(5):
            for j in range(5):
                file.write(f'{weights[5*i+j]}')
                if j != 4: 
                    file.write(' ')
            if i != 4: 
                file.write('\n')
      

class Perc(object):
    def __init__(self):
        self.weights = read(f'{dir}weights.txt')
        self.sum = 0
        self.res = []
        self.limit = 22
        self.stages = 0

    def add_weights(self, data):
        for i in range(25):
            self.weights[i] += data[i]

    def reduce_weights(self, data):
        for i in range(25):
            self.weights[i] -= data[i]

    def multiply_and_sum(self, data):
        self.sum = 0
        for i in range(25):
            self.sum += self.weights[i] * data[i]

    def save_weights(self):
        write(f'{dir}weights.txt',self.weights)

    def study_samples(self):
        self.weights = read(f'{dir}weights.txt')
        while (True):
            temp = self.weights.copy()
            for i in range(len(listdir(f'{dir}samples/good/'))):
                sample = read(f'{dir}/samples/good/{i}.txt')
                self.multiply_and_sum(sample)
                if self.sum < self.limit:
                    self.add_weights(sample)

            for i in range(len(listdir(f'{dir}samples/bad/'))):
                sample = read(f'{dir}samples/bad/{i}.txt')
                self.multiply_and_sum(sample)
                if self.sum > self.limit:
                    self.reduce_weights(sample)
            self.stages += 1
            if (set(temp) == set(self.weights)):
                break        

        self.save_weights()

    def check(self):
        self.res.clear()
        for i in range(len(listdir(f'{dir}samples/samples/'))):
            sample = read(f'{dir}samples/samples/{i}.txt')
            self.multiply_and_sum(sample)
            if self.sum > self.limit:
                self.res.append(1)
            else:
                self.res.append(0)
        with open(f'{dir}results.txt', 'w') as f:
            for i in range(len(self.res)):
                f.write(f'{i} : {self.res[i]}\n')

def run():
    perc = Perc()

    window = Tk()
    window.title('Perceptron by Ahmatzyanov')
    window.geometry('400x300')

    lbl1 = Label(window, text = '')
    lbl1.place(x = 20, y = 20)
    lbl2 = Label(window, text = '')
    lbl2.place(x = 20, y = 135)
    lbl3 = Label(window, text = 'Веса:')
    lbl3.place(x = 20, y = 5)
    lbl4 = Label(window, text = 'Результат:')
    lbl4.place(x = 20, y = 120)
    lbl5 = Label(window, text = 'Количество эпох:')
    lbl5.place(x = 20, y = 105)
    
    def click_study():
        perc.study_samples()
        lbl1.configure(text = f'{perc.weights[0:5]}\n{perc.weights[5:10]}\n{perc.weights[10:15]}\n{ perc.weights[15:20]}\n{perc.weights[20:25]}')
        lbl5.configure(text = f'Количество эпох: {perc.stages}')

    btn_study = Button(window, text = 'Обучить перцептрон', command = click_study)
    btn_study.place(x = 200, y = 20)

    def click_check():
        perc.check()
        lbl2.configure(text = f'{perc.res[0]}\n{perc.res[1]}\n{perc.res[2]}\n{ perc.res[3]}\n{perc.res[4]}\n{perc.res[5]}\n{perc.res[6]}\n{perc.res[7]}\n{perc.res[8]}\n{perc.res[9]}')

    btn_sample = Button(window, text = 'Протестировать примеры', command = click_check)
    btn_sample.place(x = 200, y = 60)
    
    def click_clear():
        perc.weights = [0,0,0,0,0, 0,0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0]
        perc.save_weights()
        perc.stages = 0
        lbl1.configure(text = f'{perc.weights[0:5]}\n{perc.weights[5:10]}\n{perc.weights[10:15]}\n{ perc.weights[15:20]}\n{perc.weights[20:25]}')

    btn_clear = Button(window, text = 'Сбросить веса', command = click_clear)
    btn_clear.place(x = 200, y = 100)

    window.mainloop()

if __name__ == '__main__':
    run()