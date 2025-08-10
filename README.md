# E-Waste Sorting System

Automated e-waste detection and sorting using computer vision and Arduino servos.


### Install Dependencies
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Upload Arduino Code
Upload `arduino/simple_arduino_servo.ino` to your Arduino

## 📁 Main Scripts

### 1. `main.py` - Manual Capture & Sort
Take photos manually and sort items
```bash
python main.py
```

### 2. `auto_detect_sort.py` - Automatic Detection & Sort
Automatically detects objects and sorts them
```bash
python auto_detect_sort.py
```

### 3. `move_left.py` - Test Left Motor
Move left servo (safe bin)
```bash
python move_left.py
```

### 4. `move_right.py` - Test Right Motor
Move right servo (unsafe bin)
```bash
python move_right.py
```

| Level | Action |
|-------|--------|
| Safe to Shred | Sort LEFT |
| Requires Preprocessing | Sort RIGHT |
| Do Not Shred | Sort RIGHT |
| Discard | Sort RIGHT |
