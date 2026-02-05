class ImageHistory:
    def __init__ (self):
        self.undoStack = []
        self.redoStack = []

    def save(self, image):
        self.undoStack.append(image.copy())
        self.redoStack.clear()
    
    def undo(self, current):
        if self.undoStack:
            self.redoStack.append(current.copy())
            return self.undoStack.pop()
        return current

    def redo(self, current):
        if self.redoStack:
            self.undoStack.append(current.copy())
            return self.redoStack.pop()
        return current