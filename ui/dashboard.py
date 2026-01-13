"""
Modern Animated Dashboard - With Animations, Glassmorphism, and Interactive Features
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QPainter, QColor, QPen, QLinearGradient
from controllers.student_controller import student_controller
from controllers.department_controller import department_controller
from controllers.course_controller import course_controller
from controllers.user_controller import user_controller
from controllers.attendance_controller import attendance_controller
from datetime import datetime, date, timedelta
from utils.animation_utils import (
    AnimatedCounter, FadeInEffect, SlideInEffect, PulseEffect,
    AnimationManager, get_glassmorphism_style, get_gradient_button_style,
    get_card_shadow_style
)


class ModernAnimatedDashboard(QWidget):
    """Modern Dashboard with animations and enhanced visuals"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #0F172A;")  # Dark modern background
        self.animation_manager = AnimationManager()
        self.counters = {}
        self.init_ui()
        
        # Delay loading to allow animations to be visible
        QTimer.singleShot(300, self.load_statistics)
        QTimer.singleShot(100, self.start_entrance_animations)
    
    def init_ui(self):
        """Initialize UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 1. Top Bar (Header)
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Scrollable content area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("""
            QScrollArea { 
                background-color: #0F172A; 
                border: none; 
            }
            QScrollBar:vertical {
                background-color: #1E293B;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: #475569;
                border-radius: 4px;
                min-height: 40px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #64748B;
            }
        """)
        
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #0F172A;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(25)
        
        # 2. Welcome message
        self.welcome_label = self.create_welcome_message()
        content_layout.addWidget(self.welcome_label)
        
        # 3. Stats Overview Row (4 Animated Cards)
        stats_row = self.create_stats_row()
        content_layout.addWidget(stats_row)
        
        # 4. Quick Actions Card
        quick_actions = self.create_quick_actions()
        content_layout.addWidget(quick_actions)
        
        # 5. Charts and Activity Row
        charts_activity_layout = QHBoxLayout()
        charts_activity_layout.setSpacing(20)
        
        # Charts section (left)
        charts_card = self.create_charts_section()
        charts_activity_layout.addWidget(charts_card, 6)
        
        # Activity Timeline (right)
        activity_card = self.create_activity_timeline()
        charts_activity_layout.addWidget(activity_card, 4)
        
        content_layout.addLayout(charts_activity_layout)
        
        # 6. Summary Cards Row
        summary_row = self.create_summary_row()
        content_layout.addWidget(summary_row)
        
        # 7. System Status
        system_status = self.create_system_status()
        content_layout.addWidget(system_status)
        
        content_layout.addStretch()
        
        # 8. Footer
        footer = self.create_footer()
        content_layout.addWidget(footer)
        
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
        
        # Store animatable widgets for entrance animations
        self.animatable_cards = [
            self.students_card, self.courses_card, 
            self.departments_card, self.users_card,
            self.male_students_card, self.female_students_card,
            self.active_students_outer_card, self.attendance_rate_card
        ]
    
    def create_header(self):
        """Create top bar header with gradient and clock"""
        header = QFrame()
        header.setFixedHeight(80)
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #6366F1, stop:0.5 #8B5CF6, stop:1 #EC4899);
                border: none;
            }
        """)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(30, 0, 30, 0)
        
        # Logo + Title
        title_layout = QHBoxLayout()
        logo = QLabel("\U0001F393")  # Graduation cap emoji
        logo.setStyleSheet("font-size: 36px; background: transparent; border: none;")
        title_layout.addWidget(logo)
        
        title = QLabel("Dashboard")
        title.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
            color: white;
            background: transparent;
            border: none;
            letter-spacing: 1px;
        """)
        title_layout.addWidget(title)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        
        # Real-time Clock
        self.clock_label = QLabel()
        self.clock_label.setStyleSheet("""
            font-size: 16px;
            color: rgba(255, 255, 255, 0.9);
            background: rgba(255, 255, 255, 0.1);
            border: none;
            border-radius: 12px;
            padding: 8px 16px;
            font-weight: 500;
        """)
        layout.addWidget(self.clock_label)
        
        # Update clock every second
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)
        self.update_clock()
        
        # Notification Bell
        notif_btn = QPushButton("\U0001F514")  # Bell emoji
        notif_btn.setFixedSize(44, 44)
        notif_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.15);
                color: white;
                border: none;
                border-radius: 22px;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.25);
            }
        """)
        layout.addWidget(notif_btn)
        
        # User Avatar
        user_btn = QPushButton("\U0001F464 Admin")  # Bust emoji
        user_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.15);
                color: white;
                border: none;
                border-radius: 22px;
                padding: 10px 24px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.25);
            }
        """)
        layout.addWidget(user_btn)
        
        return header
    
    def update_clock(self):
        """Update the clock display"""
        now = datetime.now()
        # Format time without emojis to avoid encoding issues
        time_str = now.strftime("%I:%M:%S %p")
        date_str = now.strftime("%b %d, %Y")
        self.clock_label.setText(f"\U0001F551 {time_str}  |  \U0001F4C5 {date_str}")
    
    def create_welcome_message(self):
        """Create personalized welcome message based on time"""
        hour = datetime.now().hour
        if hour < 12:
            greeting = "Good Morning"
            emoji = "\U0001F305"  # Sunrise
        elif hour < 17:
            greeting = "Good Afternoon"
            emoji = "\u2600\uFE0F"  # Sun
        else:
            greeting = "Good Evening"
            emoji = "\U0001F319"  # Crescent moon
        
        welcome = QLabel(f"{emoji} {greeting}, Administrator!")
        welcome.setStyleSheet("""
            font-size: 28px;
            font-weight: 600;
            color: #F1F5F9;
            background: transparent;
            border: none;
            margin-bottom: 10px;
        """)
        return welcome
    
    def create_stats_row(self):
        """Create stats overview row with animated cards"""
        container = QFrame()
        container.setStyleSheet("background: transparent; border: none;")
        layout = QHBoxLayout(container)
        layout.setSpacing(20)
        
        # Create 4 stat cards with different gradients
        self.students_card = self.create_animated_stat_card(
            "\U0001F465", "0", "Total Students",  # Busts emoji
            ["#6366F1", "#8B5CF6"], "#EEF2FF"
        )
        self.courses_card = self.create_animated_stat_card(
            "\U0001F4DA", "0", "Total Courses",  # Books emoji
            ["#10B981", "#34D399"], "#ECFDF5"
        )
        self.departments_card = self.create_animated_stat_card(
            "\U0001F3DB", "0", "Departments",  # Classical building emoji
            ["#F59E0B", "#FBBF24"], "#FEF3C7"
        )
        self.users_card = self.create_animated_stat_card(
            "\U0001F464", "0", "Active Users",  # Bust emoji
            ["#EC4899", "#F472B6"], "#FCE7F3"
        )
        
        layout.addWidget(self.students_card)
        layout.addWidget(self.courses_card)
        layout.addWidget(self.departments_card)
        layout.addWidget(self.users_card)
        
        return container
    
    def create_animated_stat_card(self, icon, value, title, gradient_colors, icon_bg):
        """Create an animated stat card with glassmorphism"""
        card = QFrame()
        card.setMinimumHeight(220)  # Increased from 160
        card.setMinimumWidth(200)   # Added minimum width
        card.setStyleSheet("""
            QFrame {
                background-color: rgba(30, 41, 59, 0.8);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            QFrame:hover {
                background-color: rgba(30, 41, 59, 0.95);
                border: 1px solid rgba(99, 102, 241, 0.5);
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(28, 28, 28, 28)  # Increased padding
        layout.setSpacing(20)  # Increased spacing
        
        # Top row with icon
        top_row = QHBoxLayout()
        
        # Icon container with gradient background
        icon_container = QFrame()
        icon_container.setFixedSize(65, 65)  # Slightly larger icon
        icon_container.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {gradient_colors[0]}, stop:1 {gradient_colors[1]});
                border-radius: 18px;
                border: none;
            }}
        """)
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        
        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 30px; background: transparent; border: none;")
        icon_layout.addWidget(icon_label)
        
        top_row.addWidget(icon_container)
        top_row.addStretch()
        
        # Trend indicator
        trend = QLabel("\u2191 12%")  # Up arrow
        trend.setStyleSheet("""
            font-size: 13px;
            color: #34D399;
            background: rgba(16, 185, 129, 0.2);
            border: none;
            border-radius: 10px;
            padding: 6px 12px;
            font-weight: 600;
        """)
        top_row.addWidget(trend)
        
        layout.addLayout(top_row)
        
        # Add some spacing
        layout.addSpacing(5)
        
        # Value (animated)
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            font-size: 48px;
            font-weight: bold;
            color: #F1F5F9;
            background: transparent;
            border: none;
        """)
        layout.addWidget(value_label)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 15px;
            color: #94A3B8;
            background: transparent;
            border: none;
            font-weight: 500;
        """)
        layout.addWidget(title_label)
        
        # Store references
        card.value_label = value_label
        card.trend_label = trend
        
        # Create animated counter
        counter = AnimatedCounter(value_label, duration=1200)
        self.counters[title] = counter
        
        return card
    
    def create_quick_actions(self):
        """Create quick actions card with gradient buttons"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: rgba(30, 41, 59, 0.6);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(20)
        
        # Title with icon
        title_row = QHBoxLayout()
        title = QLabel("\u26A1 Quick Actions")  # Lightning bolt
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #F1F5F9;
            background: transparent;
            border: none;
        """)
        title_row.addWidget(title)
        title_row.addStretch()
        layout.addLayout(title_row)
        
        # Buttons row
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(16)
        
        # Define buttons with gradients
        buttons_data = [
            ("\u2795 Add Student", "#10B981", "#34D399"),  # Plus sign
            ("\u2795 Add Course", "#6366F1", "#8B5CF6"),
            ("\u2795 Add Department", "#F59E0B", "#FBBF24"),
            ("\u2795 Add User", "#EC4899", "#F472B6"),
        ]
        
        for text, color1, color2 in buttons_data:
            btn = QPushButton(text)
            btn.setMinimumHeight(50)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 {color1}, stop:1 {color2});
                    color: white;
                    border: none;
                    border-radius: 12px;
                    font-weight: 600;
                    font-size: 14px;
                    padding: 12px 20px;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 {color2}, stop:1 {color1});
                }}
            """)
            buttons_layout.addWidget(btn)
        
        # Refresh button
        refresh_btn = QPushButton("\U0001F504 Refresh")  # Refresh emoji
        refresh_btn.setMinimumHeight(50)
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.clicked.connect(self.refresh_with_animation)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                color: #F1F5F9;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                font-weight: 600;
                font-size: 14px;
                padding: 12px 20px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.2);
            }
        """)
        buttons_layout.addWidget(refresh_btn)
        
        layout.addLayout(buttons_layout)
        
        return card
    
    def create_charts_section(self):
        """Create charts section with tabs"""
        card = QFrame()
        card.setMinimumHeight(350)
        card.setStyleSheet("""
            QFrame {
                background-color: rgba(30, 41, 59, 0.6);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("\U0001F4CA Analytics Overview")  # Bar chart emoji
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #F1F5F9;
            background: transparent;
            border: none;
        """)
        layout.addWidget(title)
        
        # Chart placeholder with animated bars
        chart_area = QFrame()
        chart_area.setMinimumHeight(250)
        chart_area.setStyleSheet("""
            background: rgba(15, 23, 42, 0.5);
            border-radius: 16px;
            border: 1px dashed rgba(255, 255, 255, 0.2);
        """)
        
        chart_layout = QVBoxLayout(chart_area)
        chart_layout.setAlignment(Qt.AlignCenter)
        
        # Animated progress bars as chart representation
        self.chart_bars = []
        bars_layout = QHBoxLayout()
        bars_layout.setSpacing(20)
        bars_layout.setAlignment(Qt.AlignBottom)
        
        departments = ["CS", "ECE", "ME", "CE", "EE"]
        colors = ["#6366F1", "#10B981", "#F59E0B", "#EC4899", "#8B5CF6"]
        heights = [85, 65, 75, 55, 70]
        
        for i, (dept, color, height) in enumerate(zip(departments, colors, heights)):
            bar_container = QVBoxLayout()
            
            # Bar
            bar = QFrame()
            bar.setFixedWidth(50)
            bar.setFixedHeight(0)  # Start at 0 for animation
            bar.setStyleSheet(f"""
                background: qlineargradient(x1:0, y1:1, x2:0, y2:0,
                    stop:0 {color}, stop:1 {color}aa);
                border-radius: 8px;
                border: none;
            """)
            bar._target_height = int(height * 2)
            self.chart_bars.append(bar)
            
            # Label
            label = QLabel(dept)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("""
                color: #94A3B8;
                font-size: 12px;
                font-weight: 600;
                background: transparent;
                border: none;
            """)
            
            bar_container.addWidget(bar, alignment=Qt.AlignHCenter)
            bar_container.addWidget(label)
            bars_layout.addLayout(bar_container)
        
        chart_layout.addStretch()
        chart_layout.addLayout(bars_layout)
        
        layout.addWidget(chart_area)
        
        return card
    
    def create_activity_timeline(self):
        """Create recent activity timeline"""
        card = QFrame()
        card.setMinimumHeight(350)
        card.setStyleSheet("""
            QFrame {
                background-color: rgba(30, 41, 59, 0.6);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(16)
        
        # Title
        title = QLabel("\U0001F551 Recent Activity")  # Clock emoji
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #F1F5F9;
            background: transparent;
            border: none;
        """)
        layout.addWidget(title)
        
        # Activity items
        activities = [
            ("\U0001F393", "New student enrolled", "2 min ago", "#6366F1"),  # Graduation cap
            ("\U0001F4DD", "Marks updated for CS101", "15 min ago", "#10B981"),  # Memo
            ("\U0001F464", "User login: admin", "32 min ago", "#F59E0B"),  # Bust
            ("\U0001F4CA", "Attendance marked", "1 hour ago", "#EC4899"),  # Chart
            ("\U0001F527", "System backup completed", "2 hours ago", "#8B5CF6"),  # Wrench
        ]
        
        for icon, text, time, color in activities:
            item = self.create_activity_item(icon, text, time, color)
            layout.addWidget(item)
        
        layout.addStretch()
        
        # View all link
        view_all = QPushButton("View All Activity \u2192")  # Arrow
        view_all.setCursor(Qt.PointingHandCursor)
        view_all.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #6366F1;
                border: none;
                font-weight: 600;
                font-size: 14px;
                text-align: left;
                padding: 8px 0;
            }
            QPushButton:hover {
                color: #8B5CF6;
            }
        """)
        layout.addWidget(view_all)
        
        return card
    
    def create_activity_item(self, icon, text, time, color):
        """Create a single activity item"""
        item = QFrame()
        item.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 12px;
                border: none;
            }
            QFrame:hover {
                background: rgba(255, 255, 255, 0.1);
            }
        """)
        
        layout = QHBoxLayout(item)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(14)
        
        # Icon
        icon_label = QLabel(icon)
        icon_label.setFixedSize(36, 36)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet(f"""
            font-size: 18px;
            background: {color}33;
            border-radius: 10px;
            border: none;
        """)
        layout.addWidget(icon_label)
        
        # Text
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        
        main_text = QLabel(text)
        main_text.setStyleSheet("""
            color: #F1F5F9;
            font-size: 13px;
            font-weight: 500;
            background: transparent;
            border: none;
        """)
        text_layout.addWidget(main_text)
        
        time_text = QLabel(time)
        time_text.setStyleSheet("""
            color: #64748B;
            font-size: 11px;
            background: transparent;
            border: none;
        """)
        text_layout.addWidget(time_text)
        
        layout.addLayout(text_layout)
        layout.addStretch()
        
        return item
    
    def create_summary_row(self):
        """Create summary cards row with gender and active stats"""
        container = QFrame()
        container.setStyleSheet("background: transparent; border: none;")
        layout = QHBoxLayout(container)
        layout.setSpacing(20)
        
        # Gender and Active cards using the animated premium style
        self.male_students_card = self.create_animated_stat_card(
            "\U0001F468", "0", "Male Students",  # Man emoji
            ["#3B82F6", "#2563EB"], "#DBEAFE"
        )
        self.female_students_card = self.create_animated_stat_card(
            "\U0001F469", "0", "Female Students",  # Woman emoji
            ["#F472B6", "#DB2777"], "#FCE7F3"
        )
        self.active_students_outer_card = self.create_animated_stat_card(
            "\u2705", "0", "Active Students",  # Check mark
            ["#10B981", "#059669"], "#D1FAE5"
        )
        self.attendance_rate_card = self.create_animated_stat_card(
            "\U0001F4C8", "0%", "Attendance Rate",  # Chart increasing
            ["#6366F1", "#4F46E5"], "#E0E7FF"
        )
        
        layout.addWidget(self.male_students_card)
        layout.addWidget(self.female_students_card)
        layout.addWidget(self.active_students_outer_card)
        layout.addWidget(self.attendance_rate_card)
        
        return container
    
    # Removed old create_summary_card in favor of uniform animated cards
    
    def create_system_status(self):
        """Create system status with animated indicator"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(16, 185, 129, 0.2), stop:1 rgba(52, 211, 153, 0.1));
                border-radius: 20px;
                border: 1px solid rgba(16, 185, 129, 0.3);
            }
        """)
        
        layout = QHBoxLayout(card)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(20)
        
        # Animated status indicator
        status_indicator = QFrame()
        status_indicator.setFixedSize(16, 16)
        status_indicator.setStyleSheet("""
            background-color: #10B981;
            border-radius: 8px;
            border: none;
        """)
        # Apply pulse animation
        PulseEffect.apply(status_indicator)
        layout.addWidget(status_indicator)
        
        # Status text
        status_layout = QVBoxLayout()
        status_layout.setSpacing(4)
        
        status_title = QLabel("\U0001F7E2 System Status: All Systems Operational")  # Green circle
        status_title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #10B981;
            background: transparent;
            border: none;
        """)
        status_layout.addWidget(status_title)
        
        self.status_info = QLabel("Loading system information...")
        self.status_info.setStyleSheet("""
            font-size: 13px;
            color: #94A3B8;
            background: transparent;
            border: none;
        """)
        status_layout.addWidget(self.status_info)
        
        layout.addLayout(status_layout)
        layout.addStretch()
        
        # Last updated
        now = datetime.now()
        updated = QLabel("Last updated: " + now.strftime("%I:%M %p"))
        updated.setStyleSheet("""
            font-size: 12px;
            color: #64748B;
            background: transparent;
            border: none;
        """)
        layout.addWidget(updated)
        
        return card
    
    def create_footer(self):
        """Create footer"""
        footer = QLabel("\u00A9 2025 University Exam System Built by Shayak Siraj")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("""
            font-size: 12px;
            color: #64748B;
            background: transparent;
            border: none;
            padding: 20px;
        """)
        return footer
    
    def start_entrance_animations(self):
        """Start entrance animations for cards"""
        # Animate stat cards with stagger
        for i, card in enumerate(self.animatable_cards):
            FadeInEffect.apply(card, duration=600, delay=i * 100)
        
        # Animate chart bars
        QTimer.singleShot(500, self.animate_chart_bars)
    
    def animate_chart_bars(self):
        """Animate chart bars growing"""
        for i, bar in enumerate(self.chart_bars):
            target_height = bar._target_height
            QTimer.singleShot(i * 100, lambda b=bar, h=target_height: self.grow_bar(b, h))
    
    def grow_bar(self, bar, target_height):
        """Grow a single bar with animation"""
        animation = QPropertyAnimation(bar, b"minimumHeight")
        animation.setDuration(800)
        animation.setStartValue(0)
        animation.setEndValue(target_height)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        animation.start()
        bar._grow_animation = animation
    
    def refresh_with_animation(self):
        """Refresh with animation effect"""
        # Flash effect before refresh
        for card in self.animatable_cards:
            FadeInEffect.apply(card, duration=400)
        
        QTimer.singleShot(100, self.load_statistics)
    
    def load_statistics(self):
        """Load and display statistics with animations"""
        try:
            # Get counts
            students = student_controller.get_all_students()
            departments = department_controller.get_all_departments()
            courses = course_controller.get_all_courses()
            users = user_controller.get_all_users()
            
            # Get today's attendance
            today = date.today()
            attendance_stats = attendance_controller.get_attendance_statistics(today, today)
            attendance_percentage = attendance_stats.get('average_percentage', 0) if attendance_stats else 0
            
            # Animate counters for main stats
            if "Total Students" in self.counters:
                self.counters["Total Students"].animate_to(len(students))
            if "Total Courses" in self.counters:
                self.counters["Total Courses"].animate_to(len(courses))
            if "Departments" in self.counters:
                self.counters["Departments"].animate_to(len(departments))
            if "Active Users" in self.counters:
                self.counters["Active Users"].animate_to(len(users))
            
            # Update summary cards (Gender, Active, Attendance)
            active_students = sum(1 for s in students if s.get('is_active', 1))
            male_students = sum(1 for s in students if str(s.get('gender', '')).lower() == 'male')
            female_students = sum(1 for s in students if str(s.get('gender', '')).lower() == 'female')
            
            if "Male Students" in self.counters:
                self.counters["Male Students"].animate_to(male_students)
            if "Female Students" in self.counters:
                self.counters["Female Students"].animate_to(female_students)
            if "Active Students" in self.counters:
                self.counters["Active Students"].animate_to(active_students)
            
            # Today's attendance doesn't use the simple counter easily (percentage)
            # but we can set it directly
            self.attendance_rate_card.value_label.setText(f"{attendance_percentage:.0f}%")
            
            # Update trend indicators
            import random
            all_animated_cards = self.animatable_cards + [
                self.male_students_card, self.female_students_card, 
                self.active_students_outer_card, self.attendance_rate_card
            ]
            for card in all_animated_cards:
                if hasattr(card, 'trend_label'):
                    card.trend_label.setText(f"\u2191 {random.randint(2, 15)}%")
            
            # Update system status
            active_users = sum(1 for u in users if u.get('is_active', 1))
            status_text = f"M: {male_students} | F: {female_students} | Active: {active_students} | Overall Students: {len(students)}"
            self.status_info.setText(status_text)
            
        except Exception as e:
            self.status_info.setText(f"Error loading statistics: {str(e)}")


# Backward compatibility alias
ModernDashboard = ModernAnimatedDashboard
