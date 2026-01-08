"""
Generador de informes PDF para pacientes
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os


class GeneradorInformes:
    """Clase para generar informes PDF de pacientes"""
    
    def __init__(self, output_dir='informes'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._crear_estilos_personalizados()
    
    def _crear_estilos_personalizados(self):
        """Crea estilos personalizados para el documento"""
        self.styles.add(ParagraphStyle(
            name='TituloPersonalizado',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#2E7D32'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='SubtituloPersonalizado',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#388E3C'),
            spaceAfter=12,
            fontName='Helvetica-Bold'
        ))
    
    def generar_informe_paciente(self, paciente, mediciones=None, historial=None, pauta=None):
        """Genera un informe completo del paciente"""
        fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"informe_{paciente.apellidos}_{paciente.nombre}_{fecha_actual}.pdf"
        ruta_completa = os.path.join(self.output_dir, nombre_archivo)
        
        doc = SimpleDocTemplate(ruta_completa, pagesize=A4,
                              rightMargin=2*cm, leftMargin=2*cm,
                              topMargin=2*cm, bottomMargin=2*cm)
        
        elementos = []
        
        # Título principal
        titulo = Paragraph(f"INFORME NUTRICIONAL", self.styles['TituloPersonalizado'])
        elementos.append(titulo)
        elementos.append(Spacer(1, 0.5*cm))
        
        # Fecha del informe
        fecha = Paragraph(f"Fecha: {datetime.now().strftime('%d/%m/%Y')}", 
                         self.styles['Normal'])
        elementos.append(fecha)
        elementos.append(Spacer(1, 0.5*cm))
        
        # Datos del paciente
        elementos.append(Paragraph("DATOS DEL PACIENTE", self.styles['SubtituloPersonalizado']))
        
        datos_paciente = [
            ['Nombre completo:', paciente.nombre_completo()],
            ['RUT:', paciente.rut or 'N/A'],
            ['Fecha de nacimiento:', paciente.fecha_nacimiento.strftime('%d/%m/%Y') if paciente.fecha_nacimiento else 'N/A'],
            ['Sexo:', paciente.sexo or 'N/A'],
            ['Teléfono:', paciente.telefono or 'N/A'],
            ['Email:', paciente.email or 'N/A'],
        ]
        
        tabla_paciente = Table(datos_paciente, colWidths=[5*cm, 10*cm])
        tabla_paciente.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E8F5E9')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        
        elementos.append(tabla_paciente)
        elementos.append(Spacer(1, 0.7*cm))
        
        # Mediciones antropométricas
        if mediciones and len(mediciones) > 0:
            ultima_medicion = mediciones[0]
            elementos.append(Paragraph("MEDICIONES ANTROPOMÉTRICAS", self.styles['SubtituloPersonalizado']))
            elementos.append(Paragraph(f"Fecha: {ultima_medicion.fecha.strftime('%d/%m/%Y')}", 
                                     self.styles['Normal']))
            elementos.append(Spacer(1, 0.3*cm))
            
            datos_medicion = [
                ['Peso:', f"{ultima_medicion.peso} kg" if ultima_medicion.peso else 'N/A'],
                ['Altura:', f"{ultima_medicion.altura} cm" if ultima_medicion.altura else 'N/A'],
                ['IMC:', f"{ultima_medicion.imc}" if ultima_medicion.imc else 'N/A'],
                ['Perímetro cintura:', f"{ultima_medicion.perimetro_cintura} cm" if ultima_medicion.perimetro_cintura else 'N/A'],
                ['Perímetro cadera:', f"{ultima_medicion.perimetro_cadera} cm" if ultima_medicion.perimetro_cadera else 'N/A'],
                ['% Grasa corporal:', f"{ultima_medicion.porcentaje_grasa}%" if ultima_medicion.porcentaje_grasa else 'N/A'],
            ]
            
            tabla_medicion = Table(datos_medicion, colWidths=[5*cm, 10*cm])
            tabla_medicion.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E3F2FD')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ]))
            
            elementos.append(tabla_medicion)
            elementos.append(Spacer(1, 0.7*cm))
        
        # Historial clínico
        if historial and len(historial) > 0:
            ultimo_historial = historial[0]
            elementos.append(Paragraph("HISTORIAL CLÍNICO", self.styles['SubtituloPersonalizado']))
            
            if ultimo_historial.patologias:
                elementos.append(Paragraph(f"<b>Patologías:</b> {ultimo_historial.patologias}", 
                                         self.styles['Normal']))
            if ultimo_historial.alergias:
                elementos.append(Paragraph(f"<b>Alergias:</b> {ultimo_historial.alergias}", 
                                         self.styles['Normal']))
            if ultimo_historial.objetivo_principal:
                elementos.append(Paragraph(f"<b>Objetivo:</b> {ultimo_historial.objetivo_principal}", 
                                         self.styles['Normal']))
            
            elementos.append(Spacer(1, 0.7*cm))
        
        # Pauta nutricional
        if pauta:
            elementos.append(PageBreak())
            elementos.append(Paragraph("PAUTA NUTRICIONAL", self.styles['SubtituloPersonalizado']))
            elementos.append(Paragraph(f"<b>{pauta.titulo}</b>", self.styles['Normal']))
            elementos.append(Spacer(1, 0.3*cm))
            
            if pauta.calorias_objetivo:
                elementos.append(Paragraph(
                    f"<b>Calorías objetivo:</b> {pauta.calorias_objetivo} kcal/día", 
                    self.styles['Normal']))
            
            macros = f"Proteínas: {pauta.proteinas}g | Carbohidratos: {pauta.carbohidratos}g | Grasas: {pauta.grasas}g"
            elementos.append(Paragraph(f"<b>Macronutrientes:</b> {macros}", self.styles['Normal']))
            elementos.append(Spacer(1, 0.5*cm))
            
            # Comidas del día
            comidas = [
                ('DESAYUNO', pauta.desayuno),
                ('MEDIA MAÑANA', pauta.media_manana),
                ('ALMUERZO', pauta.almuerzo),
                ('MERIENDA', pauta.merienda),
                ('CENA', pauta.cena),
            ]
            
            for nombre_comida, contenido in comidas:
                if contenido:
                    elementos.append(Paragraph(f"<b>{nombre_comida}</b>", self.styles['Heading3']))
                    elementos.append(Paragraph(contenido, self.styles['Normal']))
                    elementos.append(Spacer(1, 0.3*cm))
            
            if pauta.indicaciones:
                elementos.append(Spacer(1, 0.5*cm))
                elementos.append(Paragraph("<b>INDICACIONES GENERALES</b>", self.styles['Heading3']))
                elementos.append(Paragraph(pauta.indicaciones, self.styles['Normal']))
        
        # Generar el PDF
        doc.build(elementos)
        return ruta_completa
    
    def generar_informe_evolucion(self, paciente, mediciones):
        """Genera un informe de evolución del paciente con gráficas de peso e IMC"""
        fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"evolucion_{paciente.apellidos}_{paciente.nombre}_{fecha_actual}.pdf"
        ruta_completa = os.path.join(self.output_dir, nombre_archivo)
        
        doc = SimpleDocTemplate(ruta_completa, pagesize=A4,
                              rightMargin=2*cm, leftMargin=2*cm,
                              topMargin=2*cm, bottomMargin=2*cm)
        
        elementos = []
        
        # Título
        titulo = Paragraph("INFORME DE EVOLUCIÓN", self.styles['TituloPersonalizado'])
        elementos.append(titulo)
        elementos.append(Spacer(1, 0.5*cm))
        
        elementos.append(Paragraph(f"Paciente: {paciente.nombre_completo()}", 
                                 self.styles['Heading2']))
        elementos.append(Paragraph(f"Fecha: {datetime.now().strftime('%d/%m/%Y')}", 
                                 self.styles['Normal']))
        elementos.append(Spacer(1, 1*cm))
        
        # Tabla de evolución
        if mediciones:
            elementos.append(Paragraph("EVOLUCIÓN DE MEDICIONES", self.styles['SubtituloPersonalizado']))
            
            # Encabezados
            datos_tabla = [['Fecha', 'Peso (kg)', 'IMC', 'Cintura (cm)', '% Grasa']]
            
            # Datos de las mediciones (ordenadas de más antigua a más reciente para ver evolución)
            mediciones_ordenadas = sorted(mediciones, key=lambda x: x.fecha)
            for med in mediciones_ordenadas:
                fila = [
                    med.fecha.strftime('%d/%m/%Y'),
                    str(med.peso) if med.peso else 'N/A',
                    str(med.imc) if med.imc else 'N/A',
                    str(med.perimetro_cintura) if med.perimetro_cintura else 'N/A',
                    str(med.porcentaje_grasa) if med.porcentaje_grasa else 'N/A',
                ]
                datos_tabla.append(fila)
            
            tabla_evolucion = Table(datos_tabla)
            tabla_evolucion.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E7D32')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F1F8E9')]),
            ]))
            
            elementos.append(tabla_evolucion)
            
            # Análisis de cambios
            if len(mediciones_ordenadas) >= 2:
                primera = mediciones_ordenadas[0]
                ultima = mediciones_ordenadas[-1]
                
                elementos.append(Spacer(1, 1*cm))
                elementos.append(Paragraph("ANÁLISIS DE CAMBIOS", self.styles['SubtituloPersonalizado']))
                
                if primera.peso and ultima.peso:
                    cambio_peso = ultima.peso - primera.peso
                    texto_peso = f"Cambio de peso: {cambio_peso:+.1f} kg"
                    elementos.append(Paragraph(texto_peso, self.styles['Normal']))
                
                if primera.imc and ultima.imc:
                    cambio_imc = ultima.imc - primera.imc
                    texto_imc = f"Cambio de IMC: {cambio_imc:+.1f}"
                    elementos.append(Paragraph(texto_imc, self.styles['Normal']))
        
        # Generar el PDF
        doc.build(elementos)
        return ruta_completa
