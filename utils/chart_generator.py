"""
Chart Generator - Creates visual charts for dashboard analytics
"""
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer


class SafeFigureCanvas(FigureCanvas):
    """A FigureCanvas that handles draw errors gracefully"""
    
    def __init__(self, figure):
        super().__init__(figure)
        self._drawing_enabled = False
    
    def enable_drawing(self):
        """Enable drawing after widget is properly sized"""
        self._drawing_enabled = True
    
    def draw(self):
        """Override draw to catch and handle dimension errors"""
        if not self._drawing_enabled:
            return
        try:
            # Check if we have valid dimensions
            size = self.get_width_height()
            if size[0] > 10 and size[1] > 10:
                super().draw()
        except ValueError:
            pass
        except Exception:
            pass
    
    def _draw_idle(self):
        """Override _draw_idle to prevent automatic draw with zero dimensions"""
        if not self._drawing_enabled:
            return
        try:
            # Check if we have valid dimensions
            size = self.get_width_height()
            if size[0] > 10 and size[1] > 10:
                super()._draw_idle()
        except Exception:
            # Catch everything to prevent console flood
            pass

    def draw_idle(self):
        """Standard draw_idle override"""
        if self._drawing_enabled:
            self._draw_idle()



class ChartWidget(QWidget):
    """Widget to display matplotlib charts in PyQt5"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # Set minimum size to prevent zero dimension errors
        self.setMinimumSize(200, 150)
        
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.canvas = SafeFigureCanvas(self.figure)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)
        
        # Enable drawing after a delay to ensure widget is sized
        QTimer.singleShot(1000, self._enable_canvas)
    
    def _enable_canvas(self):
        """Enable canvas drawing after delay"""
        self.canvas.enable_drawing()
    
    def showEvent(self, event):
        """Called when widget is shown"""
        super().showEvent(event)
        # Enable drawing slightly after show
        QTimer.singleShot(500, self._enable_canvas)
    
    def clear(self):
        """Clear the figure"""
        self.figure.clear()
    
    def draw(self):
        """Redraw the canvas with error handling"""
        try:
            if self.width() > 10 and self.height() > 10:
                self.canvas.enable_drawing()
                self.canvas.draw()
        except ValueError:
            pass
        except Exception as e:
            print(f"Chart draw error: {e}")


class ChartGenerator:
    """Generates various charts for dashboard"""
    
    @staticmethod
    def create_pie_chart(figure, data, labels, title, colors=None):
        """Create a pie chart"""
        ax = figure.add_subplot(111)
        
        if not colors:
            colors = ['#27AE60', '#E74C3C', '#3498DB', '#F39C12', '#9B59B6']
        
        wedges, texts, autotexts = ax.pie(
            data, labels=labels, autopct='%1.1f%%',
            colors=colors, startangle=90
        )
        
        # Make percentage text bold and white
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
        
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        try:
            ax.axis('equal')
        except (ValueError, Exception):
            pass
        
        return figure
    
    @staticmethod
    def create_bar_chart(figure, categories, values, title, xlabel, ylabel, color='#3498DB'):
        """Create a bar chart"""
        ax = figure.add_subplot(111)
        
        bars = ax.bar(categories, values, color=color, alpha=0.8)
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontweight='bold')
        
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel(xlabel, fontsize=11)
        ax.set_ylabel(ylabel, fontsize=11)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Rotate x-axis labels if needed
        if len(categories) > 5:
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        try:
            figure.tight_layout()
        except (ValueError, Exception):
            pass
        return figure
    
    @staticmethod
    def create_horizontal_bar_chart(figure, categories, values, title, xlabel, ylabel):
        """Create a horizontal bar chart"""
        ax = figure.add_subplot(111)
        
        colors = plt.cm.viridis(range(len(categories)))
        bars = ax.barh(categories, values, color=colors, alpha=0.8)
        
        # Add value labels
        for bar in bars:
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2.,
                   f'{width:.2f}',
                   ha='left', va='center', fontweight='bold', fontsize=9)
        
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel(xlabel, fontsize=11)
        ax.set_ylabel(ylabel, fontsize=11)
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        
        try:
            figure.tight_layout()
        except (ValueError, Exception):
            pass
        return figure
    
    @staticmethod
    def create_line_chart(figure, x_data, y_data, title, xlabel, ylabel, label=None):
        """Create a line chart"""
        ax = figure.add_subplot(111)
        
        ax.plot(x_data, y_data, marker='o', linewidth=2, 
               markersize=8, color='#3498DB', label=label)
        
        # Add value labels on points
        for i, (x, y) in enumerate(zip(x_data, y_data)):
            ax.text(x, y, f'{y:.1f}', ha='center', va='bottom', fontsize=9)
        
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel(xlabel, fontsize=11)
        ax.set_ylabel(ylabel, fontsize=11)
        ax.grid(True, alpha=0.3, linestyle='--')
        
        if label:
            ax.legend()
        
        try:
            figure.tight_layout()
        except (ValueError, Exception):
            pass
        return figure
    
    @staticmethod
    def create_multi_bar_chart(figure, categories, data_dict, title, xlabel, ylabel):
        """Create a grouped bar chart with multiple datasets"""
        ax = figure.add_subplot(111)
        
        import numpy as np
        x = np.arange(len(categories))
        width = 0.35
        
        colors = ['#3498DB', '#E74C3C', '#27AE60', '#F39C12']
        
        for i, (label, values) in enumerate(data_dict.items()):
            offset = width * (i - len(data_dict)/2 + 0.5)
            bars = ax.bar(x + offset, values, width, label=label, 
                         color=colors[i % len(colors)], alpha=0.8)
            
            # Add value labels
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom', fontsize=8)
        
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel(xlabel, fontsize=11)
        ax.set_ylabel(ylabel, fontsize=11)
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        ax.legend()
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        try:
            figure.tight_layout()
        except (ValueError, Exception):
            pass
        return figure


# Global chart generator instance
chart_generator = ChartGenerator()
