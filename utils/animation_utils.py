"""
Animation Utilities for PyQt5
Provides smooth animations for dashboard elements
"""
from PyQt5.QtCore import (
    QPropertyAnimation, QEasingCurve, QTimer, QSequentialAnimationGroup,
    QParallelAnimationGroup, pyqtProperty, QObject, Qt, QPoint, QRect
)
from PyQt5.QtWidgets import QGraphicsOpacityEffect, QWidget, QLabel
from PyQt5.QtGui import QColor


class AnimatedCounter(QObject):
    """Animates a number counting up/down smoothly"""
    
    def __init__(self, label: QLabel, duration: int = 1000, parent=None):
        super().__init__(parent)
        self.label = label
        self.duration = duration
        self._value = 0
        self._target = 0
        self._prefix = ""
        self._suffix = ""
        self._decimals = 0
        
        self.timer = QTimer(self)
        self.timer.setInterval(16)  # ~60 FPS
        self.timer.timeout.connect(self._update_value)
        
        self._step = 0
        self._frames = self.duration // 16
    
    def animate_to(self, target: float, prefix: str = "", suffix: str = "", decimals: int = 0):
        """Start animation to target value"""
        self._target = target
        self._prefix = prefix
        self._suffix = suffix
        self._decimals = decimals
        self._value = 0
        self._step = target / max(self._frames, 1)
        self.timer.start()
    
    def _update_value(self):
        """Update the displayed value"""
        if self._value < self._target:
            self._value = min(self._value + self._step, self._target)
            if self._decimals > 0:
                text = f"{self._prefix}{self._value:.{self._decimals}f}{self._suffix}"
            else:
                text = f"{self._prefix}{int(self._value):,}{self._suffix}"
            self.label.setText(text)
        else:
            self.timer.stop()
            if self._decimals > 0:
                text = f"{self._prefix}{self._target:.{self._decimals}f}{self._suffix}"
            else:
                text = f"{self._prefix}{int(self._target):,}{self._suffix}"
            self.label.setText(text)


class FadeInEffect:
    """Provides fade-in animation for widgets"""
    
    @staticmethod
    def apply(widget: QWidget, duration: int = 500, delay: int = 0):
        """Apply fade-in animation to a widget"""
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        effect.setOpacity(0)
        
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        
        if delay > 0:
            QTimer.singleShot(delay, animation.start)
        else:
            animation.start()
        
        # Keep reference to prevent garbage collection
        widget._fade_animation = animation
        widget._fade_effect = effect
        
        return animation


class SlideInEffect:
    """Provides slide-in animation for widgets"""
    
    @staticmethod
    def apply(widget: QWidget, direction: str = "up", duration: int = 400, delay: int = 0):
        """Apply slide-in animation from specified direction"""
        original_pos = widget.pos()
        
        # Calculate start position based on direction
        offset = 50
        if direction == "up":
            start_pos = QPoint(original_pos.x(), original_pos.y() + offset)
        elif direction == "down":
            start_pos = QPoint(original_pos.x(), original_pos.y() - offset)
        elif direction == "left":
            start_pos = QPoint(original_pos.x() + offset, original_pos.y())
        else:  # right
            start_pos = QPoint(original_pos.x() - offset, original_pos.y())
        
        widget.move(start_pos)
        
        animation = QPropertyAnimation(widget, b"pos")
        animation.setDuration(duration)
        animation.setStartValue(start_pos)
        animation.setEndValue(original_pos)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # Combine with fade
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        effect.setOpacity(0)
        
        fade_anim = QPropertyAnimation(effect, b"opacity")
        fade_anim.setDuration(duration)
        fade_anim.setStartValue(0.0)
        fade_anim.setEndValue(1.0)
        fade_anim.setEasingCurve(QEasingCurve.OutCubic)
        
        group = QParallelAnimationGroup(widget)
        group.addAnimation(animation)
        group.addAnimation(fade_anim)
        
        if delay > 0:
            QTimer.singleShot(delay, group.start)
        else:
            group.start()
        
        widget._slide_animation = group
        widget._slide_effect = effect
        
        return group


class PulseEffect:
    """Creates a pulsing glow effect"""
    
    @staticmethod
    def apply(widget: QWidget, color: str = "#34C759", duration: int = 1500):
        """Apply continuous pulse animation"""
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(1.0)
        animation.setKeyValueAt(0.5, 0.5)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.InOutSine)
        animation.setLoopCount(-1)  # Infinite loop
        animation.start()
        
        widget._pulse_animation = animation
        widget._pulse_effect = effect
        
        return animation


class HoverScaleEffect:
    """Provides scale effect on hover with stylesheet"""
    
    @staticmethod
    def get_hover_style(base_bg: str = "white", hover_transform: bool = True) -> str:
        """Returns CSS with hover effect"""
        return f"""
            QFrame {{
                background-color: {base_bg};
                border-radius: 16px;
                border: none;
            }}
            QFrame:hover {{
                background-color: {base_bg};
                border: 1px solid rgba(26, 115, 232, 0.3);
            }}
        """


class AnimationManager:
    """Manages multiple animations for a dashboard"""
    
    def __init__(self):
        self.counters = []
        self.animations = []
    
    def create_counter(self, label: QLabel, duration: int = 1000) -> AnimatedCounter:
        """Create and track an animated counter"""
        counter = AnimatedCounter(label, duration)
        self.counters.append(counter)
        return counter
    
    def fade_in_staggered(self, widgets: list, base_delay: int = 100, duration: int = 500):
        """Apply staggered fade-in to a list of widgets"""
        for i, widget in enumerate(widgets):
            delay = i * base_delay
            anim = FadeInEffect.apply(widget, duration, delay)
            self.animations.append(anim)
    
    def slide_in_staggered(self, widgets: list, direction: str = "up", 
                           base_delay: int = 100, duration: int = 400):
        """Apply staggered slide-in to a list of widgets"""
        for i, widget in enumerate(widgets):
            delay = i * base_delay
            anim = SlideInEffect.apply(widget, direction, duration, delay)
            self.animations.append(anim)
    
    def stop_all(self):
        """Stop all managed animations"""
        for anim in self.animations:
            if hasattr(anim, 'stop'):
                anim.stop()
        for counter in self.counters:
            counter.timer.stop()


# Glassmorphism style helper
def get_glassmorphism_style(blur_amount: int = 10, opacity: float = 0.85, 
                            border_radius: int = 16) -> str:
    """Returns CSS for glassmorphism effect"""
    return f"""
        QFrame {{
            background-color: rgba(255, 255, 255, {opacity});
            border-radius: {border_radius}px;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }}
    """


def get_gradient_button_style(color1: str, color2: str, text_color: str = "white") -> str:
    """Returns CSS for gradient button"""
    return f"""
        QPushButton {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {color1}, stop:1 {color2});
            color: {text_color};
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 600;
            font-size: 14px;
        }}
        QPushButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {color2}, stop:1 {color1});
        }}
        QPushButton:pressed {{
            background: {color1};
        }}
    """


def get_card_shadow_style(color: str = "#1A73E8") -> str:
    """Returns CSS for modern card with accent"""
    return f"""
        QFrame {{
            background-color: white;
            border-radius: 16px;
            border: none;
            border-left: 4px solid {color};
        }}
        QFrame:hover {{
            border: 1px solid rgba(26, 115, 232, 0.2);
            border-left: 4px solid {color};
        }}
    """
