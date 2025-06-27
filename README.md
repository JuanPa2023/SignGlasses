# 👓 SignGlasses – Proyecto de Ingeniería Mecatrónica

_Dispositivo portátil de interpretación automática para personas sordas._

## 🏫 Universidad Nacional de Lomas de Zamora  
**Facultad de Ingeniería – Cátedra de Vigilancia Tecnológica**  
**Autores:** Ignacio Ezequiel Gauna (DNI 42.874.840), Juan Pablo Saracino (DNI 42.113.281)  
**Año:** 2025

---

## 📌 Índice

- [🎯 Motivaciones](#-motivaciones)
- [🧩 Problemática y Oportunidad Tecnológica](#-problemática-y-oportunidad-tecnológica)
- [💡 Descripción de la Propuesta](#-descripción-de-la-propuesta)
- [⚙️ Funcionalidad del Dispositivo](#-funcionalidad-del-dispositivo)
- [🧠 Tecnología y Arquitectura del Sistema](#-tecnología-y-arquitectura-del-sistema)
- [📈 Alcance](#-alcance)
- [👨‍🏫 Docentes de Apoyo](#-docentes-de-apoyo)
- [✅ Especificación de Requerimientos](#-especificación-de-requerimientos)
- [🔌 Diseño Funcional](#-diseño-funcional)
- [📍 Pinout del Microcontrolador](#-pinout-del-microcontrolador)
- [💰 Costos y Plazos de Entrega](#-costos-y-plazos-de-entrega)

---

## 🎯 Motivaciones

El proyecto surge con el fin de brindar una solución socio-tecnológica que rompa la barrera lingüística entre personas sordas y oyentes, especialmente en contextos donde no hay intérpretes disponibles, como hospitales, escuelas, trámites, o ambientes laborales. 

---

## 🧩 Problemática y Oportunidad Tecnológica

Muchas personas sordas se enfrentan a la falta de herramientas de comunicación adaptadas. El objetivo es desarrollar un dispositivo portátil que permita:

1. Traducir Lengua de Señas Argentina (LSA) a voz.
2. Transcribir voz hablada a texto visible para personas sordas.

   ![image](https://github.com/user-attachments/assets/9898e130-32c2-41b1-828b-ab4058537c97)


---

## 💡 Descripción de la Propuesta

Se propone el desarrollo de unas gafas inteligentes llamadas **"SignGlasses"**, que permitan una traducción bidireccional:

- **Portabilidad:** livianas y cómodas.
- **Ergonomía:** diseño discreto y adaptable.
- **Autonomía:** funcionamiento sin asistencia externa.
![image](https://github.com/user-attachments/assets/cc5addf6-0cd0-4d01-8684-e408f129bc58)

---

## ⚙️ Funcionalidad del Dispositivo

El dispositivo tendrá dos modos de operación principales:

### 1. LSA → Voz (Persona sorda → Oyente)
- Captura de gestos con cámara.
- Reconocimiento con redes neuronales.
- Síntesis de voz en español.

### 2. Voz → Texto (Oyente → Persona sorda)
- Captura de audio con micrófono.
- Transcripción por reconocimiento de voz.
- Proyección de texto en pantalla integrada.

---

## 🧠 Tecnología y Arquitectura del Sistema

- **Visión artificial:** OpenCV, MediaPipe.
- **Deep Learning:** TensorFlow, PyTorch.
- **Reconocimiento de voz:** ASR (Automatic Speech Recognition).
- **Procesamiento de lenguaje:** NLP.
- **Hardware:** Raspberry Pi Zero 2W, cámara, micrófono, pantalla OLED, amplificador de audio.

> ⚠️ Por cuestiones de rendimiento, la IA se ejecutará inicialmente en una PC externa, manteniendo el hardware embebido para las demás tareas.

---

## 📈 Alcance

El primer prototipo:

- Se conectará a una PC para el procesamiento.
- Tendrá componentes visibles.
- No incluirá reconocimiento facial ni batería interna.

Versión futura (objetivo):

- Totalmente autónomo y portátil.
- Integración de la electrónica en la montura.
- Reconocimiento completo de expresiones faciales.

---

## 👨‍🏫 Docentes de Apoyo

- **Diego López:** Instrumentación industrial (electrónica y comunicación).
- **Daniel Omar Esmoris:** Redes de comunicaciones industriales (comunicación cámara y motores).

---

## ✅ Especificación de Requerimientos

### Funcionales

- Traducción LSA → voz.
- Transcripción voz → texto.
- Seguimiento de manos.
- Proyección de texto en pantalla.

### No funcionales

- Diseño ergonómico y estético.
- Autonomía total (versión final).
- Latencia < 2s.
- Precisión de reconocimiento >90%.

### Técnicos

- Sincronización de sensores y actuadores.
- Ejecución local de modelos IA sin conexión.
- Capacidad de actualización.

---

## 🔌 Diseño Funcional

![image](https://github.com/user-attachments/assets/ef6916fb-c80a-49b1-bee0-212ee2517911)


---

## 📍 Pinout del Microcontrolador

![image](https://github.com/user-attachments/assets/02bc291e-e018-4a9b-af88-3c8914a4b226)


---

## 💰 Costos y Plazos de Entrega

| Componente                         | Precio ARS | Precio USD | Proveedor            | Fecha de Compra | Fecha de Entrega |
|-----------------------------------|------------|------------|----------------------|------------------|------------------|
| Cámara OV4547 ojo de pez 5MP      | $10.829    | $10,18     | Starware             | 15/01/2025       | 20/01/2025       |
| Cable cámara Raspberry Pi 15cm    | $1.959     | $1,84      | Starware             | 15/01/2025       | 20/01/2025       |
| Amplificador audio PAM8403        | $2.239     | $2,10      | Starware             | 15/01/2025       | 20/01/2025       |
| Pantalla OLED SSD1306 0.96"       | $5.549     | $5,21      | Starware             | 15/01/2025       | 20/01/2025       |
| Raspberry Pi Zero 2WH             | $38.957    | $36,61     | Siranet              | 09/01/2025       | 11/01/2025       |
| Micrófono INMP441                 | $7.676     | $7,21      | Synergeek            | 26/03/2025       | 31/03/2025       |
| **Total**                         | **$67.209**| **$63,16** |                      |                  |                  |

> Dólar de referencia: 1064,15 ARS/USD

---

## 📬 Contacto

**Ignacio Ezequiel Gauna**
gauna.ignaciosh@hotmail.com
**Juan Pablo Saracino**  
saracinojuanpablo@gmail.com
Facultad de Ingeniería – UNLZ  
Proyecto: _SignGlasses_  
