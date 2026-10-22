
def conclusion(p, alpha=0.05):
    """
    Interpreta el p-valor de una prueba de hipótesis.

    Parámetros
    ----------
    p : float
        P-valor obtenido en el contraste.
    alpha : float
        Nivel de significación (por defecto, 0.05).

    Retorna
    -------
    str
        Interpretación del resultado estadístico.
    """
    if p < alpha:
        return "Rechazamos H0: la diferencia es estadísticamente significativa"

    return "No rechazamos H0: no hay evidencia de diferencia significativa"


import pandas as pd


def preparar_datos_web(web_ab):
    """
    Prepara los registros web del experimento A/B.

    Elimina duplicados exactos, convierte las fechas
    y ordena los eventos cronológicamente por visita.

    Parameters
    ----------
    web_ab : pd.DataFrame
        Registros web de los participantes del experimento.

    Returns
    -------
    pd.DataFrame
        Datos web limpios y ordenados.
    """
    web_ab_clean = web_ab.drop_duplicates().copy()

    web_ab_clean["date_time"] = pd.to_datetime(
        web_ab_clean["date_time"]
    )

    web_ab_clean = web_ab_clean.sort_values(
        ["client_id", "visit_id", "date_time"]
    )

    return web_ab_clean


def unir_datos_clientes(exp_ab, demo):
    """
    Une los participantes del experimento A/B
    con sus datos demográficos.

    Parameters
    ----------
    exp_ab : pd.DataFrame
        Clientes asignados a Control o Test.
    demo : pd.DataFrame
        Información demográfica de los clientes.

    Returns
    -------
    pd.DataFrame
        Tabla de participantes con datos demográficos.
    """
    clientes_ab = pd.merge(
        exp_ab,
        demo,
        on="client_id",
        how="left",
        validate="one_to_one"
    )

    return clientes_ab


def resumir_visitas(web_ab_clean, exp_ab):
    """
    Crea una tabla resumen de las visitas del experimento.

    Para cada visita identifica el último paso,
    si llegó a confirmación y su grupo A/B.
    """
    visitas = web_ab_clean.groupby(
        ["client_id", "visit_id"]
    )

    ultimo_paso = visitas["process_step"].last()

    completadas = visitas["process_step"].apply(
        lambda pasos: (pasos == "confirm").any()
    )

    visitas_resumen = pd.DataFrame({
        "ultimo_paso": ultimo_paso,
        "completada": completadas
    }).reset_index()

    visitas_resumen = visitas_resumen.merge(
        exp_ab,
        on="client_id",
        how="left"
    )

    return visitas_resumen


def tasa_finalizacion_visitas(visitas_resumen):
    """
    Calcula el porcentaje de visitas completadas
    para cada grupo del experimento A/B.
    """
    return (
        visitas_resumen
        .groupby("Variation")["completada"]
        .mean()
        .mul(100)
        .round(2)
    )



def tasa_finalizacion_por_cliente(clientes_ab, web_ab):
    """
    Calcula el porcentaje de clientes que llegaron
    a confirm al menos una vez en el experimento A/B.
    """

    clientes = clientes_ab.copy()

    clientes_confirm = web_ab.loc[
        web_ab["process_step"] == "confirm",
        "client_id"
    ].unique()

    clientes["completo"] = clientes["client_id"].isin(
        clientes_confirm
    )

    tasa = (
        clientes
        .groupby("Variation")["completo"]
        .mean()
        .mul(100)
        .round(2)
    )

    return tasa



def calcular_tiempos_por_paso(web_ab):
    """
    Calcula la mediana del tiempo entre eventos
    consecutivos de una misma visita, en segundos.
    """

    web_tiempos = web_ab.copy()

    # Asegurar que las fechas sean datetime
    web_tiempos["date_time"] = pd.to_datetime(
        web_tiempos["date_time"]
    )

    # Ordenar los eventos cronológicamente
    web_tiempos = web_tiempos.sort_values(
        ["client_id", "visit_id", "date_time"]
    )

    # Obtener la fecha del siguiente evento
    web_tiempos["hora_siguiente"] = (
        web_tiempos.groupby(
            ["client_id", "visit_id"]
        )["date_time"].shift(-1)
    )

    # Calcular el tiempo transcurrido
    web_tiempos["duracion_seg"] = (
        web_tiempos["hora_siguiente"]
        - web_tiempos["date_time"]
    ).dt.total_seconds()

    # Calcular la mediana por grupo y paso
    tiempos = (
        web_tiempos
        .groupby(["Variation", "process_step"])["duracion_seg"]
        .median()
        .unstack()[["start", "step_1", "step_2", "step_3"]]
        .round(1)
    )

    return tiempos



def calcular_tasa_errores(web_ab):
    """
    Calcula el porcentaje de visitas con al menos
    un retroceso durante el proceso.

    Identifica cada visita mediante client_id y visit_id.
    """

    web_errores = web_ab.copy()

    orden_pasos = {
        "start": 0,
        "step_1": 1,
        "step_2": 2,
        "step_3": 3,
        "confirm": 4
    }

    # Convertir cada paso a su valor numérico
    web_errores["step_num"] = (
        web_errores["process_step"].map(orden_pasos)
    )

    # Ordenar cronológicamente
    web_errores["date_time"] = pd.to_datetime(
        web_errores["date_time"]
    )

    web_errores = web_errores.sort_values(
        ["client_id", "visit_id", "date_time"]
    )

    # Obtener el paso anterior de la misma visita
    web_errores["paso_anterior"] = (
        web_errores.groupby(
            ["client_id", "visit_id"]
        )["step_num"].shift(1)
    )

    # Detectar retrocesos
    web_errores["error"] = (
        web_errores["step_num"]
        < web_errores["paso_anterior"]
    )

    # Una fila por cliente, visita y grupo
    errores = (
        web_errores
        .groupby(
            ["client_id", "visit_id", "Variation"]
        )["error"]
        .any()
        .reset_index()
    )

    # Porcentaje de visitas con retrocesos
    tasa_errores = (
        errores.groupby("Variation")["error"]
        .mean()
        .mul(100)
        .round(2)
    )

    return errores, tasa_errores


def calcular_embudo(web_ab):
    """
    Calcula el número y porcentaje de clientes
    que alcanzan cada paso, por grupo experimental.
    """

    orden = ["start", "step_1", "step_2", "step_3", "confirm"]

    # Número de clientes únicos que llegan a cada paso
    embudo = (
        web_ab.groupby(["Variation", "process_step"])["client_id"]
        .nunique()
        .unstack()
        .reindex(columns=orden, fill_value=0)
        .fillna(0)
        .astype(int)
    )

    # Porcentaje respecto a los clientes que llegan a start
    embudo_pct = (
        embudo.div(embudo["start"], axis=0)
        .mul(100)
        .round(1)
    )

    return embudo, embudo_pct


def contraste_embudo(paso_max):
    """
    Compara la distribución del paso máximo alcanzado
    entre Control y Test mediante chi-cuadrado.
    """

    from scipy.stats import chi2_contingency

    # Tabla de frecuencias por grupo y paso máximo
    tabla = pd.crosstab(
        paso_max["Variation"],
        paso_max["step_num"]
    )

    # Contraste estadístico
    chi2, p, dof, esperados = chi2_contingency(tabla)

    return tabla, chi2, p, dof, esperados



def contraste_genero(clientes_ab):
    """
    Compara la distribución de género entre
    los grupos Control y Test mediante chi-cuadrado.
    """

    from scipy.stats import chi2_contingency

    # Trabajar sobre una copia para no modificar el original
    clientes = clientes_ab.copy()

    # Agrupar categorías de género
    clientes["genero_grupo"] = clientes["gendr"].replace({
        "U": "Otro/No_informado",
        "X": "Otro/No_informado"
    })

    # Tabla de frecuencias
    tabla_genero = pd.crosstab(
        clientes["Variation"],
        clientes["genero_grupo"]
    )

    # Porcentajes dentro de cada grupo
    tabla_pct = (
        pd.crosstab(
            clientes["Variation"],
            clientes["genero_grupo"],
            normalize="index"
        )
        .mul(100)
        .round(1)
    )

    # Contraste estadístico
    chi2, p, dof, esperados = chi2_contingency(
        tabla_genero
    )

    return tabla_genero, tabla_pct, chi2, p, dof, esperados



def contraste_finalizacion(clientes_ab):
    """
    Compara la tasa de finalización por cliente
    entre Test y Control mediante una prueba Z unilateral.
    """

    from statsmodels.stats.proportion import proportions_ztest

    # Resumen por grupo
    resumen = (
        clientes_ab
        .groupby("Variation")["completo"]
        .agg(
            total_clientes="count",
            clientes_completaron="sum",
            tasa_finalizacion="mean"
        )
    )

    resumen["tasa_finalizacion"] *= 100

    # Clientes que completaron el proceso
    exitos = [
        resumen.loc["Test", "clientes_completaron"],
        resumen.loc["Control", "clientes_completaron"]
    ]

    # Total de clientes de cada grupo
    totales = [
        resumen.loc["Test", "total_clientes"],
        resumen.loc["Control", "total_clientes"]
    ]

    # Prueba Z unilateral: Test > Control
    z_stat, p_valor = proportions_ztest(
        count=exitos,
        nobs=totales,
        alternative="larger"
    )

    return resumen, z_stat, p_valor



def contraste_umbral_finalizacion(resumen_hipotesis, umbral=0.05):
    """
    Evalúa si la mejora relativa de Test frente a Control
    supera un umbral determinado.

    Por defecto, el umbral es del 5 % relativo.
    """

    import numpy as np
    from scipy.stats import norm

    # Tasas originales sin redondear
    p_control = (
        resumen_hipotesis.loc["Control", "clientes_completaron"]
        / resumen_hipotesis.loc["Control", "total_clientes"]
    )

    p_test = (
        resumen_hipotesis.loc["Test", "clientes_completaron"]
        / resumen_hipotesis.loc["Test", "total_clientes"]
    )

    n_control = resumen_hipotesis.loc["Control", "total_clientes"]
    n_test = resumen_hipotesis.loc["Test", "total_clientes"]

    # Mejoras observadas
    mejora_absoluta = (p_test - p_control) * 100
    mejora_relativa = ((p_test - p_control) / p_control) * 100

    # Diferencia respecto al umbral
    factor = 1 + umbral
    diferencia_umbral = p_test - factor * p_control

    # Error estándar estimado
    error_estandar = np.sqrt(
        p_test * (1 - p_test) / n_test
        + (factor ** 2) * p_control * (1 - p_control) / n_control
    )

    # Contraste unilateral
    z_umbral = diferencia_umbral / error_estandar
    p_valor_umbral = norm.sf(z_umbral)

    return (
        mejora_absoluta,
        mejora_relativa,
        diferencia_umbral,
        z_umbral,
        p_valor_umbral
    )



def contraste_edad(clientes_ab):
    """
    Compara la edad media de Control y Test
    mediante la prueba t de Welch.
    """

    from scipy.stats import ttest_ind

    # Resumen descriptivo por grupo
    resumen_edad = (
        clientes_ab
        .groupby("Variation")["clnt_age"]
        .agg(
            total_clientes="size",
            edades_validas="count",
            edad_media="mean",
            desviacion="std",
            mediana="median"
        )
    )

    # Seleccionar edades válidas
    edad_control = clientes_ab.loc[
        clientes_ab["Variation"] == "Control",
        "clnt_age"
    ].dropna()

    edad_test = clientes_ab.loc[
        clientes_ab["Variation"] == "Test",
        "clnt_age"
    ].dropna()

    # Prueba t de Welch
    t_stat, p_valor_edad = ttest_ind(
        edad_test,
        edad_control,
        equal_var=False
    )

    return resumen_edad, t_stat, p_valor_edad
