import sys
from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsTextItem, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtGui import QPen, QColor, QFont
from PyQt6.QtCore import Qt

class ClickableNode(QGraphicsEllipseItem):
    def __init__(self, label, x, y, parent):
        super().__init__(x - 20, y - 20, 40, 40)
        self.label = label
        self.parent = parent  # Reference to the main window or scene to access methods
        self.setPen(QPen(Qt.GlobalColor.blue, 2))
        self.setBrush(QColor(51, 153, 255))
        self.setAcceptHoverEvents(True)  # Enable hover events to show enabled/disabled state
        
        # Initially disable the node
        self.enabled = False
        self.setBrush(QColor(150, 150, 150))  # Gray color to indicate disabled state
        
        # Create label text item and position it
        self.text = QGraphicsTextItem(label, self)
        self.text.setDefaultTextColor(Qt.GlobalColor.white)
        self.text.setFont(QFont("Arial", 10))
        self.text.setPos(x - 20 + 5, y - 20 + 5)

    # Override mousePressEvent to handle clicks
    def mousePressEvent(self, event):
        if self.enabled:
            # Call the appropriate method in the main window based on the label
            method_name = f"on_{self.label.replace(' ', '_').lower()}_clicked"
            if hasattr(self.parent, method_name):
                getattr(self.parent, method_name)()
        else:
            print(f"{self.label} node is disabled.")

    def enable(self):
        """Enable the node to be clickable and change color."""
        self.enabled = True
        self.setBrush(QColor(51, 153, 255))  # Light blue color to indicate enabled state

class PipelineTree(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pipeline Flow with Branches")
        self.setGeometry(100, 100, 800, 800)

        # Set up graphics view and scene
        self.graphics_view = QGraphicsView()
        self.graphics_scene = QGraphicsScene()
        self.graphics_view.setScene(self.graphics_scene)

        # Set up main layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.graphics_view)
        self.setCentralWidget(central_widget)

        # Store pipeline steps
        self.pipeline_steps = []

        # Populate the graphics scene with pipeline nodes
        self.create_pipeline_flow()

    def create_pipeline_flow(self):
        # Define pipeline steps and positions
        steps = [
            ("Initialization", 400, 50),
            ("Synthesis", 400, 150),
            ("Floor Plan", 400, 250),
            ("Placement", 400, 350),
            ("CTS", 400, 450),
            ("Route", 400, 550),
            ("RCEXT", 400, 650),
            ("STA", 400, 750),
            ("PDV", 400, 850),
            ("EMIR", 400, 950),
            ("Power Analysis", 400, 1050)
        ]

        # Positions for branching nodes
        branches = [
            ("LEC1", 300, 250),  # Branch for LEC1 to the left of "Floor Plan"
            ("LEC2", 500, 350),  # Branch for LEC2 to the right of "Placement"
        ]

        # Create main pipeline nodes
        previous_item = None
        for i, (step, x, y) in enumerate(steps):
            # Create clickable node and disable it initially
            node = ClickableNode(step, x, y, self)
            self.graphics_scene.addItem(node)
            self.pipeline_steps.append(node)

            # Draw a line to the next node
            if previous_item:
                prev_x, prev_y = previous_item
                self.graphics_scene.addLine(prev_x, prev_y, x, y - 20, QPen(Qt.GlobalColor.blue))

            # Save current node position for the next line
            previous_item = (x, y + 20)

        # Enable the first node
        if self.pipeline_steps:
            self.pipeline_steps[0].enable()

        # Create branching nodes
        for branch, bx, by in branches:
            # Create clickable branch node and disable it initially
            branch_node = ClickableNode(branch, bx, by, self)
            self.graphics_scene.addItem(branch_node)

            # Draw a line from the main pipeline to the branch node
            if branch == "LEC1":
                self.graphics_scene.addLine(400, 250, bx + 20, by, QPen(Qt.GlobalColor.blue))  # Connect "Floor Plan" to "LEC1"
            elif branch == "LEC2":
                self.graphics_scene.addLine(400, 350, bx - 20, by, QPen(Qt.GlobalColor.blue))  # Connect "Placement" to "LEC2"

    # Define empty functions for each pipeline step, enabling the next node when clicked
    def on_initialization_clicked(self):
        print("Initialization node clicked.")
        self.enable_next_step("Initialization")

    def on_synthesis_clicked(self):
        print("Synthesis node clicked.")
        self.enable_next_step("Synthesis")

    def on_floor_plan_clicked(self):
        print("Floor Plan node clicked.")
        self.enable_next_step("Floor Plan")

    def on_placement_clicked(self):
        print("Placement node clicked.")
        self.enable_next_step("Placement")

    def on_cts_clicked(self):
        print("CTS node clicked.")
        self.enable_next_step("CTS")

    def on_route_clicked(self):
        print("Route node clicked.")
        self.enable_next_step("Route")

    def on_rcext_clicked(self):
        print("RCEXT node clicked.")
        self.enable_next_step("RCEXT")

    def on_sta_clicked(self):
        print("STA node clicked.")
        self.enable_next_step("STA")

    def on_pdv_clicked(self):
        print("PDV node clicked.")
        self.enable_next_step("PDV")

    def on_emir_clicked(self):
        print("EMIR node clicked.")
        self.enable_next_step("EMIR")

    def on_power_analysis_clicked(self):
        print("Power Analysis node clicked.")
        self.enable_next_step("Power Analysis")

    def on_lec1_clicked(self):
        print("LEC1 node clicked.")

    def on_lec2_clicked(self):
        print("LEC2 node clicked.")

    def enable_next_step(self, current_step):
        """Enables the next node in sequence based on the current step."""
        for i, node in enumerate(self.pipeline_steps):
            if node.label == current_step and i + 1 < len(self.pipeline_steps):
                # Enable the next node
                self.pipeline_steps[i + 1].enable()
                break

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PipelineTree()
    window.show()
    sys.exit(app.exec())
