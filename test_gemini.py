import google.generativeai as genai

genai.configure(api_key="AIzaSyDf22ITgR26v-DlL90SxfV1BHjz8Jn1NGM")

models = genai.list_models()
for model in models:
    print(model.name)


