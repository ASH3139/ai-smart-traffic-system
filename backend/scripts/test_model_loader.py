from backend.app.services.detection.model_loader import ModelLoader


def main():

    loader = ModelLoader()

    loader.load()

    print("✅ YOLO Model Loaded Successfully")


if __name__ == "__main__":
    main()
    