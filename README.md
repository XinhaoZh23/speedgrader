# Speed Grader Pro

Speed Grader Pro is a user-friendly desktop application designed to streamline the grading process. It allows instructors to quickly calculate and format student scores, including bonus points, while maintaining a clean and organized output format.

## Features

- **Intuitive User Interface**: Clean and modern design that's easy to navigate
- **Flexible Question Management**: Support for both regular and bonus questions
- **Automatic Score Calculation**: Instantly calculates total scores with bonus point handling
- **Score Capping**: Automatically caps total scores at 100 points
- **Easy Score Export**: One-click copying of formatted scores
- **Scrollable Interface**: Comfortably handle any number of questions

## Installation

No installation required! Simply download the `Speed Grader Pro.exe` file and run it directly.

## Usage Guide

### Getting Started

1. Launch the application by double-clicking `Speed Grader Pro.exe`
2. The application will automatically center itself on your screen

### Basic Workflow

1. **Enter Question Counts**
   - Specify the number of regular questions
   - Specify the number of bonus questions (optional)
   - Click "Confirm" to proceed

2. **Input Scores**
   - Enter scores for each regular question
   - Enter scores for bonus questions (if any)
   - Click "Calculate Total" to process

3. **View Results**
   - The total score will be displayed prominently
   - Individual question scores will be formatted in the text area
   - Use the "Copy Results" button to copy the formatted scores to clipboard

### Example Output Format
```
1. 10
2. 8
3. 15
4. 12

Bonus:
B1. 5
B2. 3
```

## Tips and Notes

- The application automatically prevents invalid inputs (negative scores)
- Bonus points are added to the total but won't exceed the maximum score of 100
- The window is vertically resizable if you need to see more content
- Use mouse wheel to scroll when there are many questions

## Technical Details

- **Version**: 1.0.0
- **Platform**: Windows
- **Requirements**: No additional software required
- **File Size**: ~50 MB

## Support

For any issues or feature requests, please contact the developer.

## Development

If you're interested in the source code or want to contribute to the project, the application is built using:
- Python 3.9
- Tkinter for GUI
- PyInstaller for executable creation

Required dependencies for development:
```
pyperclip==1.8.2
pyinstaller==6.3.0
```

## License

This software is provided as-is for educational purposes.
