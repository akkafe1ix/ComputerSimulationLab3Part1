import math
class Calculat():
    #Одноканальная с отказами в обслуживании  
    def Single_channel_failures(self, l, tobsl):
        mu = 1/tobsl
        tprost = 1 / l
        roobs = l / (l + mu)
        rootk = 1 - roobs   
        a = l * roobs
        return round(mu, 2), round(tprost,2), round(roobs,2), round(rootk,2), round(a,2)
    
    # Одноканальная с ограниченной и неограниченной очередью
    def Single_channel_limited_or_unlimited(self, l, tobsl, n, f):
        mu = 1/tobsl
        ro = l / (l + mu)
        if not f: #f - показатель с ограниченной очередью или нет
            if ro == 1:
                r_0 = 1/(n+2)
                lq = (n*(n+1))/(2*(n+2))
            else:
                r_0 = (1-ro)/(1-ro**(n+2))
                lq = ro**2 * ((1-ro**n*(n-n*ro+1))/(1-ro)**2)    
            rootkaz = ro**(n+1)*r_0
            roobsl = 1 - rootkaz
            a = l*roobsl
            tq = lq/l
            lsmo = 1 + lq
            if ro == 1:
                tsmo = (n+1)/(2*mu)
            else:
                tsmo = lsmo/l
            return round(roobsl,2), round(rootkaz,2), round(lq,2), round(tq,2), round(lsmo,2), round(tsmo,2),round(r_0, 2)
        else:
            if ro >= 1:
                print('Режим не явлеятся стационарным')
                return False
            lq = (ro**2)/(1-ro)
            tq = lq/l
            lsmo = ro/(1-ro)
            tsmo = ro/l
            return round(lq,2),round(tq,2),round(lsmo,2),round(tsmo,2)

    # Многоканальная с отказами в обслуживании
    def Multi_channel_failures(self, l, tobsl, n):
        mu = 1/tobsl
        ro = l/mu
        ro_0 = 0
        for i in range(0, n, 1):
            ro_0 += (ro**i)/(math.factorial(i))
        ro_0 = ro_0**-1
        rootkaz = ro_0 * (ro**n)/math.factorial(n)
        roobsl = 1 - rootkaz
        a = l*roobsl
        k_ = l/mu
        return round(ro_0,2), round(rootkaz,2), round(roobsl,2),round(a,2), round(k_,2)

    #Многоканальная с ограниченной очередью 
    def Multi_channel_limited(self, l, tobsl, n, m):
        mu = 1/tobsl
        ro = l/mu
        ro_0 = 0
        if ro/n == 1:
            for k in range(0, n, 1):
                ro_0 += (ro**k)/math.factorial(k) + (m * (ro**(n+1)))/(n * math.factorial(n))
            ro_0 = ro_0**-1
            lq = (ro**(n+1)*m*(m+1)*ro_0)/(n*math.factorial(n)*2)
        else:
            for k in range(0, n, 1):
                ro_0 += (ro**k)/math.factorial(k) + (ro**(n+1))/(math.factorial(n)*(n-ro))*(1 - (ro/n)**m)
            ro_0 = ro_0**-1
            lq = (ro**(n+1))/(n*math.factorial(n)) * (1 - (ro/n)**(m) * (m+1-m*ro/n))/((1 - ro/n)**2)
        rootkaz = (ro**(n+m))/(n**(m)*math.factorial(n)) * ro_0
        tq = lq/l
        tsmo = tq + (1 - rootkaz)/mu
        k_ = (l/mu)*(1 - rootkaz)
        return round(ro_0,2), round(rootkaz,2), round(lq,2),round(tq,2),round(tsmo,2), round(k_,2)

    #Многоканальная с неограниченной очередью
    def Multi_channel_unlimited(self, l, tobsl, n):
        mu = 1/tobsl
        ro = l/mu
        if(ro/n>= 1):
            print('Режим нестационнарный!')
            return False
        ro_0 = 0
        for k in range(0, n, 1):
            ro_0 += (ro**k)/(math.factorial(k))+(ro**(n+1))/(math.factorial(n)*(n-ro))
        ro_0 = ro_0**-1
        roq = (ro**(n+1)*ro_0)/(math.factorial(n)*(n-ro))
        lq = n * roq / (n - ro)
        tq = lq / l
        lsmo = lq  + ro
        tsmo = tq + tobsl
        return round(ro_0,2), round(roq,2), round(lq,2),round(tq,2),round(lsmo,2), round(tsmo,2)

if __name__ == '__main__':
    ca = Calculat()
    cmd = -2564
    while cmd != 3:
        print('Выберите канальность:\n1. Одноканальность \n2. Многоканальность\n3. Выход')
        cmd = int(input('Для продолжение введите число:'))
        match cmd:
            case 1:
                print('Выберите вид СМО: \n1. С отказами в обслуживании\n2. С ограниченной очередью\n3. С неограниченной очередью')
                cmd1 = int(input('Для продолжение введите число:'))
                match cmd1:
                    case 1:
                        l = float(input('Введите интенсивноть потока: '))
                        tobsl = float(input('Введите время обслуживания: '))
                        res = ca.Single_channel_failures(l, tobsl)
                        print(f"Вероятность обслуживания-{res[3]}, вероятность отказа-{res[2]}, интенсивность обслуживания-{res[0]}, время обслуживания-{tobsl}, время простоя-{res[1]}, абсолютная пропускная способность-{res[4]}")
                    case 2:
                        l = float(input('Введите интенсивноть потока: '))
                        tobsl = float(input('Введите время обслуживания: '))
                        n = int(input('Введите максимум элементов в очереди: '))
                        res = ca.Single_channel_limited_or_unlimited(l, tobsl, n, False)
                        print(f"P_0-{res[5]}, вер отказа-{res[1]}, ср длина оч-{res[2]}, ср время ож в оч-{res[3]}, относит пропускная способность-{res[0]}, ср время нахождения в СМО-{res[4]}, число в СМО-{res[3]}")
                    case 3:
                        l = float(input('Введите интенсивноть потока: '))
                        tobsl = float(input('Введите время обслуживания: '))
                        res = ca.Single_channel_limited_or_unlimited(l, tobsl, 0, True)
                        if not res:
                            continue 
                        print(f"ср число заявок в оч-{res[0]}, ср число заявок в смо-{res[2]}, ср время ож в оч-{res[1]}, ср время преб в смо-{res[3]}")
            case 2:
                print('Выберите вид СМО: \n1. С отказами в обслуживании\n2. С ограниченной очередью\n3. С неограниченной очередью')
                cmd1 = int(input('Для продолжение введите число:'))
                match cmd1:
                    case 1:
                        l = float(input('Введите интенсивноть потока: '))
                        tobsl = float(input('Введите время обслуживания: '))
                        n = int(input('Введите колличество каналов: '))
                        res = ca.Multi_channel_failures(l, tobsl, n)
                        print(f"Р_0-{res[0]}, вер отказа-{res[1]}, вер обслуж-{res[2]}, абс проп способность-{res[3]}, ср число зан каналов-{res[4]}")
                    case 2:
                        l = float(input('Введите интенсивноть потока: '))
                        tobsl = float(input('Введите время обслуживания: '))
                        n = int(input('Введите колличество каналов: '))
                        m = int(input('Введите максимум в очереди: '))
                        res = ca.Multi_channel_limited(l, tobsl, n, m)
                        print(f"ro_0-{res[0]}, вероятность отказа-{res[1]}, ср длина оч-{res[2]}, ср время ож в оч-{res[3]}, ср время ож в СМО-{res[4]}, ср число занятых каналов-{res[5]}")
                    case 3:
                        l = float(input('Введите интенсивноть потока: '))
                        tobsl = float(input('Введите время обслуживания: '))
                        n = int(input('Введите колличество каналов: '))
                        res = ca.Multi_channel_unlimited(l, tobsl, n)
                        if not res:
                            continue 
                        print(f"ro_0-{res[0]}, вер образования оч-{res[1]}, ср длина оч-{res[2]}, ср время ож в оч-{res[3]}, ср число в СМО-{res[4]}, ср время в СМО-{res[5]}")
            case 3:
                break
            case _:
                print('Введено не верное число')
                continue
    

