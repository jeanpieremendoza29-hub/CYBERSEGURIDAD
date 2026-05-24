# Registro de Errores y Soluciones en LaTeX

Este documento recopila los errores comunes de compilación encontrados al trabajar con LaTeX y TikZ en este proyecto, junto con sus respectivas soluciones, para servir como referencia futura.

## 1. Conflicto entre TikZ y Babel (Español)

**El Problema:**
Al utilizar el paquete `babel` con el idioma español (`\usepackage[spanish]{babel}`), caracteres como `>` y `<` se vuelven "activos" (*active characters*). Esto interfiere directamente con la sintaxis que utiliza TikZ para dibujar flechas (por ejemplo, al usar `->` en los comandos `\draw`), provocando fallos de compilación.

**La Solución:**
Cargar la librería específica de TikZ diseñada para manejar incompatibilidades con paquetes de idiomas. Se debe agregar la siguiente línea en el preámbulo del documento, justo después de cargar TikZ:

```latex
\usepackage{tikz}
\usetikzlibrary{babel}
```

## 2. Parseo de Coordenadas en bucles `\foreach` (TikZ)

**El Problema:**
El error `Cannot parse this coordinate (Missing character: There is no ( in font nullfont!)` ocurre cuando se intenta iterar una macro que contiene un par de coordenadas completas con paréntesis (ej. `\pos`) y pasarlas a parámetros como `shift={\pos}`. TikZ no logra "desempaquetar" correctamente los paréntesis internos de la variable.

**La Solución:**
En lugar de iterar sobre una única variable que contenga las coordenadas agrupadas con paréntesis, se deben separar las coordenadas `x` e `y` explícitamente utilizando una barra diagonal `/` en la declaración del bucle `\foreach`. Luego, los paréntesis se colocan de forma manual en el uso.

**Ejemplo incorrecto (genera error):**
```latex
\foreach \pos in {(-1.2,-0.8), (-0.8,-1.5)} {
    \begin{scope}[shift={\pos}]
        % ...
    \end{scope}
}
```

**Ejemplo corregido:**
```latex
\foreach \x/\y in {-1.2/-0.8, -0.8/-1.5} {
    \begin{scope}[shift={(\x,\y)}]
        % ...
    \end{scope}
}
```

## 3. Incluir Imágenes Externas en LaTeX (`graphicx`)

**El Problema:**
De forma nativa, LaTeX básico no cuenta con un comando directo para insertar archivos de imagen (como `.jpg`, `.png` o `.pdf`) con control de escala y posicionamiento dentro del texto.

**La Solución:**
Se debe utilizar el paquete estándar `graphicx`. Este paquete proporciona el comando `\includegraphics`, el cual permite importar imágenes y modificar sus atributos (como el ancho, el alto o el ángulo de rotación).

**Ejemplo de uso:**
```latex
% 1. Añadir al preámbulo (antes de \begin{document}):
\usepackage{graphicx}

% 2. Usar en el cuerpo del documento:
% (Se recomienda envolverlo en un entorno 'center' o 'figure' para alinearlo)
\begin{center}
    % El parámetro 'width=0.6\textwidth' ajusta la imagen al 60% del ancho del texto
    \includegraphics[width=0.6\textwidth]{ruta/o/nombre_de_la_imagen.jpg}
\end{center}
```

## 4. Inclusión de Código Fuente (Bloques de Código)

**El Problema:**
Intentar pegar código de programación directamente en el flujo de texto de LaTeX provoca errores críticos de compilación debido a la presencia de caracteres reservados (como `{`, `}`, `%`, `_`, `#`). Además, el texto pierde el formato monoespaciado y el resaltado de sintaxis.

**La Solución:**
Utilizar el paquete `listings` para entornos de código ligeros y estándar. Permite definir palabras clave, colores para comentarios y strings, así como el ajuste automático de líneas largas.

**Ejemplo de configuración (Preámbulo):**
```latex
\usepackage{listings}
\usepackage{xcolor}

\lstset{
    backgroundcolor=\color{gray!5},
    basicstyle=\ttfamily\small,
    breaklines=true,
    keywordstyle=\color{blue},
    commentstyle=\color{green!60!black},
    stringstyle=\color{purple},
    numbers=left,
    numberstyle=\tiny\color{gray},
    frame=single,
    showstringspaces=false
}
```

**Ejemplo de uso en el cuerpo:**
```latex
\begin{lstlisting}[language=Python, caption={Cálculo de Impedancia}]
# Código limpio sin conflictos con caracteres especiales de LaTeX
def calcular_impedancia(r, x):
    return (r**2 + x**2)**0.5
\end{lstlisting}
```

## 5. Escape de Caracteres Especiales en Texto Plano

**El Problema:**
Al redactar explicaciones técnicas fuera de los bloques de código, el uso accidental de caracteres de control de LaTeX (especialmente el guion bajo `_` en nombres de variables o el signo `%` para porcentajes) corrompe la compilación generando errores opacos como `Missing $ inserted`.

**La Solución:**
Cualquier carácter reservado que se mencione en el texto normal debe ser precedido por una barra invertida (`\`), o bien aislarse dentro del comando de texto monoespaciado `\texttt{...}`.

* **Caracteres que siempre deben escaparse:** `_`, `%`, `&`, `#`, `{`, `}`.
* **Incorrecto:** La variable `config_base` controla el 100% del ciclo de reloj.
* **Correcto:** La variable `config\_base` controla el 100\% del ciclo de reloj.
* **Alternativa recomendada:** La variable `\texttt{config\_base}` controla el 100\% del ciclo de reloj.

## 6. Escritura Uniforme de Unidades Técnicas (`siunitx`)

**El Problema:**
Escribir valores numéricos y unidades de ingeniería de forma manual (ej. `50 ohm`, `50 \Omega`, `10nF`) produce inconsistencias en el espaciado tipográfico, problemas de justificación de línea (separando el número de su unidad) y errores de formato en modo matemático.

**La Solución:**
Utilizar el paquete `siunitx` y su comando estandarizado `\qty{}{}`. Esto garantiza que los números, prefijos y unidades sigan estrictamente las normas tipográficas internacionales del Sistema Internacional.

**Ejemplo de uso:**
```latex
% 1. Añadir al preámbulo:
\usepackage{siunitx}

% 2. Usar en el cuerpo del documento:
El circuito requiere una resistencia de \qty{10}{\k\ohm} y un capacitor de \qty{100}{\n\F}.
La frecuencia de operación del reloj principal es de \qty{16}{\MHz}.
```

## 7. Uso de Modo Matemático en Etiquetas de Gráficos (TikZ / Circuitikz)

**El Problema:**
Al colocar texto (*labels*) en componentes de Circuitikz o nodos de TikZ que incluyen subíndices (como `$R_1$`) o símbolos griegos (como `\Omega`), se suele omitir el entorno matemático, provocando fallos inmediatos al procesar el gráfico.

**La Solución:**
Toda notación científica, variable o unidad especial que resida dentro de los parámetros de un componente gráfico debe estar estrictamente encerrada entre signos de dólar `$ ... $`.

**Ejemplo incorrecto (genera error):**
```latex
\draw (0,0) to[R, l=$R_1 = 10 \Omega$] (2,0);
```

**Ejemplo correcto:**
```latex
\draw (0,0) to[R, l=$R_1 = \qty{10}{\k\ohm}$] (2,0);
```
## 8. Error de compilación con comillas dobles y texto monoespaciado (Babel Español)

**El Problema:**
Al compilar el documento surge el error `Bad character code (-1). \es@chf ->\char \hyphenchar \font`. Este problema ocurre por una interacción entre el paquete babel (configurado en español) y el uso de comillas dobles (") dentro de comandos de texto monoespaciado como `\texttt{}`. En español, babel convierte las comillas en caracteres activos, y al intentar buscar el guion de separación de sílabas en la fuente monoespaciada (cuyo valor es -1 por defecto), LaTeX colapsa.

**La Solución:**
Se deben realizar ajustes en el preámbulo para incluir la codificación T1 y desactivar los atajos conflictivos de babel. Además, se recomienda usar comillas simples dentro de bloques `\texttt{}`.

**Ejemplo de configuración corregida (Preámbulo):**
```latex
% 1. Añadir codificación de fuente T1:
\usepackage[T1]{fontenc}

% 2. Configurar babel para desactivar atajos de comillas:
\usepackage[spanish,es-noquoting,es-noshorthands]{babel}
```

**Ejemplo de uso corregido en texto:**
Preferir `flags='R'` en lugar de usar dobles comillas `flags="R"`.

## 9. Error de compilación con `\widthof` en entornos de lista (`enumitem` sin `calc`)

**El Problema:**
Al intentar ajustar dinámicamente el ancho de las etiquetas en un entorno de lista como `description` mediante el paquete `enumitem` usando la opción `labelwidth=\widthof{...}`, LaTeX produce el error:
```text
! Undefined control sequence.
<argument> \widthof
```
Esto ocurre debido a que la macro `\widthof` es provista por el paquete `calc` y no por `enumitem` de manera nativa. Sin importar `calc` en el preámbulo, LaTeX no reconoce la función `\widthof`.

**La Solución:**
Importar explícitamente el paquete `calc` en el preámbulo del documento.

**Ejemplo de configuración corregida (Preámbulo):**
```latex
\usepackage{enumitem}
\usepackage{calc} % Requerido para habilitar \widthof y otras macros de cálculo de medidas
```

**Ejemplo de uso corregido:**
```latex
\begin{description}[leftmargin=!,labelwidth=\widthof{\bfseries Programación Orientada a Objetos (POO)}]
    \item[\textbf{Programación Orientada a Objetos (POO)}] Paradigma de programación basado en el concepto de clases y objetos.
\end{description}
```

