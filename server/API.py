import json, datetime

user = 'User-Agent: PBLredes/Guilherme\n'
content_type = 'Content-Type: text/html\n'

def POST_loginCliente(param, host_name, session):
    cod = param.get("codigo")
    status = 'HTTP/1.1 200 OK\n'
    response_body = '{\"resultado\": \"Medidor nao existe.\"}'

    if cod:
        with open("medidores.json", encoding='utf-8') as med_file_read:
            meds = json.load(med_file_read)
            login_med = meds.get(cod)
            if login_med:
                response_body = '{\"resultado\": \"Login feito com sucesso.\"}'
                status = 'HTTP/1.1 200 OK\n'
                session["codigo"] = cod
                session["auth"] = 0
            else:
                status = 'HTTP/1.1 404 Not Found\n'
                pass
    else:
        return bad_request(host_name)

    content_length = 'Content-Length: {leng}\n\n'.format(leng=str(len(response_body)))
    response_headers = status + host_name + user + content_type + content_length
    response = response_headers + response_body

    return response

def POST_loginFuncionario(param, host_name, session):
    matricula = param.get("matricula")
    senha = param.get("senha")
    status = 'HTTP/1.1 200 OK\n'
    response_body = '{\"resultado\": \"Matricula nao encontrada.\"}'

    if matricula and senha:
        with open("funcionarios.json", encoding='utf-8') as work_file_read:
            workers = json.load(work_file_read)
            worker = workers.get(matricula)
            if worker:
                if worker.get("senha") == senha:
                    response_body = '{\"resultado\": \"Login feito com sucesso.\"}'
                    status = 'HTTP/1.1 200 OK\n'
                    session["matricula"] = matricula
                    session["auth"] = worker.get("auth")
                else:
                    '{\"resultado\": \"Senha incorreta.\"}'
            else:
                status = 'HTTP/1.1 404 Not Found\n'
                pass
    else:
        return bad_request(host_name)

    content_length = 'Content-Length: {leng}\n\n'.format(leng=str(len(response_body)))
    response_headers = status + host_name + user + content_type + content_length
    response = response_headers + response_body

    return response

def POST_cadastrarFuncionario(param, host_name, session):
    matricula = param.get("matricula")
    nome = param.get("nome")
    senha = param.get("senha")
    auth = param.get("auth")
    workers = {}
    status = 'HTTP/1.1 200 OK\n'
    response_body = '{\"resultado\": \"Matricula ja existe.\"}'

    if session.get("auth") == "2":
        with open("funcionarios.json", encoding='utf-8') as work_file_read:
            workers = json.load(work_file_read)
            worker_exists = workers.get(matricula)
        if not worker_exists:
            workers[matricula] = {"nome": nome, "senha": senha, "auth": auth}
            response_body = '{\"resultado\": \"Cadastro realizado.\"}'
            status = 'HTTP/1.1 202 Created\n'
            with open("funcionarios.json", 'w', encoding='utf-8') as work_file_write:
                json.dump(workers, work_file_write, indent=4)
    else:
        status = 'HTTP/1.1 401 Unauthorized\n'
        response_body = '{\"resultado\": \"Sem autoridade.\"}'

    content_length = 'Content-Length: {leng}\n\n'.format(leng=str(len(response_body)))
    response_headers = status + host_name + user + content_type + content_length
    response = response_headers + response_body

    return response

def POST_cadastrarMedidor(param, host_name, session):
    auth = session.get("auth")

    user = 'User-Agent: PBL/redes\n'
    content_type = 'Content-Type: text/html\n'
    status = 'HTTP/1.1 401 Unauthorized\n'
    response_body = '{\"resultado\": \"Sem autoridade.\"}'

    meds = {}

    if auth == "1" or auth == "2":
        status = 'HTTP/1.1 200 OK\n'
        codigo = param.get("codigo")
        with open("medidores.json", encoding='utf-8') as med_file_read:
            meds = json.load(med_file_read)
            med_exists = meds.get(codigo)
            print(med_exists)
        if not med_exists:
            meds[codigo] = {"consumos": [], "ativo": "1"}
            with open("medidores.json", 'w', encoding='utf-8') as med_file_write:
                json.dump(meds, med_file_write, indent=4)
            response_body = '{\"resultado\": \"Medidor cadastrado.\"}'
            status = 'HTTP/1.1 201 Created\n'
        else:
            response_body = '{\"resultado\": \"Ja existe um medidor com este codigo.\"}'

    content_length = 'Content-Length: {leng}\n\n'.format(leng=str(len(response_body)))
    response_headers = status + host_name + user + content_type + content_length
    response = response_headers + response_body
    return response

def inserir_medida(param):
    cod = param[0]
    measure = param[1:]
    meds = {}
    valid_insert = 0
    if cod and measure:
        with open("medidores.json", encoding='utf-8') as med_file_read:
            meds = json.load(med_file_read)
            altered_med = meds.get(cod)
            if altered_med:
                if altered_med.get("ativo") == "1":
                    measures = altered_med.get("consumos")
                    #measures.append(measure)
                    measures.insert(0, measure)
                    valid_insert = 1
        if valid_insert:
            with open("medidores.json", 'w', encoding='utf-8') as med_file_write:
                json.dump(meds, med_file_write, indent=4)

def POST_historico(param, host_name, session):
    med_cod = session.get("codigo")
    prazo = int(param.get("prazo"))
    medias = {}
    max_list = [0, 0]
    status = 'HTTP/1.1 401 Unauthorized\n'
    result_body = '{\"resultado\": \"Sem login.\", '
    meds = {}

    if prazo:
        status = 'HTTP/1.1 200 OK\n'
        result_body = '{\"resultado\": \"Sem medidas de consumo.\", '

        with open("medidores.json", encoding='utf-8') as med_file_read:
            meds = json.load(med_file_read)
            login_med = meds.get(med_cod)
            if login_med:
                prev_med = login_med.get("consumos")

                if len(prev_med):
                    result_body = '{\"resultado\": \"Consumo regular.\", '

                    for i in range(len(prev_med)):
                        current_day = prev_med[i][0]
                        current_day = current_day[:10]

                        if medias.get(current_day):
                            print("adding to sum")
                            new_sum = float(medias.get(current_day)) + float(prev_med[i][1])
                            new_sum = round(new_sum, 2)
                            print(new_sum)
                            medias[current_day] = str(new_sum)
                        else:
                            print("adding new day")
                            print(prev_med[i][1])
                            medias[current_day] = prev_med[i][1]

                        if len(medias.keys()) >= prazo:
                            break

                    if prazo > 1 and len(medias.keys()) > 1:
                        m_sum = 0
                        m_value = 0
                        m_date = 0

                        for date, item in medias.items():
                            print(date, item)
                            current_value = float(item)
                            current_value = round(current_value/24, 2)
                            medias[date] = str(current_value)
                            m_sum += current_value
                            if current_value > m_value:
                                m_value = current_value
                                m_date = date

                        m_avg = m_sum/len(medias.keys())

                        if m_date and m_value > m_avg * 1.5:
                            result_body = '\"resultado\": \"Consumo acima da media no dia {mday}.\", '.format(mday=m_date)
                            result_body = '{' + result_body
                            result_body += '\"media\": \"{avg}\", '.format(avg=round(m_avg, 2))

                status = 'HTTP/1.1 200 OK\n'
    else:
        return bad_request()

    fatura_body = '\"Medias de consumo (kW/h)\": ' + json.dumps(medias)
    response_body = result_body + fatura_body + '}'
    print(response_body)
    content_length = 'Content-Length: {leng}\n\n'.format(leng=str(len(response_body)))

    response_headers = status + host_name + user + content_type + content_length
    response = response_headers + response_body
    return response

def GET_fatura(param, host_name, session):
    med_cod = session.get("codigo")

    fatura = 0
    status = 'HTTP/1.1 401 Unauthorized\n'
    result_body = '{\"resultado\": \"Sem login.\",'
    meds = {}

    print(f"med cod is {med_cod}")
    if med_cod:
        with open("medidores.json", encoding='utf-8') as med_file_read:
            meds = json.load(med_file_read)
            login_med = meds.get(med_cod)
            if login_med:
                prev_med = login_med.get("consumos")

                year_month = datetime.datetime.now()
                year_month = str(year_month)[:7]

                if len(prev_med):
                    for i in range(len(prev_med)):
                        current_year_month = prev_med[i][0]
                        current_year_month = current_year_month[:7]

                        if current_year_month == year_month:
                            fatura += float(prev_med[i][1])
                        else:
                            break
                status = 'HTTP/1.1 200 OK\n'
                result_body = '{\"resultado\": \"Fatura encontrada.\",'
            else:
                status = 'HTTP/1.1 404 Not Found\n'
                result_body = '{\"resultado\": \"Medidor nao existe.\",'
                pass

    fatura = round(fatura * 1.04, 2)

    fatura_body = '\"fatura\": \"R$ {fat}\"'.format(fat=fatura)
    response_body = result_body + fatura_body + '}'
    content_length = 'Content-Length: {leng}\n\n'.format(leng=str(len(response_body)))

    response_headers = status + host_name + user + content_type + content_length
    response = response_headers + response_body
    return response

def bad_request(host_name):
    status = 'HTTP/1.1 400 Bad Request\n'
    response_body = '{\"result\" : \"Hello, Bad Request!\"}'
    content_length = 'Content-Length: {leng}\n\n'.format(leng=str(len(response_body)))
    response_headers = status + host_name + user + content_type + content_length
    return response_headers + response_body

'''

def PUT_inserirMedida(param, host_name, session):
    med_cod = param.get("codigo")
    update = param.get("consumo")

    success = 0
    status = 'HTTP/1.1 409 Conflict\n'
    meds = {}

    with open("medidores.json", encoding='utf-8') as med_file_read:
        meds = json.load(med_file_read)
        login_med = meds.get(med_cod)
        if login_med:
            if login_med["ativo"] == "1":
                login_med["consumoAtual"] = update
                meds[med_cod] = login_med
                success = 1
                status = 'HTTP/1.1 200 OK\n'
            else:
                status = 'HTTP/1.1 403 Forbidden\n'
        else:
            status = 'HTTP/1.1 404 Not Found\n'
            pass

    if success:
        with open("medidores.json", 'w', encoding='utf-8') as med_file_write:
            json.dump(meds, med_file_write, indent=4)

    response_body = '{result: ' + str(success) + '}'
    content_length = 'Content-Length: {leng}\n\n'.format(leng=str(len(response_body)))

    response_headers = status + host_name + user + content_type + content_length
    response = response_headers + response_body
    return response

def POST_loginMedidor(param, host_name, session):
    med_cod = param.get("codigo")

    success = 0
    status = 'HTTP/1.1 409 Conflict\n'
    meds = {}

    with open("medidores.json", encoding='utf-8') as med_file_read:
        meds = json.load(med_file_read)
        login_med = meds.get(med_cod)
        if login_med:
            activity = login_med.get("ativo")
            if activity == "0":
                login_med["ativo"] = "1"
                meds[med_cod] = login_med
                success = 1
                status = 'HTTP/1.1 200 OK\n'
        else:
            status = 'HTTP/1.1 404 Not Found\n'
            pass

    if success:
        with open("medidores.json", 'w', encoding='utf-8') as med_file_write:
            json.dump(meds, med_file_write, indent=4)

    response_body = '{result: ' + str(success)+ '}'
    content_length = 'Content-Length: {leng}\n\n'.format(leng=str(len(response_body)))

    response_headers = status + host_name + user + content_type + content_length
    response = response_headers + response_body
    return response
'''
