from Controller.app_controller import AppController


if __name__ == "__main__":
  # Dependency Inject services later
  app: AppController = AppController()
  app.run()