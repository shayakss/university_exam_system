"""
PDF Generator - Creates professional marksheets
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from datetime import datetime
import config
import os


class PDFGenerator:
    """Generates PDF marksheets"""
    
    # Class-level font registration (only done once)
    _fonts_registered = False
    _fonts_available = False
    
    def __init__(self):
        self._register_fonts()
        self.watermark_logo_path = None

    @classmethod
    def _register_fonts(cls):
        """Register custom fonts from Windows Fonts directory (cached at class level)"""
        if cls._fonts_registered:
            return
        
        cls._fonts_registered = True
        try:
            font_dir = r"C:\Windows\Fonts"
            # Bookman Old Style
            if os.path.exists(os.path.join(font_dir, 'BOOKOS.TTF')):
                pdfmetrics.registerFont(TTFont('Bookman', os.path.join(font_dir, 'BOOKOS.TTF')))
                pdfmetrics.registerFont(TTFont('Bookman-Italic', os.path.join(font_dir, 'BOOKOSI.TTF')))
            
            # Goudy Old Style
            if os.path.exists(os.path.join(font_dir, 'GOUDOSB.TTF')):
                pdfmetrics.registerFont(TTFont('Goudy-Bold', os.path.join(font_dir, 'GOUDOSB.TTF')))
            
            # Times New Roman
            if os.path.exists(os.path.join(font_dir, 'times.ttf')):
                pdfmetrics.registerFont(TTFont('TimesNewRoman', os.path.join(font_dir, 'times.ttf')))
                pdfmetrics.registerFont(TTFont('TimesNewRoman-Bold', os.path.join(font_dir, 'timesbd.ttf')))
                
            cls._fonts_available = True
        except Exception as e:
            print(f"Warning: Could not register fonts: {e}")
    
    @property
    def fonts_registered(self):
        """Check if fonts are available"""
        return PDFGenerator._fonts_available
    
    def generate_marksheet(self, result_data: dict, output_path: str, university_data: dict = None) -> bool:
        """
        Generate a professional marksheet PDF
        
        Args:
            result_data: Dictionary containing student and result information
            output_path: Path where PDF should be saved
            university_data: Optional dict with university details (name, address, phone, email, website)
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create PDF document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=0.75*inch,
                leftMargin=0.75*inch,
                topMargin=0.75*inch,
                bottomMargin=0.75*inch
            )
            
            # Container for PDF elements
            elements = []
            styles = getSampleStyleSheet()
            
            # Get university name from custom data or config
            university_name = university_data.get('name', config.UNIVERSITY_NAME) if university_data else config.UNIVERSITY_NAME
            
            # University header
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#2C3E50'),
                spaceAfter=6,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )
            
            university_title = Paragraph(university_name, title_style)
            elements.append(university_title)
            
            # Add university contact info if provided
            if university_data:
                contact_parts = []
                if university_data.get('address'):
                    contact_parts.append(university_data['address'])
                if university_data.get('phone'):
                    contact_parts.append(f"Phone: {university_data['phone']}")
                if university_data.get('email'):
                    contact_parts.append(f"Email: {university_data['email']}")
                if university_data.get('website'):
                    contact_parts.append(university_data['website'])
                
                if contact_parts:
                    contact_style = ParagraphStyle(
                        'Contact',
                        parent=styles['Normal'],
                        fontSize=9,
                        textColor=colors.HexColor('#7F8C8D'),
                        alignment=TA_CENTER,
                        spaceAfter=12
                    )
                    contact_text = " | ".join(contact_parts)
                    contact = Paragraph(contact_text, contact_style)
                    elements.append(contact)
            
            # Subtitle
            subtitle_style = ParagraphStyle(
                'Subtitle',
                parent=styles['Normal'],
                fontSize=12,
                textColor=colors.HexColor('#7F8C8D'),
                alignment=TA_CENTER,
                spaceAfter=20
            )
            
            subtitle = Paragraph("Academic Transcript / Marksheet", subtitle_style)
            elements.append(subtitle)
            elements.append(Spacer(1, 0.3*inch))
            
            # Student information
            student = result_data['student']
            student_info = [
                ['Roll Number:', student['roll_number'], 'Name:', student['name']],
                ['Department:', student['department_name'], 'Semester:', str(result_data['semester'])],
                ['Date of Birth:', student.get('date_of_birth', 'N/A'), 'Gender:', student.get('gender', 'N/A')]
            ]
            
            student_table = Table(student_info, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
            student_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2C3E50')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            
            elements.append(student_table)
            elements.append(Spacer(1, 0.3*inch))
            
            # Marks table
            marks_data = [['S.No', 'Course Code', 'Course Name', 'Max Marks', 'Marks Obtained', 'Grade', 'Status']]
            
            for idx, mark in enumerate(result_data['marks'], 1):
                marks_data.append([
                    str(idx),
                    mark['course_code'],
                    mark['course_name'],
                    str(mark['max_marks']),
                    str(mark['marks_obtained']),
                    mark['grade'],
                    mark['status']
                ])
            
            # Total row
            marks_data.append([
                '', '', 'TOTAL',
                str(result_data['total_marks']),
                str(result_data['marks_obtained']),
                '', ''
            ])
            
            marks_table = Table(marks_data, colWidths=[0.5*inch, 1*inch, 2.5*inch, 1*inch, 1.2*inch, 0.8*inch, 0.8*inch])
            marks_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -2), 9),
                ('ALIGN', (0, 1), (0, -1), 'CENTER'),
                ('ALIGN', (3, 1), (-1, -1), 'CENTER'),
                ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#ECF0F1')),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, -1), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7')),
                ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#2C3E50')),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            
            elements.append(marks_table)
            elements.append(Spacer(1, 0.3*inch))
            
            # Result summary
            result_summary = [
                ['Percentage:', f"{result_data['percentage']}%", 'SGPA:', str(result_data['sgpa'])],
                ['CGPA:', str(result_data['cgpa']), 'Overall Grade:', result_data['overall_grade']],
                ['Result:', result_data['status'], '', '']
            ]
            
            result_table = Table(result_summary, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
            result_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2C3E50')),
                ('BACKGROUND', (0, 2), (1, 2), 
                 colors.HexColor('#27AE60') if result_data['status'] == 'Pass' else colors.HexColor('#E74C3C')),
                ('TEXTCOLOR', (0, 2), (1, 2), colors.whitesmoke),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
            ]))
            
            elements.append(result_table)
            elements.append(Spacer(1, 0.5*inch))
            
            # Signature section
            signature_data = [
                [config.SIGNATURE_PRINCIPAL, '', config.SIGNATURE_CONTROLLER],
                ['Principal', '', 'Controller of Examinations']
            ]
            
            signature_table = Table(signature_data, colWidths=[2.5*inch, 2*inch, 2.5*inch])
            signature_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, 1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
                ('LINEABOVE', (0, 0), (0, 0), 1, colors.black),
                ('LINEABOVE', (2, 0), (2, 0), 1, colors.black),
            ]))
            
            elements.append(signature_table)
            
            # Footer
            elements.append(Spacer(1, 0.3*inch))
            footer_text = f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
            footer = Paragraph(footer_text, styles['Normal'])
            elements.append(footer)
            
            # Build PDF
            doc.build(elements)
            
            print(f"✓ PDF marksheet generated: {output_path}")
            return True
        
        except Exception as e:
            print(f"✗ PDF generation error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _draw_watermark(self, canvas_obj, doc):
        """Draw watermark logo on page"""
        if not self.watermark_logo_path or not os.path.exists(self.watermark_logo_path):
            return
        
        try:
            # Save canvas state
            canvas_obj.saveState()
            
            # Get page dimensions
            page_width, page_height = A4
            
            # Calculate watermark size (140% of original)
            watermark_width = 3 * inch * 1.4  # Original size * 140%
            watermark_height = 3 * inch * 1.4
            
            # Center position
            x = (page_width - watermark_width) / 2
            y = (page_height - watermark_height) / 2
            
            # Set opacity to 15%
            canvas_obj.setFillAlpha(0.15)
            
            # Draw the image
            canvas_obj.drawImage(
                self.watermark_logo_path,
                x, y,
                width=watermark_width,
                height=watermark_height,
                preserveAspectRatio=True,
                mask='auto'
            )
            
            # Restore canvas state
            canvas_obj.restoreState()
        except Exception as e:
            print(f"Warning: Could not draw watermark: {e}")
    
    def generate_transcript(self, student_data: dict, marks_data: list, output_path: str, university_data: dict = None) -> bool:
        """
        Generate academic transcript PDF matching University of Balochistan format
        
        Args:
            student_data: Dict with student info (roll_number, name, father_name, department_name, etc.)
            marks_data: List of dicts with course marks grouped by semester
            output_path: Path where PDF should be saved
            university_data: Optional dict with university details
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=0.5*inch,
                leftMargin=0.5*inch,
                topMargin=0.5*inch,
                bottomMargin=0.5*inch
            )
            
            elements = []
            styles = getSampleStyleSheet()
            
            # Custom styles
            # University Name: Bookman Old Style, 12
            uni_name_font = 'Bookman' if self.fonts_registered else 'Helvetica-Bold'
            uni_name_style = ParagraphStyle(
                'UniName',
                parent=styles['Normal'],
                fontSize=12,
                alignment=TA_CENTER,
                fontName=uni_name_font,
                spaceAfter=2
            )

            # Subtitle: Bookman Old Style, 12, Italic
            subtitle_font = 'Bookman-Italic' if self.fonts_registered else 'Helvetica-Oblique'
            subtitle_style = ParagraphStyle(
                'Subtitle',
                parent=styles['Normal'],
                fontSize=12,
                alignment=TA_CENTER,
                fontName=subtitle_font,
                spaceAfter=6
            )
            
            # Transcript Title: Goudy Old Style, 14, Bold, Double Underline (simulated with <u>)
            title_font = 'Goudy-Bold' if self.fonts_registered else 'Helvetica-Bold'
            title_style = ParagraphStyle(
                'TranscriptTitle',
                parent=styles['Heading1'],
                fontSize=14,
                textColor=colors.black,
                alignment=TA_CENTER,
                spaceAfter=12,
                fontName=title_font
            )
            
            # General Text: Times New Roman
            text_font = 'TimesNewRoman' if self.fonts_registered else 'Times-Roman'
            text_bold_font = 'TimesNewRoman-Bold' if self.fonts_registered else 'Times-Bold'
            
            normal_style = ParagraphStyle(
                'CustomNormal',
                parent=styles['Normal'],
                fontName=text_font,
                fontSize=10
            )
            
            # Semester Heading: Middle of table with underline
            semester_style = ParagraphStyle(
                'SemesterHeading',
                parent=styles['Heading2'],
                fontName=text_bold_font,
                fontSize=12,
                alignment=TA_CENTER,
                spaceAfter=6
            )
            
            # Header
            # Header Table
            # Try final logo first, then new, then old
            from utils.resource_helper import resource_path
            
            logo_path = resource_path(os.path.join('resources', 'images', 'uob_logo_final.png'))
            if not os.path.exists(logo_path):
                 logo_path = resource_path(os.path.join('resources', 'images', 'uob_logo_new.jpg'))
            if not os.path.exists(logo_path):
                 logo_path = resource_path(os.path.join('resources', 'images', 'uob_logo.png'))
            
            logo = None
            if os.path.exists(logo_path):
                logo = Image(logo_path, width=1.2*inch, height=1.2*inch)
            
            # Define university details
            university_name = "UNIVERSITY OF BALOCHISTAN, QUETTA"
            sub_campus = "Kharan"
            
            # Text content for right column
            header_text = []
            header_text.append(Paragraph(university_name, uni_name_style))
            header_text.append(Paragraph(f"Sub-Campus {sub_campus}", subtitle_style))
            header_text.append(Paragraph("Office of the Examination", subtitle_style))
            
            # Create header table
            if logo:
                # Logo on left, text on right
                header_data = [[logo, header_text]]
                # A4 width is ~8.27 inch, margins 0.5 each side -> ~7.27 usable
                col_widths = [1.5*inch, 5.7*inch]
                table_style = [
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('ALIGN', (0, 0), (0, 0), 'LEFT'),   # Logo column
                    ('ALIGN', (1, 0), (1, 0), 'CENTER'), # Text column
                ]
            else:
                # Just text if no logo
                header_data = [[header_text]]
                col_widths = [7.2*inch]
                table_style = [
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'), # Text centered
                ]
            
            # Common padding
            table_style.extend([
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ])

            header_table = Table(header_data, colWidths=col_widths)
            header_table.setStyle(TableStyle(table_style))
            
            elements.append(header_table)
            elements.append(Spacer(1, 0.1*inch))
            
            # Title below header
            elements.append(Paragraph("<u><b>STUDENT TRANSCRIPT</b></u>", title_style))
            elements.append(Spacer(1, 0.2*inch))
            
            # Student Information
            info_data = [
                ['Roll No:', student_data.get('roll_number', ''), 
                 'Session:', student_data.get('session', '2021-2025'), 
                 'Reg. No:', student_data.get('registration_no', '')],
                ['Name:', student_data.get('name', ''), 
                 '', '', 
                 "Father's Name:", student_data.get('father_name', '')]
            ]
            
            info_table = Table(info_data, colWidths=[0.8*inch, 1.8*inch, 0.8*inch, 0.8*inch, 1.1*inch, 1.8*inch])
            info_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), text_font),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('FONTNAME', (0, 0), (0, -1), text_bold_font),
                ('FONTNAME', (2, 0), (2, -1), text_bold_font),
                ('FONTNAME', (4, 0), (4, -1), text_bold_font),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            
            elements.append(info_table)
            
            # Department
            dept_text = f"<b>Department:</b> {student_data.get('department_name', '')} (Morning)"
            elements.append(Paragraph(dept_text, normal_style))
            elements.append(Spacer(1, 0.15*inch))
            
            # Group marks by semester
            semesters = {}
            for mark in marks_data:
                sem = mark.get('semester', 1)
                if sem not in semesters:
                    semesters[sem] = []
                semesters[sem].append(mark)
            
            # Create table for each semester
            for semester in sorted(semesters.keys()):
                # Semester heading
                ordinal = self._get_ordinal(semester)
                sem_heading = Paragraph(f"<u>{ordinal} Semester</u>", semester_style)
                elements.append(sem_heading)
                elements.append(Spacer(1, 0.1*inch))
                
                # Table data
                table_data = [
                    ['S/N', 'COURSE NAME', 'CREDIT HOURS', 'TOTAL MARKS', 'OBTAINED MARKS', 'GRADE POINT']
                ]
                
                total_credits = 0
                total_marks = 0
                obtained_marks = 0
                
                for idx, course in enumerate(semesters[semester], 1):
                    credits = course.get('credits', 3)
                    total = course.get('total_marks', 100)
                    obtained = course.get('obtained_marks', 0)
                    grade = self._calculate_grade_point(obtained, total)
                    
                    total_credits += credits
                    total_marks += total
                    obtained_marks += obtained
                    
                    table_data.append([
                        str(idx),
                        course.get('course_name', ''),
                        str(credits),
                        str(total),
                        str(obtained),
                        f"{grade:.2f}"
                    ])
                
                # Fill empty rows to make 6 total
                while len(table_data) < 7:
                    table_data.append(['', '', '', '', '', ''])
                
                # Totals
                gpa = self._calculate_gpa(semesters[semester])
                table_data.append([
                    '', 'Total/GPA', 
                    str(total_credits), 
                    str(total_marks), 
                    str(obtained_marks), 
                    f"{gpa:.2f}"
                ])
                
                # Create table
                table = Table(table_data, colWidths=[0.4*inch, 2.8*inch, 0.9*inch, 0.9*inch, 1.1*inch, 0.9*inch])
                table.setStyle(TableStyle([
                    # Header
                    ('FONTNAME', (0, 0), (-1, 0), text_bold_font),
                    ('FONTSIZE', (0, 0), (-1, 0), 8),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('BOX', (0, 0), (-1, 0), 1, colors.black),
                    ('INNERGRID', (0, 0), (-1, 0), 0.5, colors.black),
                    # Data
                    ('FONTNAME', (0, 1), (-1, -2), text_font),
                    ('FONTSIZE', (0, 1), (-1, -2), 9),
                    ('ALIGN', (0, 1), (0, -2), 'CENTER'),
                    ('ALIGN', (2, 1), (-1, -2), 'CENTER'),
                    ('BOX', (0, 1), (-1, -2), 1, colors.black),
                    ('INNERGRID', (0, 1), (-1, -2), 0.5, colors.black),
                    # Totals
                    ('FONTNAME', (0, -1), (-1, -1), text_bold_font),
                    ('FONTSIZE', (0, -1), (-1, -1), 9),
                    ('ALIGN', (1, -1), (-1, -1), 'CENTER'),
                    ('BOX', (0, -1), (-1, -1), 1, colors.black),
                    ('INNERGRID', (0, -1), (-1, -1), 0.5, colors.black),
                ]))
                
                elements.append(table)
                elements.append(Spacer(1, 0.2*inch))
            
            # Add signature section at the end
            elements.append(Spacer(1, 0.5*inch))
            
            # Signature style - Times New Roman, size 11, right-aligned
            from reportlab.lib.enums import TA_RIGHT
            
            signature_style = ParagraphStyle(
                'Signature',
                parent=styles['Normal'],
                fontName=text_bold_font,
                fontSize=11,
                alignment=TA_RIGHT
            )
            
            signature_detail_style = ParagraphStyle(
                'SignatureDetail',
                parent=styles['Normal'],
                fontName=text_font,
                fontSize=11,
                alignment=TA_RIGHT
            )
            
            # Add signature text
            elements.append(Paragraph("<b>Assistant Director Examination</b>", signature_style))
            elements.append(Paragraph("University of Balochistan", signature_detail_style))
            elements.append(Paragraph("Sub Campus Kharan", signature_detail_style))
            
            # Set watermark logo path
            logo_path = resource_path(os.path.join('resources', 'images', 'uob_logo_final.png'))
            if not os.path.exists(logo_path):
                 logo_path = resource_path(os.path.join('resources', 'images', 'uob_logo_new.jpg'))
            if not os.path.exists(logo_path):
                 logo_path = resource_path(os.path.join('resources', 'images', 'uob_logo.png'))
            
            if os.path.exists(logo_path):
                self.watermark_logo_path = logo_path
            
            # Build PDF with watermark
            doc.build(elements, onFirstPage=self._draw_watermark, onLaterPages=self._draw_watermark)
            print(f"✓ Transcript generated: {output_path}")
            return True
            
        except Exception as e:
            print(f"✗ Transcript generation error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _get_ordinal(self, n):
        """Convert number to ordinal (1st, 2nd, 3rd, etc.)"""
        if 10 <= n % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
        return f"{n}{suffix}"
    
    def _calculate_grade_point(self, obtained, total):
        """Calculate grade point based on percentage"""
        if total == 0:
            return 0.0
        percentage = (obtained / total) * 100
        if percentage >= 85: return 4.0
        elif percentage >= 80: return 3.7
        elif percentage >= 75: return 3.3
        elif percentage >= 70: return 3.0
        elif percentage >= 65: return 2.7
        elif percentage >= 60: return 2.3
        elif percentage >= 55: return 2.0
        elif percentage >= 50: return 1.7
        else: return 0.0
    
    def _calculate_gpa(self, courses):
        """Calculate GPA for semester"""
        if not courses:
            return 0.0
        total_points = 0
        total_credits = 0
        for course in courses:
            credits = course.get('credits', 3)
            total = course.get('total_marks', 100)
            obtained = course.get('obtained_marks', 0)
            grade_point = self._calculate_grade_point(obtained, total)
            total_points += grade_point * credits
            total_credits += credits
        return total_points / total_credits if total_credits > 0 else 0.0


# Global PDF generator instance
pdf_generator = PDFGenerator()
