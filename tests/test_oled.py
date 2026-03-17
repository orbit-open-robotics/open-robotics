from orbit import oled

if __name__ == '__main__':
    from time import sleep
    print(os.getcwd())
    oled = Oled(scl_pin = 9, sda_pin = 8)
    
    expressions = ['happy','angry','neutral','sad','scared','sleepy','surprised']
    while True:
        for expression in expressions:
            oled.draw_face(expression)
            sleep(1)