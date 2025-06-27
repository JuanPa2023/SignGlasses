# 🎯 SignGlasses – Gafas Inteligentes para Comunicación Inclusiva

**Transformá la barrera de comunicación en conexión real**: SignGlasses traduce Lengua de Señas Argentina (LSA) a voz y voz hablada a texto, en tiempo real.

---

## 📌 Contenido

1.0 🔗 [Introducción](#10-introducción)  
2.0 📲 [Características Principales](#20-características-principales)  
&nbsp;&nbsp;2.1 🔄 [Reconocimiento de Señas en Tiempo Real](#21-reconocimiento-de-señas-en-tiempo-real)  
&nbsp;&nbsp;2.2 🗣️ [Transcripción de Voz a Texto](#22-transcripción-de-voz-a-texto)  
&nbsp;&nbsp;2.3 🔁 [Comunicación Bidireccional](#23-comunicación-bidireccional)  
&nbsp;&nbsp;2.4 🎨 [Diseño Ergonómico y Portátil](#24-diseño-ergonómico-y-portátil)  
3.0 💻 [Recursos y Tecnologías](#30-recursos-y-tecnologías)  
&nbsp;&nbsp;3.1 🛠️ [Hardware Integrado](#31-hardware-integrado)  
&nbsp;&nbsp;3.2 📚 [Software y Bibliotecas](#32-software-y-bibliotecas)  
4.0 🔩 [Arquitectura y Diseño del Sistema](#40-arquitectura-y-diseño-del-sistema)  
&nbsp;&nbsp;4.1 📷 [Sistema de Visión y Sensores](#41-sistema-de-visión-y-sensores)  
&nbsp;&nbsp;4.2 🎤 [Captura de Audio y Síntesis](#42-captura-de-audio-y-síntesis)  
&nbsp;&nbsp;4.3 🖥️ [Procesamiento Embebido vs. Externo](#43-procesamiento-embebido-vs-externo)  
5.0 💡 [Diseño Electrónico](#50-diseño-electrónico)  
&nbsp;&nbsp;5.1 🔌 [Diagramas de Circuito](#51-diagramas-de-circuito)  
&nbsp;&nbsp;5.2 📋 [Especificaciones de Componentes](#52-especificaciones-de-componentes)  
6.0 🛠️ [Instalación y Uso](#60-instalación-y-uso)  
&nbsp;&nbsp;6.1 🔧 [Montaje del Hardware](#61-montaje-del-hardware)  
&nbsp;&nbsp;6.2 💾 [Instalación del Software](#62-instalación-del-software)  
&nbsp;&nbsp;6.3 ▶️ [Ejecución del Prototipo](#63-ejecución-del-prototipo)  
7.0 📹 [Demostración en Acción](#70-demostración-en-acción)  
8.0 🚀 [Roadmap & Futuras Mejoras](#80-roadmap--futuras-mejoras)  
&nbsp;&nbsp;8.1 🔋 [Autonomía y Batería Integrada](#81-autonomía-y-batería-integrada)  
&nbsp;&nbsp;8.2 😊 [Reconocimiento de Expresiones Faciales](#82-reconocimiento-de-expresiones-faciales)  
&nbsp;&nbsp;8.3 📐 [Miniaturización y Estética](#83-miniaturización-y-estética)  
9.0 📝 [Agradecimientos](#90-agradecimientos)

---

## 1.0 🔗 Introducción

SignGlasses es un wearable innovador diseñado para derribar la barrera lingüística entre personas sordas y oyentes. Combina visión artificial, IA y procesamiento de señales para ofrecer una comunicación inclusiva, fluida y en tiempo real.

---

## 2.0 📲 Características Principales

### 2.1 🔄 Reconocimiento de Señas en Tiempo Real  
- Captura de gestos manuales con cámara integrada.  
- Modelos CNN+MediaPipe para detección rápida (> 90 % de precisión).  

### 2.2 🗣️ Transcripción de Voz a Texto  
- Micrófono direccional para capturar audio en entornos ruidosos.  
- ASR y NLP locales para mostrar texto instantáneo en pantalla OLED.  

### 2.3 🔁 Comunicación Bidireccional  
- LSA → voz sintetizada en español.  
- Voz → texto proyectado sobre el campo visual del usuario sordo.  

### 2.4 🎨 Diseño Ergonómico y Portátil  
- Montura ligera, ajustable y discreta.  
- Futuras versiones con electrónica embebida y batería interna.

---

## 3.0 💻 Recursos y Tecnologías

### 3.1 🛠️ Hardware Integrado  
- Raspberry Pi Zero 2W  
- Cámara OV4547 (5 MP)  
- Micrófono INMP441  
- Pantalla OLED SSD1306 (0.96″)  
- Amplificador PAM8403  

### 3.2 📚 Software y Bibliotecas  
- **Visión por Computadora:** OpenCV, MediaPipe  
- **Deep Learning:** TensorFlow, PyTorch  
- **ASR & NLP:** SpeechRecognition, Transformers  
- **Lenguaje:** Python 3.x  

---

## 4.0 🔩 Arquitectura y Diseño del Sistema

### 4.1 📷 Sistema de Visión y Sensores  
Bloque de captura de imagen, preprocesamiento y extracción de características.

### 4.2 🎤 Captura de Audio y Síntesis  
Micrófono direccional + modelo ASR + motor de síntesis TTS.

### 4.3 🖥️ Procesamiento Embebido vs. Externo  
- **Prototipo v0:** IA ejecutándose en PC externa.  
- **v1 & v2:** Migración a hardware local con optimización de modelos.

---

## 5.0 💡 Diseño Electrónico

### 5.1 🔌 Diagramas de Circuito  
Agregá aquí tu diagrama en PNG/SVG dentro de `docs/` o `images/`.

### 5.2 📋 Especificaciones de Componentes  
- Voltajes, corrientes, conexiones I²C/SPI, pines GPIO detallados.

---

## 6.0 🛠️ Instalación y Uso

### 6.1 🔧 Montaje del Hardware  
1. Conectá cámara y micrófono a la Raspberry Pi Zero 2W.  
2. Ensamblá pantalla OLED y amplificador en la montura.

### 6.2 💾 Instalación del Software  
```bash
git clone https://github.com/TU_USUARIO/SignGlasses.git
cd SignGlasses
pip install -r requirements.txt
