# Vanguard: ¿El nuevo diseño digital consigue que más clientes completen el proceso online?

Análisis de un A/B test para evaluar si un rediseño de la interfaz web de Vanguard mejora la experiencia de usuario y la tasa de finalización del proceso online.

Equipo: Beatriz Fernández · Juan Carlos Del Mar Lostanau ; Bootcamp: Ironhack Data Analytics

## 1. Objetivo del proyecto
Evaluar, a partir de los datos de un experimento A/, si la nueva interfaz consigue que mas clientes completen el proceso online, lo hagan mas rapido y con menos erorres. El resultado ayudará a Vanguard a decidir si extiende el nuevo diseño a todos sus clientes.

## 2. Contexto de negocio
- Empresa: Vanguard, gestora de inversiones estadounidense (caso basado en datos reales).
- Desafío: el equipo de Customer Experience (CX) cree que un diseño más intuitivo y con mensajes de ayuda puede hacer el proceso online más sencillo y aumentar el número de clientes que lo completan.
- Experimento: A/B test realizado entre el 15/03/2017 y el 20/06/2017.
        - Control: clientes que usaron el proceso tradicional.
        - Test: clientes que usaron el nuevo diseño.
        - Ambos grupos siguen la misma secuencia: start → step_1 → step_2 → step_3 → confirm.
- Decisión a tomar: ¿se implanta el nuevo diseño para todos los clientes?

## 3. Dataset
- df_final_demo; con 70.609 filas ; 	Perfil demográfico y de cuenta de cada cliente
- df_final_experiment_clients ; con 70.609 filas;	Grupo asignado a cada cliente (Test / Control)
- df_final_web_data (pt_1 + pt_2) ; con 755.405	Registro de cada paso del proceso online (unimos las dos partes)
Fuente: datos reales de Vanguard proporcionados por Ironhack. Hay tres tablas:

- Diccionario de las variables principales

Variable                                    Descripción

client_id	                        Identificador único del cliente (clave para unir tablas)
Variation	                        Grupo del experimento: Test o Control
clnt_age	                        Edad del cliente
clnt_tenure_yr / clnt_tenure_mnth	Antigüedad como cliente (años / meses)
gendr	                            Género: M, F, U (no informado), X
num_accts	                        Número de cuentas
bal	                                Saldo total
calls_6_mnth / logons_6_mnth	    Llamadas y accesos online en los últimos 6 meses
visitor_id / visit_id	            Identificador del dispositivo / de la sesión web
process_step	                    Paso del proceso (start, step_1, step_2, step_3, confirm)
date_time	                        Fecha y hora de cada paso

- Notas sobre calidad del dato

20.109 clientes no tienen grupo asignado y se excluyeron. Quedan 50.500 participantes: 26.968 en Test y 23.532 en Control.
12 participantes no tienen datos demográficos y se excluyeron del análisis de clientes.
4.074 filas de actividad web eran duplicados exactos (mismo cliente, sesión, paso y hora) y se eliminaron por considerarse registros técnicos repetidos.
La columna date_time se convirtió de texto a fecha.
logons_6_mnth es exactamente calls_6_mnth + 3 en el 96,7 % de los clientes, por lo que ambas variables no son independientes y no se usaron para comparar canales.

## 4. Preguntas clave
¿Quiénes son los principales clientes que usan el proceso online? ¿Son jóvenes o mayores, nuevos o antiguos?
¿Los grupos Test y Control son comparables (edad, saldo, antigüedad, género, número de cuentas)?
¿Los clientes con más saldo son los de mayor antigüedad y edad?
¿Qué KPIs determinan el éxito del nuevo diseño?
Según esos KPIs, ¿el nuevo diseño funciona mejor que el antiguo?

## 5. Proceso de análisis
- EDA y limpieza: revisión de tamaño, tipos, nulos y duplicados de cada tabla; unión de las dos partes de los datos web; filtrado de los participantes del experimento; unión de tablas por client_id.
- Comprobación de equilibrio entre grupos: comparación de edad, saldo, antigüedad, género y número de cuentas entre Test y Control.
- Análisis de comportamiento de clientes: tramos de edad, clasificación en clientes nuevos (≤5 años) o de larga trayectoria (>5 años) y saldo según edad y antigüedad (histogramas y boxplots).
- KPIs del experimento:
        -Tasa de finalización: % de clientes que llegan a confirm.
        -Tiempo en cada paso: mediana de segundos entre un paso y el siguiente dentro de la misma visita. Usamos la mediana porque la media se ve muy afectada por sesiones que se quedan abiertas.
        -Tasa de errores: % de visitas con al menos un retroceso (pasar de un paso a uno anterior).
        -Embudo (funnel): % de clientes que alcanzan cada paso.