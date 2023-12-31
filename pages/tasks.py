# from __future__ import absolute_import, unicode_literals
#
# from datetime import datetime
#
# from django.conf import settings
# from celery import shared_task
# from .models import Questions, Answers
# from django.contrib.auth.models import User
# from django.core.mail import EmailMessage
# from reportlab.pdfgen import canvas
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.pdfbase import pdfmetrics
# from reportlab.platypus import Paragraph
# from reportlab.lib.styles import ParagraphStyle
# from reportlab.lib.pagesizes import A4
# from bs4 import BeautifulSoup
# import os
# import io
#
#
#
# @shared_task
# def generate_report(user_id, selected_date=None):
#     user = User.objects.get(id=user_id)
#     email = user.email
#     if selected_date:
#         if user.is_superuser:
#             user_que = Questions.objects.filter(published_date__date=selected_date)
#         else:
#             user_que = Questions.objects.filter(user=user_id, published_date__date=selected_date)
#     else:
#         if user.is_superuser:
#             user_que = Questions.objects.all()
#         else:
#             user_que = Questions.objects.filter(user=user_id)
#
#     if not user_que.exists():
#         return None
#
#     pdfmetrics.registerFont(TTFont("Times_Bold", "timesbd.ttf"))
#
#     buffer = io.BytesIO()
#     p = canvas.Canvas(buffer, pagesize=A4)
#
#     width, height = A4
#     my_style = ParagraphStyle('paragraph style', fontName='Times_Bold', fontSize=17, alignment=1)
#     ansStyle = ParagraphStyle('ans style', alignment=1, fontSize=17, fontName='Times_Bold')
#     queStyle = ParagraphStyle('que style', fontName='Times_Bold', fontSize=13, alignment=0, leading=14)
#     ansText = ParagraphStyle('ans_text style', fontName='Times_Bold', fontSize=13, alignment=0)
#     dateParagraphStyle = ParagraphStyle('date style', fontName='Times_Bold', fontSize=11, alignment=1, textColor='coral')
#     headerStyle = ParagraphStyle('header style', fontName='Times_Bold', fontSize=40, alignment=1, leading=40)
#     date_time_style = ParagraphStyle('datetime style', fontName='Times_Bold', fontSize=14, alignment=1, leading=20)
#
#     static_dir = os.path.join(settings.STATIC_ROOT, 'img', 'stack-overflow-logo.png')
#     p.drawImage(static_dir, width/2-275, height-225, 550, 200)
#     date_time = Paragraph(f"Raporun gönderildiği tarih {datetime.now().strftime('%d %B %Y %H:%M')}", date_time_style)
#     date_time.wrapOn(p,170, 100)
#     date_time.drawOn(p, width-200, height-50)
#
#     if selected_date:
#         text = f"{selected_date.strftime('%d %B %Y')} Tarihine ait Sorular ve Cevaplar Raporu"
#     else:
#         text = "Sorular ve Cevaplar Raporu"
#     header = Paragraph(text, headerStyle)
#     header.wrapOn(p, 350, 500)
#     header.drawOn(p, width/2-175, height-450)
#
#
#     p.roundRect(width/2-275, 150, 550, 90, 10)
#     p.setFont('Times_Bold', 20)
#     p.drawString(50, 190, f"Toplam soru sayısı :")
#     p.drawString(500, 190, f"{user_que.count()}")
#
#     p.setFillColorRGB(0.996, 0.891, 0.765)
#     p.circle(width/2+3, height-(height-15), 13, fill=1)
#     p.setFillColorRGB(0, 0, 0)
#     p.setFontSize(14)
#     p.drawString(width/2 , height-(height-10), str(p.getPageNumber()))
#     p.showPage()
#
#     for que in user_que:
#         p.roundRect(width/2-275, height-385, 550, 370, 15)
#
#         date1 = Paragraph(f"{que.published_date.astimezone().strftime('%d %B %Y %H:%M')}", dateParagraphStyle)
#         date1.wrapOn(p, 400, 700)
#         date1.drawOn(p, width-320, height-60)
#
#         p1 = Paragraph(f"<b>{que.title}</b>", my_style)
#         p1.wrapOn(p, 200, 700)
#         p1.drawOn(p, width-400, height-50)
#         p.setFont("Times_Bold", 14)
#
#         p.line(50, height-70, 530, height-70)
#
#         soup = BeautifulSoup(que.context, 'html.parser')
#         for img in soup.find_all('img'):
#             img.extract()
#         text_content = soup.get_text(strip=True)
#
#         que_paragraph = Paragraph(f"Soru : <br/>{text_content}", queStyle)
#         que_paragraph.wrapOn(p, 505, 700)
#
#         if len(text_content) < 150:
#             que_paragraph.drawOn(p, width-550, height-120)
#             ans_text_y = height-200
#             ans_line_y = height-220
#             ans_y = height-250
#         else:
#             que_paragraph.drawOn(p, width-550, height-250)
#             ans_text_y = height-270
#             ans_line_y = height-290
#             ans_y = height-320
#
#
#         user_ans = Answers.objects.filter(answer_to_the_question=que)
#
#         ans_paragraph = Paragraph("<b>Cevaplar</b>", ansStyle)
#         ans_paragraph.wrapOn(p, 200, 700)
#         ans_paragraph.drawOn(p, width-400, ans_text_y)
#
#
#         p.line(50, ans_line_y, 530, ans_line_y)
#
#
#         if not user_ans.exists():
#             ans_text = "Bu soru için bir cevap yok!"
#             ans_paragraph = Paragraph(ans_text, ansText)
#             ans_paragraph.wrapOn(p, 200, 700)
#             ans_paragraph.drawOn(p, 50, ans_y)
#             ans_y -= 20
#         else:
#             for i, ans in enumerate(user_ans, start=1):
#                 ans_text = f"{i}. {BeautifulSoup(ans.answer, 'html.parser').get_text(strip=True)} - <font size='12' face='Times_Bold' color='gray'>{ans.user}-{ans.published_date.astimezone().strftime('%d %B %Y %H:%M')}</font>"
#                 ans_paragraph = Paragraph(ans_text, ansText)
#                 ans_paragraph.wrapOn(p, 500, 700)
#                 ans_paragraph.drawOn(p, 50, ans_y)
#                 ans_y -= 20
#
#
#         page_num = str(p.getPageNumber())
#         if len(page_num) == 1:
#             num_width = width/2 + 3
#         else:
#             num_width = width/2 + 7
#
#
#         p.setFillColorRGB(0.996, 0.891, 0.765)
#         p.circle(num_width, height-(height-15), 13, fill=1)
#         p.setFillColorRGB(0, 0, 0)
#         p.drawString(width/2, height-(height-10), page_num)
#
#
#         space = 400
#
#         if height - space < 50:
#             p.showPage()
#             height = A4[1]
#         else:
#             height -= space
#
#     p.save()
#
#
#     message = EmailMessage('over-flow', 'Sorularınız ve cevapları pdf içerisinde dir.', 'yildirimuhammed058@gmail.com', [email])
#     message.attach('rapor.pdf', buffer.getvalue(), 'application/pdf')
#     message.send()


from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.conf import settings
from pages.models import Questions, Answers
from datetime import datetime
from PIL import Image
import PyPDF2
import pdfkit
import os
import io


@shared_task
def GenerateReport(user_id, selected_date=None):
    user = User.objects.get(id=user_id)
    if selected_date:
        if user.is_superuser:
            user_questions = Questions.objects.filter(published_date__date=selected_date)
        else:
            user_questions = Questions.objects.filter(user=user_id, published_date__date=selected_date)
    else:
        if user.is_superuser:
            user_questions = Questions.objects.all()
        else:
            user_questions = Questions.objects.filter(user=user_id)

    if not user_questions.exists():
        return None

    image_path = os.path.join(settings.STATIC_ROOT, 'img', 'stack-overflow-logo.png')


    pdf_name = 'report.pdf'
    config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF_PATH)



    context = {
        "questions": user_questions,
        "get_report_date": datetime.now().strftime("%d %B %Y"),
        "image_path": image_path,
        "selected_date": selected_date,
    }

    rendered_html = render_to_string('pages/report_pdf.html', context)


    pdfkit.from_string(rendered_html, pdf_name, configuration=config, options={"enable-local-file-access": "",
                                                                               "encoding": "UTF-8",
                                                                               "load-media-error-handling": "ignore"
                                                                               })


    with open(pdf_name, 'rb') as pdf_file:
        pdf_content = pdf_file.read()


    message = EmailMessage('stackoverflow', 'Sorularınız ve cevapları pdf içerisinde dir.',
                           'yildirimuhammed058@gmail.com', [user.email])
    message.attach(pdf_name, pdf_content, 'application/pdf')
    message.send()
