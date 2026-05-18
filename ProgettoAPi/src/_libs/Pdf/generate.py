from fpdf import FPDF
import io
import os
import tempfile

class AnnuarioPDF(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 16)
        self.cell(0, 10, "ANNUARIO SCOLASTICO Europa Unita", align="C", ln=True)
        self.ln(5)

def create_annuario(dati_classi):
    pdf = AnnuarioPDF()

    cols = 5
    rows_per_page = 6
    margin = 10
    page_width = pdf.w - (2 * margin)
    col_width = page_width / cols
    row_height = 42 

    img_h = 22
    qr_size = 12
    
    with tempfile.TemporaryDirectory() as tmpdir:
        for classe_index, classe in enumerate(dati_classi):
            pdf.add_page()
            
            pdf.set_font("helvetica", "B", 14)
            pdf.set_text_color(50, 50, 150)
            pdf.cell(0, 10, f"Classe: {classe['nome_classe']}", ln=True, align='L')
            pdf.set_text_color(0, 0, 0)
            pdf.ln(2)

            x_start = margin
            y_base = pdf.get_y()

            for i, studente in enumerate(classe['studenti']):
                if i > 0 and i % 30 == 0:
                    pdf.add_page()
                    y_base = pdf.get_y() + 10

                col = i % cols
                row = (i // cols) % rows_per_page
                
                x = x_start + (col * col_width)
                y = y_base + (row * row_height)

                foto_x = x + (col_width - 20) / 2
                
                if os.path.exists(studente['person']):
                    pdf.image(studente['person'], x=foto_x, y=y, w=20, h=img_h)
                else:
                    pdf.set_fill_color(240, 240, 240)
                    pdf.rect(foto_x, y, 20, img_h, style='F')

                pdf.set_xy(x, y + img_h + 1)
                pdf.set_font("helvetica", "B", 7)
                pdf.multi_cell(col_width, 4, studente['name'].upper(), align="C")
                
                qr_x = x + (col_width - qr_size) / 2
                qr_y = y + img_h + 8 
                
                if isinstance(studente['qr_img'], (bytes, bytearray)):
                    qr_path = os.path.join(tmpdir, f"qr_{classe_index}_{i}.png")
                    with open(qr_path, "wb") as qr_file:
                        qr_file.write(studente['qr_img'])
                    pdf.image(qr_path, x=qr_x, y=qr_y, w=qr_size, h=qr_size)
                else:
                    pdf.set_fill_color(220, 220, 220)
                    pdf.rect(qr_x, qr_y, qr_size, qr_size, style='F')

            if 'foto_gruppo' in classe and os.path.exists(classe['foto_gruppo']):
                if pdf.get_y() > 200: 
                    pdf.add_page()
                
                pdf.ln(15) 
                y_foto_classe = pdf.get_y()
                
                larghezza_foto_classe = page_width - 20
                x_foto_classe = (pdf.w - larghezza_foto_classe) / 2
                
                pdf.set_font("helvetica", "I", 10)
                pdf.cell(0, 8, f"Foto di gruppo - Classe {classe['nome_classe']}", ln=True, align='C')
                pdf.image(classe['foto_gruppo'], x=x_foto_classe, y=pdf.get_y(), w=larghezza_foto_classe)

    output = pdf.output(dest='S')
    return output.encode('latin-1')
