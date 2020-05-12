class QuestionSet:
    def __init__(self, questions: list, save_objects=False):
        self.current = None
        self.questions = iter(questions)
        self._save_objects = save_objects
        if self._save_objects:
            self._saved = []

    def __next__(self):
        self.current = next(self.questions)
        if self._save_objects:
            self._saved.append(self.current)
        return self.current

    @property
    def saved(self):
        if self._save_objects:
            return self._saved
