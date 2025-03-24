from celery import shared_task
from django.core.mail import EmailMessage
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.db.models import Count
from io import BytesIO
from datetime import datetime
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.conf import settings
import os

from .models import Course, Certificate
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def generate_weekly_report():
    # Регистрируем шрифт Arial
    pdfmetrics.registerFont(TTFont('Arial', '/System/Library/Fonts/Supplemental/Arial.ttf'))
    pdfmetrics.registerFont(TTFont('Arial-Bold', '/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
    
    # Создаем буфер для PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Получаем статистику
    total_users = User.objects.count()
    total_courses = Course.objects.count()
    total_certificates = Certificate.objects.count()
    
    # Статистика по курсам
    courses_stats = Course.objects.annotate(
        student_count=Count('students'),
        certificate_count=Count('certificate')
    ).values('title', 'student_count', 'certificate_count')
    
    # Создаем стили с поддержкой русского языка
    styles = getSampleStyleSheet()
    
    # Создаем собственные стили для русского текста
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName='Arial-Bold',
        fontSize=24,
        spaceAfter=30,
        alignment=1  # По центру
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontName='Arial',
        fontSize=12,
        spaceAfter=20
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontName='Arial-Bold',
        fontSize=18,
        spaceAfter=20
    )
    
    # Добавляем заголовок
    elements.append(Paragraph('Еженедельный отчет по платформе', title_style))
    elements.append(Paragraph(f'Дата создания: {datetime.now().strftime("%d.%m.%Y")}', normal_style))
    elements.append(Paragraph(f'Общая статистика:', heading2_style))
    
    # Создаем таблицу общей статистики
    general_data = [
        ['Показатель', 'Значение'],
        ['Всего пользователей', str(total_users)],
        ['Всего курсов', str(total_courses)],
        ['Выдано сертификатов', str(total_certificates)]
    ]
    
    general_table = Table(general_data, colWidths=[300, 200])
    general_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
        ('FONTNAME', (0, 0), (-1, 0), 'Arial-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWHEIGHT', (0, 0), (-1, -1), 30),
    ]))
    elements.append(general_table)
    
    # Добавляем статистику по курсам
    elements.append(Paragraph('Статистика по курсам:', heading2_style))
    
    courses_data = [['Курс', 'Студентов', 'Сертификатов']]
    for course in courses_stats:
        courses_data.append([
            course['title'],
            str(course['student_count']),
            str(course['certificate_count'])
        ])
    
    courses_table = Table(courses_data, colWidths=[300, 100, 100])
    courses_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
        ('FONTNAME', (0, 0), (-1, 0), 'Arial-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWHEIGHT', (0, 0), (-1, -1), 30),
    ]))
    elements.append(courses_table)
    
    # Генерируем PDF
    doc.build(elements)
    
    # Отправляем email
    email = EmailMessage(
        'Еженедельный отчет по платформе',
        'Во вложении находится еженедельный отчет по статистике платформы.',
        'larachka.06@gmail.com',
        ['larachka.06@gmail.com']
    )
    
    # Прикрепляем PDF
    email.attach(f'weekly_report_{datetime.now().strftime("%Y%m%d")}.pdf', 
                buffer.getvalue(), 
                'application/pdf')
    
    # Отправляем email
    email.send()
    
    return "Отчет успешно создан и отправлен" 