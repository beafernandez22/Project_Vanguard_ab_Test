# Vanguard A/B Test | Evaluación del impacto de un rediseño digital


## 1. Objetivo del proyecto

Evaluar si el rediseño de la interfaz digital de Vanguard mejora la experiencia de usuario y aumenta la tasa de finalización de su proceso online.

El objetivo no es únicamente identificar diferencias entre las versiones, sino determinar si la mejora es estadísticamente significativa, si alcanza el umbral de rentabilidad establecido y si existen riesgos que deban resolverse antes de implementar el nuevo diseño.

## 2. Contexto de negocio

Vanguard es una empresa estadounidense de gestión de inversiones que ofrece a sus clientes servicios financieros a través de canales digitales.

Con el propósito de optimizar su experiencia online, Vanguard desarrolló una nueva interfaz con un diseño más moderno e indicaciones para guiar a los usuarios durante el proceso.

Para evaluar su efectividad, realizó un **experimento A/B entre el 15 de marzo y el 20 de junio de 2017**, comparando dos versiones:

- **Control:** interfaz tradicional.
- **Test:** nueva interfaz rediseñada.

Ambos grupos recorrieron cinco pantallas: `start → step_1 → step_2 → step_3 → confirm`.

La decisión de negocio consiste en determinar si Vanguard debería implementar el nuevo diseño para todos sus clientes, introducir mejoras adicionales o realizar otro experimento antes de su lanzamiento.

## 3. Dataset

Los datos proceden del proyecto educativo *Vanguard A/B Test* de Ironhack y representan información de clientes e interacciones digitales durante el experimento.

Se utilizaron tres fuentes principales:

| Dataset | Descripción | Volumen inicial |
|---|---|---:|
| `df_final_demo` | Información demográfica y financiera de clientes | 70.609 clientes |
| `df_final_web_data` | Registro de interacciones digitales, dividido en dos archivos | 755.405 registros |
| `df_final_experiment_clients` | Asignación de clientes a Control o Test | 50.500 clientes |

Las tablas se relacionaron mediante `client_id`.

### Diccionario de datos

| Variable | Descripción |
|---|---|
| `client_id` | Identificador único del cliente |
| `Variation` | Grupo experimental: Control o Test |
| `visitor_id` | Identificador asociado al cliente y dispositivo |
| `visit_id` | Identificador de sesión web |
| `process_step` | Etapa alcanzada en el proceso digital |
| `date_time` | Fecha y hora de la interacción |
| `clnt_age` | Edad del cliente |
| `gendr` | Género registrado |
| `clnt_tenure_yr` | Antigüedad del cliente en años |
| `clnt_tenure_mnth` | Antigüedad del cliente en meses |
| `num_accts` | Número de cuentas del cliente |
| `bal` | Saldo del cliente |

## 4. Calidad y preparación de los datos

Antes del análisis se realizaron tareas de exploración, limpieza y transformación para mejorar la consistencia de los resultados.

Las principales actuaciones fueron:

- Identificación y eliminación de **4.074 registros duplicados exactos** en las interacciones web.
- Exclusión de **20.109 clientes sin asignación experimental**, que no formaban parte de Control ni Test.
- Agrupación de las categorías de género `U` y `X` en «Otro / No informado», debido a la escasa representación de `X`.
- Conversión de fechas almacenadas como texto a formato fecha-hora.
- Unión de las fuentes mediante `client_id`.
- Construcción de tablas analíticas a nivel de cliente y de visita.

Se diferenciaron las métricas calculadas por cliente de las calculadas por visita, ya que responden a preguntas de negocio distintas.

## 5. Preguntas clave del análisis

1. ¿El nuevo diseño aumenta la proporción de clientes que completan el proceso?
2. ¿La mejora observada es estadísticamente significativa?
3. ¿Supera el umbral mínimo de rentabilidad del 5 %?
4. ¿El rediseño reduce el tiempo necesario para avanzar por las distintas etapas?
5. ¿En qué pasos se producen los principales abandonos y retrocesos?
6. ¿Cómo varía el resultado según la edad, el género y la antigüedad del cliente?
7. ¿Son suficientemente fiables los resultados como para recomendar un lanzamiento generalizado?

## 6. Metodología y proceso de análisis

### Análisis exploratorio (EDA)

Se estudiaron las características de los clientes y su comportamiento digital, incluyendo distribuciones de edad, género, antigüedad, saldo, número de cuentas, finalización y abandono.

También se compararon los perfiles de Control y Test para identificar posibles desequilibrios entre ambos grupos.

### Definición de KPIs

Se seleccionaron cuatro indicadores principales:

| KPI | Definición |
|---|---|
| Tasa de finalización | Porcentaje de clientes que alcanzan `confirm` al menos una vez |
| Tiempo por paso | Tiempo transcurrido entre etapas consecutivas de una visita |
| Tasa de error | Porcentaje de visitas con al menos un retroceso a una etapa anterior |
| Embudo de conversión | Proporción de clientes que alcanza cada etapa del proceso |

Para resumir los tiempos se utilizaron medianas, debido a la presencia de valores extremos.

### Contrastes de hipótesis

Se aplicaron pruebas estadísticas con un nivel de significación de **α = 0,05**:

- Test Z de dos proporciones para comparar tasas de finalización.
- Contraste unilateral para evaluar el umbral de mejora del 5 %.
- Prueba t de Welch para comparar edades medias.
- Test Z para comparar tasas de retroceso.
- Pruebas chi-cuadrado para estudiar asociaciones entre variables categóricas.
- Test binomial para evaluar el reparto observado entre grupos experimentales.

### Visualización

Los resultados se trasladaron a **Tableau**, mediante dashboards interactivos que permiten explorar el perfil de los clientes, su comportamiento, los resultados del experimento y las diferencias entre segmentos.

## 7. Resultados e insights principales

### 7.1. El nuevo diseño mejora la finalización

| Grupo | Tasa de finalización |
|---|---:|
| Control | 65,6 % |
| Test | 69,3 % |
| **Diferencia** | **+3,7 puntos porcentuales** |

La mejora es estadísticamente significativa (`p < 0,001`).

En términos de negocio, aproximadamente cuatro clientes adicionales de cada cien completan el proceso con la nueva interfaz.

### 7.2. No se demuestra que la mejora supere el umbral del 5 %

Aunque la mejora relativa observada es aproximadamente del **5,65 %**, el contraste del umbral obtiene un `p = 0,16`.

Por tanto, con el nivel de significación establecido, **no existe evidencia suficiente para afirmar que la mejora real supera el 5 % exigido**.

Este resultado es fundamental: una mejora estadísticamente significativa no implica necesariamente que se haya demostrado el cumplimiento del objetivo de negocio.

### 7.3. El nuevo diseño reduce algunos tiempos, pero genera más retrocesos

| Indicador | Control | Test |
|---|---:|---:|
| Suma de medianas por paso | 176 s | 160 s |
| Visitas con retrocesos | 20,5 % | 27,0 % |

El diseño Test presenta una suma de medianas por paso 16 segundos inferior, aunque esta medida no equivale necesariamente al tiempo total mediano por visita.

Sin embargo, también registra **6,5 puntos porcentuales más de visitas con retrocesos**.

El incremento se concentra principalmente en los retornos a la pantalla de inicio, lo que señala un posible problema de navegación o comprensión de la interfaz.

### 7.4. La principal ventaja aparece al comienzo del proceso

En el paso del inicio a la primera etapa, Test conserva una mayor proporción de clientes que Control.

La ventaja inicial se mantiene durante las siguientes etapas y contribuye a explicar la mayor tasa final de conversión.

### 7.5. La mejora no es igual en todos los segmentos

El análisis por edad, género y antigüedad permite identificar diferencias en las tasas de finalización.

En las comparaciones descriptivas realizadas, Test muestra mejores resultados en los segmentos analizados, con mejoras especialmente destacadas entre los clientes jóvenes.

Estos resultados ayudan a identificar oportunidades de personalización, aunque las diferencias entre segmentos no deben interpretarse automáticamente como estadísticamente significativas.

### 7.6. La ventaja disminuye durante el experimento

El análisis temporal muestra una diferencia favorable a Test durante marzo y abril, que se reduce considerablemente a partir de mayo.

Este patrón es compatible con un posible efecto novedad, aunque los datos disponibles no permiten demostrar que sea su causa.

## 8. Recomendaciones de negocio

**Recomendación principal: no implementar todavía el nuevo diseño para el 100 % de los clientes.**

Aunque Test mejora la finalización, existen incertidumbres sobre el umbral de rentabilidad, la navegación y la estabilidad temporal del efecto.

Se proponen tres líneas de actuación:

**1. Optimizar la experiencia de navegación**

Revisar especialmente la pantalla de inicio y el primer paso, donde se concentran las fricciones detectadas. Analizar la claridad de las instrucciones, los botones y las opciones de navegación.

**2. Repetir el experimento tras introducir mejoras**

Realizar una nueva prueba A/B con una asignación aleatoria documentada, idealmente equilibrada entre Control y Test, y una duración suficiente para comprobar si la mejora se mantiene.

**3. Incorporar criterios económicos y de experiencia de usuario**

Relacionar las conversiones adicionales con el coste de implementación y mantenimiento del rediseño. Complementar el análisis cuantitativo con pruebas de usabilidad y opiniones de clientes.

## 9. Limitaciones

El estudio presenta varias limitaciones que deben considerarse antes de tomar una decisión definitiva:

- **Asignación experimental:** el reparto observado entre grupos no es 50/50 y no se dispone de información completa sobre el mecanismo de asignación.
- **Evolución temporal:** la reducción de la ventaja de Test puede afectar a la sostenibilidad de los resultados.
- **Información técnica:** no se dispone de suficientes datos sobre dispositivos, navegadores y posibles problemas de compatibilidad.
- **Contexto económico:** faltan los costes del rediseño y el valor generado por cada finalización.
- **Comportamiento del usuario:** los registros permiten detectar retrocesos, pero no explicar con certeza sus causas.
- **Interpretación de segmentos:** las diferencias descriptivas no sustituyen a pruebas específicas de heterogeneidad del efecto.

## 10. Próximos pasos

Como continuación del proyecto se propone:

1. Realizar un análisis más detallado de las sesiones con retrocesos.
2. Incorporar información sobre dispositivos y navegadores.
3. Ejecutar pruebas de usabilidad para investigar los puntos de fricción.
4. Diseñar y evaluar una versión optimizada de las primeras pantallas.
5. Repetir el experimento con un plan de aleatorización y un tamaño muestral previamente definidos.
6. Medir el impacto económico real mediante un análisis coste-beneficio.
7. Evaluar la persistencia de la mejora y su posible variación entre segmentos.

## 11. Cómo replicar el proyecto

### Requisitos

- Python 3
- Jupyter Notebook
- Pandas y NumPy
- SciPy y Statsmodels
- Matplotlib, si se utilizan los gráficos del notebook
- Tableau Desktop o Tableau Public para consultar las visualizaciones

### Pasos

**1. Clonar el repositorio**

```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_REPOSITORIO>
```

**2. Instalar las dependencias**

Si el repositorio incluye un archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

**3. Preparar los datos**

Colocar los datasets originales en la ruta esperada por el notebook, respetando los nombres de archivo y la estructura de carpetas utilizada en el proyecto.

**4. Ejecutar el análisis**

```bash
jupyter notebook
```

Abrir `trabajo_final.ipynb` y ejecutar las celdas en orden, verificando previamente las rutas de importación y los módulos auxiliares.

**5. Explorar las visualizaciones**

Abrir el workbook `Proyecto_Vanguard.twbx` en Tableau o consultar su versión publicada.

### Recursos del proyecto

- **Notebook de Python:** `trabajo_final.ipynb`
- **Dashboard de Tableau:** [Añadir enlace a Tableau Public]
- **Repositorio de GitHub:** [Añadir enlace]
- **Presentación:** [Añadir enlace]
- **Gestión del proyecto en Trello:** [Añadir enlace, si se desea]



## 12. Conclusión

El experimento muestra que el rediseño de Vanguard consigue aumentar significativamente la tasa de finalización del proceso online.

Sin embargo, **la evidencia disponible no demuestra que la mejora supere el umbral de rentabilidad del 5 %**, mientras que el aumento de retrocesos y la reducción de la ventaja a lo largo del tiempo plantean dudas sobre su implementación inmediata.

La principal conclusión es que **una mejora estadística no siempre es suficiente para justificar una decisión de negocio**.

La recomendación es optimizar los puntos de fricción identificados, validar nuevamente el diseño y complementar los indicadores de conversión con información económica y de experiencia de usuario.

