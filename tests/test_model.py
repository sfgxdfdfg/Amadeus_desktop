from modules.essentials.emotion_analysis_hugging_face import *

class Test:
    def __init__(self):
        self.emotion_analyzer = EmotionAnalysis()
    
    def run(self):
        while True:
            user_input = input('sentence: ')
            result = self.emotion_analyzer.analyze_emotion(user_input)
            print(result[0]['label'])

            choice = input('Quit?: ')
            if choice.lower() == 'n':
                pass
            elif choice.lower() == 'y':
                break
            else:
                print('not a valid input, restarting automatically')

if __name__ == "__main__":
    Test().run()