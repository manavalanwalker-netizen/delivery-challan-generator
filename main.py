#!/usr/bin/env python3
"""
Delivery Challan PDF Generator
A GUI application to generate delivery challan PDFs
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.gui_application import DeliveryChallanApp

def main():
    app = DeliveryChallanApp()
    app.run()

if __name__ == "__main__":
    main()
