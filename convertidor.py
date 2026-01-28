import os
import sys
from pathlib import Path

class ConvertidorAutomatico:
    def __init__(self, directorio=None):
        self.directorio = directorio or os.getcwd()
        self.archivos_svg = []
        self.archivos_png = []
        self.archivos_pdf = []
        self.escanear_archivos()
    
    def escanear_archivos(self):
        """Escanea y encuentra todos los archivos convertibles"""
        print(f"\n📁 Escaneando: {self.directorio}")
        
        self.archivos_svg = []
        self.archivos_png = []
        self.archivos_pdf = []
        
        for archivo in os.listdir(self.directorio):
            ruta = os.path.join(self.directorio, archivo)
            if os.path.isfile(ruta):
                extension = archivo.lower()
                
                if extension.endswith('.svg'):
                    self.archivos_svg.append(archivo)
                elif extension.endswith('.png'):
                    self.archivos_png.append(archivo)
                elif extension.endswith('.pdf'):
                    self.archivos_pdf.append(archivo)
        
        print(f"🎯 SVG: {len(self.archivos_svg)} archivos")
        print(f"📸 PNG: {len(self.archivos_png)} archivos")
        print(f"📄 PDF: {len(self.archivos_pdf)} archivos")
    
    def mostrar_menu(self):
        """Muestra menú con archivos detectados"""
        while True:
            print("\n" + "="*60)
            print("🔄 CONVERTIDOR AUTOMÁTICO")
            print("="*60)
            
            # Mostrar archivos disponibles
            print("\n📂 ARCHIVOS ENCONTRADOS:")
            
            if self.archivos_svg:
                print("\n🎯 ARCHIVOS SVG:")
                for i, archivo in enumerate(self.archivos_svg, 1):
                    print(f"   {i:2}. {archivo}")
            
            if self.archivos_png:
                print("\n📸 ARCHIVOS PNG:")
                for i, archivo in enumerate(self.archivos_png, 1):
                    print(f"   {i:2}. {archivo}")
            
            if self.archivos_pdf:
                print("\n📄 ARCHIVOS PDF:")
                for i, archivo in enumerate(self.archivos_pdf, 1):
                    print(f"   {i:2}. {archivo}")
            
            print("\n" + "="*60)
            print("OPCIONES DE CONVERSIÓN:")
            print("1. 🎯 SVG → PNG (alta calidad)")
            print("2. 🎯 SVG → PDF")
            print("3. 📸 PNG → SVG")
            print("4. 📄 PDF → PNG (todas las páginas)")
            print("5. 🔄 Re-escanear directorio")
            print("6. 🚪 Salir")
            print("="*60)
            
            opcion = input("\n👉 Selecciona opción (1-6): ").strip()
            
            if opcion == '6':
                print("👋 ¡Hasta luego!")
                break
            
            elif opcion == '5':
                self.escanear_archivos()
                continue
            
            elif opcion in ['1', '2']:
                self.menu_svg(opcion)
            
            elif opcion == '3':
                self.menu_png()
            
            elif opcion == '4':
                self.menu_pdf()
    
    def menu_svg(self, tipo_conversion):
        """Menu para archivos SVG"""
        if not self.archivos_svg:
            print("\n❌ No hay archivos SVG en el directorio.")
            input("Presiona Enter para continuar...")
            return
        
        print(f"\n🎯 ARCHIVOS SVG DISPONIBLES:")
        for i, archivo in enumerate(self.archivos_svg, 1):
            print(f"{i:2}. {archivo}")
        
        try:
            seleccion = input("\n👉 Número del archivo a convertir: ").strip()
            if not seleccion:
                return
            
            idx = int(seleccion) - 1
            if 0 <= idx < len(self.archivos_svg):
                archivo = self.archivos_svg[idx]
                ruta_completa = os.path.join(self.directorio, archivo)
                
                if tipo_conversion == '1':  # SVG → PNG
                    dpi = input("DPI (300, 600, 1200, Enter=600): ").strip()
                    dpi = int(dpi) if dpi else 600
                    self.convertir_svg_png(ruta_completa, dpi)
                else:  # SVG → PDF
                    self.convertir_svg_pdf(ruta_completa)
            else:
                print("❌ Selección inválida")
        
        except ValueError:
            print("❌ Ingresa un número válido")
    
    def menu_png(self):
        """Menu para archivos PNG"""
        if not self.archivos_png:
            print("\n❌ No hay archivos PNG en el directorio.")
            input("Presiona Enter para continuar...")
            return
        
        print(f"\n📸 ARCHIVOS PNG DISPONIBLES:")
        for i, archivo in enumerate(self.archivos_png, 1):
            print(f"{i:2}. {archivo}")
        
        try:
            seleccion = input("\n👉 Número del archivo a convertir: ").strip()
            if not seleccion:
                return
            
            idx = int(seleccion) - 1
            if 0 <= idx < len(self.archivos_png):
                archivo = self.archivos_png[idx]
                ruta_completa = os.path.join(self.directorio, archivo)
                self.convertir_png_svg(ruta_completa)
            else:
                print("❌ Selección inválida")
        
        except ValueError:
            print("❌ Ingresa un número válido")
    
    def menu_pdf(self):
        """Menu para archivos PDF"""
        if not self.archivos_pdf:
            print("\n❌ No hay archivos PDF en el directorio.")
            input("Presiona Enter para continuar...")
            return
        
        print(f"\n📄 ARCHIVOS PDF DISPONIBLES:")
        for i, archivo in enumerate(self.archivos_pdf, 1):
            # Mostrar tamaño del archivo
            ruta = os.path.join(self.directorio, archivo)
            tamano = os.path.getsize(ruta) // 1024  # KB
            print(f"{i:2}. {archivo} ({tamano} KB)")
        
        try:
            seleccion = input("\n👉 Número del archivo a convertir: ").strip()
            if not seleccion:
                return
            
            idx = int(seleccion) - 1
            if 0 <= idx < len(self.archivos_pdf):
                archivo = self.archivos_pdf[idx]
                ruta_completa = os.path.join(self.directorio, archivo)
                
                dpi = input("DPI para PNG (150, 300, 600, Enter=300): ").strip()
                dpi = int(dpi) if dpi else 300
                self.convertir_pdf_png(ruta_completa, dpi)
            else:
                print("❌ Selección inválida")
        
        except ValueError:
            print("❌ Ingresa un número válido")
    
    def convertir_svg_png(self, svg_path, dpi=600):
        """Convierte SVG a PNG con máxima calidad"""
        try:
            import cairosvg
            
            nombre_base = Path(svg_path).stem
            png_path = os.path.join(self.directorio, f"{nombre_base}_{dpi}dpi.png")
            
            print(f"🔄 Convirtiendo: {Path(svg_path).name} → PNG ({dpi} DPI)...")
            
            cairosvg.svg2png(
                url=svg_path,
                write_to=png_path,
                dpi=dpi,
                background_color='white',
                scale=1.0
            )
            
            # Verificar tamaño resultante
            if os.path.exists(png_path):
                from PIL import Image
                with Image.open(png_path) as img:
                    ancho, alto = img.size
                tamano = os.path.getsize(png_path) // 1024
                print(f"✅ Convertido: {Path(png_path).name}")
                print(f"   📐 Dimensiones: {ancho}×{alto} px")
                print(f"   📊 Tamaño: {tamano} KB")
                print(f"   🎯 Calidad: {dpi} DPI")
            else:
                print("❌ Error: No se creó el archivo PNG")
            
            return png_path
            
        except ImportError:
            print("❌ Error: cairosvg no está instalado")
            print("   Ejecuta: pip install cairosvg")
            return None
        except Exception as e:
            print(f"❌ Error en conversión: {e}")
            return None
    
    def convertir_svg_pdf(self, svg_path):
        """Convierte SVG a PDF"""
        try:
            import cairosvg
            
            nombre_base = Path(svg_path).stem
            pdf_path = os.path.join(self.directorio, f"{nombre_base}.pdf")
            
            print(f"🔄 Convirtiendo: {Path(svg_path).name} → PDF...")
            
            cairosvg.svg2pdf(url=svg_path, write_to=pdf_path)
            
            if os.path.exists(pdf_path):
                tamano = os.path.getsize(pdf_path) // 1024
                print(f"✅ Convertido: {Path(pdf_path).name}")
                print(f"   📊 Tamaño: {tamano} KB")
            else:
                print("❌ Error: No se creó el archivo PDF")
            
            return pdf_path
            
        except ImportError:
            print("❌ Error: cairosvg no está instalado")
            print("   Ejecuta: pip install cairosvg")
            return None
        except Exception as e:
            print(f"❌ Error en conversión: {e}")
            return None
    
    def convertir_png_svg(self, png_path):
        """Convierte PNG a SVG con calidad óptima"""
        try:
            import vtracer
            
            nombre_base = Path(png_path).stem
            svg_path = os.path.join(self.directorio, f"{nombre_base}.svg")
            
            print(f"🔄 Convirtiendo: {Path(png_path).name} → SVG...")
            
            # Parámetros para buena calidad
            vtracer.convert_image_to_svg_py(
                png_path,
                svg_path,
                colormode='color',
                hierarchical='stacked',
                mode='spline',
                filter_speckle=12,
                color_precision=6,
                corner_threshold=60,
                max_iterations=15
            )
            
            if os.path.exists(svg_path):
                tamano = os.path.getsize(svg_path) // 1024
                print(f"✅ Convertido: {Path(svg_path).name}")
                print(f"   📊 Tamaño: {tamano} KB")
                print("   ⚠️  Nota: PNG→SVG es vectorización, puede perder detalles")
            else:
                print("❌ Error: No se creó el archivo SVG")
            
            return svg_path
            
        except ImportError:
            print("❌ Error: vtracer no está instalado")
            print("   Ejecuta: pip install vtracer")
            return None
        except Exception as e:
            print(f"❌ Error en conversión: {e}")
            return None
    
    def convertir_pdf_png(self, pdf_path, dpi=300):
        """Convierte PDF a PNG (cada página)"""
        try:
            from pdf2image import convert_from_path
            
            nombre_base = Path(pdf_path).stem
            
            print(f"🔄 Convirtiendo PDF a PNG ({dpi} DPI)...")
            print("   Esto puede tardar unos segundos...")
            
            # Convertir todas las páginas
            imagenes = convert_from_path(pdf_path, dpi=dpi)
            
            archivos_creados = []
            for i, imagen in enumerate(imagenes):
                png_path = os.path.join(self.directorio, f"{nombre_base}_pagina_{i+1}_{dpi}dpi.png")
                imagen.save(png_path, 'PNG', quality=95)
                
                # Obtener tamaño de la imagen
                from PIL import Image
                with Image.open(png_path) as img:
                    ancho, alto = img.size
                
                tamano = os.path.getsize(png_path) // 1024
                print(f"   ✅ Página {i+1}: {ancho}×{alto} px, {tamano} KB")
                archivos_creados.append(png_path)
            
            print(f"\n📊 Resumen: {len(archivos_creados)} páginas convertidas")
            print(f"🎯 Calidad: {dpi} DPI")
            print(f"📁 Guardadas en: {self.directorio}")
            
            return archivos_creados
            
        except ImportError:
            print("❌ Error: pdf2image no está instalado")
            print("   Ejecuta: pip install pdf2image")
            print("\n💡 Además, necesitas instalar poppler:")
            print("   Ubuntu/Debian: sudo apt-get install poppler-utils")
            print("   Mac: brew install poppler")
            return []
        except Exception as e:
            print(f"❌ Error en conversión: {e}")
            return []

def verificar_dependencias():
    """Verifica e instala dependencias automáticamente"""
    print("🔍 Verificando dependencias...")
    
    dependencias = {
        'cairosvg': 'cairosvg',
        'vtracer': 'vtracer',
        'pdf2image': 'pdf2image',
        'PIL': 'pillow'
    }
    
    faltantes = []
    
    # Verificar cada dependencia
    for modulo, paquete in dependencias.items():
        try:
            if modulo == 'PIL':
                __import__('PIL')
            else:
                __import__(modulo)
            print(f"   ✅ {modulo}")
        except ImportError:
            print(f"   ❌ {modulo}")
            faltantes.append(paquete)
    
    # Instalar dependencias faltantes
    if faltantes:
        print(f"\n📦 Instalando {len(faltantes)} dependencia(s)...")
        for paquete in faltantes:
            try:
                import subprocess
                subprocess.check_call([sys.executable, "-m", "pip", "install", paquete, "--quiet"])
                print(f"   ✅ {paquete} instalado")
            except:
                print(f"   ❌ Error instalando {paquete}")
    
    print("\n✅ Dependencias verificadas")
    
    # Verificar poppler para pdf2image
    try:
        import subprocess
        result = subprocess.run(['which', 'pdftoppm'], capture_output=True, text=True)
        if result.returncode != 0:
            print("\n⚠️  ATENCIÓN: Necesitas poppler para convertir PDF")
            print("   En Ubuntu/Debian: sudo apt-get install poppler-utils")
            print("   En Fedora: sudo dnf install poppler-utils")
            print("   En Mac: brew install poppler")
    except:
        pass

def main():
    """Función principal"""
    print("="*60)
    print("🔄 CONVERTIDOR AUTOMÁTICO SVG/PNG/PDF")
    print("="*60)
    print("📂 Directorio actual:", os.getcwd())
    print("="*60)
    
    # Verificar dependencias
    verificar_dependencias()
    
    # Crear e iniciar convertidor
    convertidor = ConvertidorAutomatico()
    convertidor.mostrar_menu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrumpido")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        input("Presiona Enter para salir...")