import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io
from datetime import datetime

st.set_page_config(
    page_title="Remplir mon PDF",
    page_icon="📄",
    layout="centered"
)

st.title("📄 Remplir mon document PDF")
st.markdown("---")

with st.form("formulaire_pdf"):
    st.subheader("Informations à remplir")
    
    nom = st.text_input("Nom complet *")
    email = st.text_input("Email *")
    telephone = st.text_input("Téléphone")
    date = st.date_input("Date", datetime.now())
    message = st.text_area("Message")
    
    accord = st.checkbox("J'accepte les conditions *")
    
    submitted = st.form_submit_button("📥 Générer mon PDF", use_container_width=True)
    
    if submitted:
        if not nom or not email or not accord:
            st.error("Veuillez remplir tous les champs obligatoires (*)")
        else:
            with st.spinner("Génération du PDF en cours..."):
                buffer = io.BytesIO()
                c = canvas.Canvas(buffer, pagesize=A4)
                
                c.setFont("Helvetica-Bold", 16)
                c.drawString(100, 800, "Document rempli")
                
                c.setFont("Helvetica", 10)
                c.drawString(100, 780, f"Généré le : {datetime.now().strftime('%d/%m/%Y %H:%M')}")
                
                c.line(100, 770, 500, 770)
                
                c.setFont("Helvetica", 12)
                y = 740
                
                champs = [
                    ("Nom", nom),
                    ("Email", email),
                    ("Téléphone", telephone),
                    ("Date", date.strftime('%d/%m/%Y')),
                    ("Message", message)
                ]
                
                for champ, valeur in champs:
                    c.setFont("Helvetica-Bold", 11)
                    c.drawString(100, y, f"{champ} :")
                    c.setFont("Helvetica", 11)
                    c.drawString(200, y, str(valeur))
                    y -= 30
                
                c.save()
                buffer.seek(0)
                
                st.success("✅ PDF généré avec succès !")
                st.download_button(
                    label="📥 Télécharger mon PDF",
                    data=buffer,
                    file_name=f"document_{nom.replace(' ', '_')}.pdf",
                    mime="application/pdf"
                )

st.markdown("---")
st.caption("👆 Remplissez le formulaire et téléchargez votre PDF")