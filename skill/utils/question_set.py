class QuestionSet:
    def __init__(self, questions: list):
        self.current = None
        self.questions = iter(questions)

    def __next__(self):
        self.current = next(self.questions)
        return self.current
